import os

os.environ['PATH'] = r'D:\home\site\wwwroot\cntk\cntk;' + os.environ['PATH']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

import sys, importlib, random
import PARAMETERS
import base64
import urllib
import numpy as np
import cntk
from PIL import Image, ImageOps
from io import BytesIO
from flask import Flask, render_template, json, request
from flask_cors import CORS
import pytz
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import datetime
import config
import pydocumentdb.document_client as document_client

app = Flask(__name__)

# Establish a link to blob
block_blob_service = BlockBlobService(account_name=config.blob_account_name,
                                      account_key=config.blob_account_key)

# Establish a link to DocDB
client = document_client.DocumentClient(config.documentdb_host,
                                        {'masterKey': config.documentdb_key})

# Read databases and take first since id should not be duplicated.
db = next((data for data in client.ReadDatabases()
           if data['id'] == config.documentdb_database))

# Read collections and take first since id should not be duplicated.
collection = next((coll for coll in client.ReadCollections(db['_self'])
                   if coll['id'] == config.documentdb_collectoion_image))

# CORS on entry-point
cors = CORS(app, resources={r"/api/uploader": {"origins": "*"}})

# PRELOAD Params
locals().update(importlib.import_module("PARAMETERS").__dict__)

# Parameters
classifier = 'svm'
svm_experimentName = 'exp1'

# no need to change these parameters
boAddSelectiveSearchROIs = True
boAddGridROIs = True
boFilterROIs = True
boUseNonMaximaSurpression = True

# load cntk model
model_path = "WebApp/proc/grocery/models/frcn_svm.model"
model = load_model(model_path)
#z_out = combine([model.outputs[2].owner])

if classifier == "svm":
    print("Loading svm weights..")
    tstart = datetime.datetime.now()
    svmWeights, svmBias, svmFeatScale = loadSvm(trainedSvmDir, svm_experimentName)
    print("Time loading svm [ms]: " + str((datetime.datetime.now() - tstart).total_seconds() * 1000))
else:
    svmWeights, svmBias, svmFeatScale = (None, None, None)

@app.route("/", methods=['GET'])
def load():
    return render_template('index.html')
    
@app.route("/uploader", methods=['POST'])
def upload_file():
    file = request.files['file']

    # save to blob
    appliance_id, blob_url, modified_date, modified_date_utc, usage = save_file(file)

    file.stream.seek(0)

    # score
    img = Image.open(BytesIO(file.read())).convert('RGB')
    roi_annotated, roi_annotated_dict, roi_selective_search, scored_image = run_some_deep_learning_cntk(img)

    model_version = config.model_version

    upload_docdb(appliance_id, blob_url, modified_date,
                 modified_date_utc, usage, roi_annotated, roi_annotated_dict, roi_selective_search, model_version)

    return render_template('index.html', **locals())
    
@app.route("/api/uploader", methods=['POST'])
def api_upload_file():

    file = request.files['file']

    # save to blob
    appliance_id, blob_url, modified_date, modified_date_utc, usage = save_file(file)

    file.stream.seek(0)

    # score
    img = Image.open(BytesIO(file.read())).convert('RGB')
    roi_annotated, roi_annotated_dict, roi_selective_search, scored_image = run_some_deep_learning_cntk(img)

    model_version = config.model_version

    upload_docdb(appliance_id, blob_url, modified_date,
                 modified_date_utc, usage, roi_annotated, roi_annotated_dict, roi_selective_search, model_version)

    return json.dumps(scored_image)


def save_file(file):
    print(file)

    # get image information
    filename = file.filename
    print(filename)
    file_name_split = os.path.splitext(filename)
    main_name = file_name_split[0]
    appliance_id = main_name.split("-")[0]
    usage = "livestream"
    # dt_modified = os.path.getmtime(file)
    # modified_date = datetime.datetime.fromtimestamp(
    #     dt_modified,
    #     pytz.timezone('US/Eastern')
    # ).isoformat()
    # modified_date_utc = datetime.datetime.utcfromtimestamp(
    #     dt_modified
    # ).isoformat()

    # dt_modified = str(datetime.datetime.now())
    dt_modified = ""
    modified_date =  dt_modified
    modified_date_utc = dt_modified

    # save to blob
    blob_name = "live_stream_" + filename
    print(blob_name)

    block_blob_service.create_blob_from_stream(
        config.blob_container_image,
        blob_name,
        file,
        content_settings=ContentSettings(content_type='image/png')
    )

    blob_url = ("https://" + config.blob_account_name
                + ".blob.core.windows.net/"
                + config.blob_container_image + "/" + blob_name)
    print(blob_url)

    return appliance_id, blob_url, modified_date, modified_date_utc, usage

def upload_docdb(appliance_id, blob_url, modified_date,
    modified_date_UTC, usage, roiAnnotated, roiAnnotatedDict, roiSelectiveSearch, modelVersion):

    roi_annotated = roiAnnotated
    roi_annotated_dict = roiAnnotatedDict
    # annotate source info
    annotated_by_user = None
    annotated_by_model = modelVersion
    annotated_date = datetime.datetime.utcnow().isoformat()
    roi_selective_search = roiSelectiveSearch
    
    # create the document
    entry = {
        "applianceID": appliance_id,
        "azureBlobUrl": blob_url,
        "modifiedDate": modified_date,
        "modifiedDateUTC": modified_date_UTC,
        "usage": usage,
        "annotatedByUser": annotated_by_user,
        "annotatedByModel": annotated_by_model,
        "annotatedDate": annotated_date,
        "roiAnnotated": roi_annotated,
        "roiAnnotatedDict": roi_annotated_dict, 
        "roiSelectiveSearch": roi_selective_search,
        "annotationHistory": [
            {
                "annotatedByUser": annotated_by_user,
                "annotatedByModel": annotated_by_model,
                "annotatedDate": annotated_date,
                "roiAnnotated": roi_annotated,
            }
        ]
    }

    # upload the document
    document = client.CreateDocument(collection['_self'], entry)

def run_some_deep_learning_cntk(pil_image):
    # Load image
    open_cv_image = np.array(pil_image)
    imgOrig = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    imgPath = open_cv_image
    # Note: had to make alteration (cntk_helpers.py)
    # imgDebug = imresize(imread(imgPath), scale)
    # TO: imgDebug = imresize(imgPath, scale)
    currRois = computeRois(imgOrig, boAddSelectiveSearchROIs, boAddGridROIs, boFilterROIs, ss_kvals, ss_minSize,
                           ss_max_merging_iterations, ss_nmsThreshold,
                           roi_minDimRel, roi_maxDimRel, roi_maxImgDim, roi_maxAspectRatio, roi_minNrPixelsRel,
                           roi_maxNrPixelsRel, grid_nrScales, grid_aspectRatios, grid_downscaleRatioPerIteration)

    currRois = currRois[:cntk_nrRois]  # only keep first cntk_nrRois rois
    imgPadded = imresizeAndPad(imgOrig, cntk_padWidth, cntk_padHeight)
    _, _, roisCntk = getCntkInputs(imgPath, currRois, None, train_posOverlapThres, nrClasses, cntk_nrRois,
                                   cntk_padWidth, cntk_padHeight)
    arguments = {
        model.arguments[0]: [np.ascontiguousarray(np.array(imgPadded, dtype=np.float32).transpose(2, 0, 1))],
    # convert to CNTK's HWC format
        model.arguments[1]: [np.array(roisCntk)]
    }
    dnnOutputs = model.eval(arguments)[0][0]
    dnnOutputs = dnnOutputs[:len(currRois)]  # remove the zero-padded rois
    labels, scores = scoreRois(classifier, dnnOutputs, svmWeights, svmBias, svmFeatScale, len(classes),
                               decisionThreshold=vis_decisionThresholds[classifier])
    # perform non-maxima surpression
    nmsKeepIndices = []
    if boUseNonMaximaSurpression:
        nmsKeepIndices = applyNonMaximaSuppression(nmsThreshold, labels, scores, currRois)
    imgDebug = visualizeResults(imgPath, labels, scores, currRois, classes,
                                nmsKeepIndices, boDrawNegativeRois=False, boDrawNmsRejectedRois=False)

    # Return processed as stream
    ret_imgio = BytesIO()
    imgDebug = Image.fromarray(imgDebug)
    imgDebug.save(ret_imgio, 'PNG')
    processed_file = base64.b64encode(ret_imgio.getvalue())

    roi_selective_search = [
        {
            "coords": [float(r[0]), float(r[1]), float(r[2]), float(r[3])],
            "label": {classes[int(l)]: float(s)}
        } for l, s, r in zip(labels, scores, currRois)
    ]
    
    roi_annotated = [
        {
            "coords": [float(r[0]), float(r[1]), float(r[2]), float(r[3])],
            "label": {classes[int(l)]: float(s)}
        } for l, s, r, i in zip(labels, scores, currRois, range(len(labels))) if (i in nmsKeepIndices) and classes[int(l)] != "__background__"
    ]

    roi_annotated_list = [ classes[int(l)] for l, i in zip(labels, range(len(labels))) if (i in nmsKeepIndices) and (classes[int(l)] != "__background__")]
    print(roi_annotated_list)

    roi_annotated_dict = dict()
    for e in roi_annotated_list:
      roi_annotated_dict[e] = roi_annotated_dict.get(e, 0) + 1
          
    return roi_annotated, roi_annotated_dict, roi_selective_search, urllib.parse.quote(processed_file)


