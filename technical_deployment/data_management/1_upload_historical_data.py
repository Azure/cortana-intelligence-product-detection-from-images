# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
# =============================================================================

"""Upldoad on-premise images with annotations to Azure Blob and DocDB"""

# =============================================================================
# import packages
# =============================================================================
import os
import re
import pytz
import datetime
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import pydocumentdb.document_client as document_client
import config
from helper import merge_roi_label

# =============================================================================
# Create containers and collections
# =============================================================================
# Establish a link to blob
block_blob_service = BlockBlobService(account_name=config.storage_account_name,
                                      account_key=config.storage_account_key)

# Create a container for saving images
if block_blob_service.create_container(config.blob_container_image):
    print("Container for images was created successfully.")
else:
    print("Container for images exists already.")

# Create a container for saving models
if block_blob_service.create_container(config.blob_container_model):
    print("Container for models was created successfully.")
else:
    print("Container for models exists already.")

# Establish a link to DocDB
client = document_client.DocumentClient(config.documentdb_uri,
                                        {'masterKey': config.documentdb_key})

# check existing databases                                        
# databases = list(client.ReadDatabases())

# check if database exists 
databases = list(client.QueryDatabases({
    "query": "SELECT * FROM r WHERE r.id=@id",
    "parameters": [
        {"name": "@id", "value": config.documentdb_database}
    ]
}))

if len(databases) == 0:
    # Create DocumentDB database
    db = client.CreateDatabase({'id': config.documentdb_database})
else:
    db = next((data for data in client.ReadDatabases()
               if data['id'] == config.documentdb_database))
    print("DocumentDB database exists already.")

# check existing collections
collections = [collection['id'] for collection in list(client.ReadCollections(db['_self']))]

if config.documentdb_collectoion_image not in collections:
    # Create collection for saving image meta-data
    collection = client.CreateCollection(
        db['_self'],
        {'id': config.documentdb_collectoion_image}
    )
else:
    collection = next((coll for coll in client.ReadCollections(db['_self'])
                       if coll['id'] == config.documentdb_collectoion_image))
    print("The colleciton for images exists already.")

if config.documentdb_collectoion_performance not in collections:
    # Create collection for saving model performance
    collection2 = client.CreateCollection(
        db['_self'],
        {'id': config.documentdb_collectoion_performance}
    )
else:
    collection2 = next((coll for coll in client.ReadCollections(db['_self'])
                        if coll['id'] == config.documentdb_collectoion_performance))
    print("The colleciton for model performance exists already.")

# =============================================================================
# upload historic data
# =============================================================================
print("\nUploading data ...\n")
# file_names = []

num_files = 0

for dirname, dirnames, filenames in os.walk(config.image_folder_onprem):
    for filename in filenames:
        # print path to all filenames.
        # print(os.path.join(dirname, filename))

        filename_split = filename.split(".")
        if filename_split[-1] == "jpg":
            f_t = filename_split[0]
            # file_names.append(f_t)

            sub_folder = re.split(r"[/\\]+", dirname)[-1]

            # upload image to Azure blob
            blob_name = "historic_" + sub_folder + "_" + f_t + ".jpg"
            local_image = os.path.join(dirname, filename)
            block_blob_service.create_blob_from_path(
                config.blob_container_image,
                blob_name,
                local_image,
                content_settings=ContentSettings(content_type='image/png')
            )

            blob_url = ("https://" + config.storage_account_name
                        + ".blob.core.windows.net/"
                        + config.blob_container_image + "/" + blob_name)

            # get image information
            appliance_id = "appliance_0"
            usage = sub_folder
            dt_modified = os.path.getmtime(local_image)
            modified_date = datetime.datetime.fromtimestamp(
                dt_modified,
                pytz.timezone('US/Eastern')
            ).isoformat()
            modified_date_UTC = datetime.datetime.utcfromtimestamp(
                dt_modified
            ).isoformat()

            roi_annotated = []
            roi_annotated_dict = {}
            # annotate source info
            annotated_by_user = None
            annotated_by_model = None
            annotated_date = None

            num_files += 1

            if sub_folder in ["positive", "testImages"]:
                # merge roi and label
                f_t_roi = f_t + ".bboxes.tsv"
                fname_box = os.path.join(dirname, f_t_roi)
                f_t_label = f_t + ".bboxes.labels.tsv"
                fname_label = os.path.join(dirname, f_t_label)
                roi_annotated = merge_roi_label(fname_box, fname_label)

                annotated_by_user = config.annotated_by_user_history
                annotated_by_model = None
                dt = os.path.getmtime(fname_box)
                annotated_date = datetime.datetime.fromtimestamp(
                    dt,
                    pytz.timezone('US/Eastern')
                ).isoformat()

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
                "roiSelectiveSearch": [
                ],
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

print("\nData for {} out of 30 images have been uploaded.".format(num_files))
print("Done.") 
