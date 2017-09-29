# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# =============================================================================

"""Upload ROIs and labels to DocDB"""

# %%
# =============================================================================
# import packages
# =============================================================================
import os
import pytz
import config
import pydocumentdb.document_client as document_client
import datetime
from helper import merge_roi_label

# %%
# =============================================================================
# Establish links to DocDB
# =============================================================================
client = document_client.DocumentClient(config.documentdb_uri,
                                        {'masterKey': config.documentdb_key})

# Read databases and take first since id should not be duplicated.
db = next((data for data in client.ReadDatabases()
           if data['id'] == config.documentdb_database))

# Read collections and take first since id should not be duplicated.
collection = next((coll for coll in client.ReadCollections(db['_self'])
                   if coll['id'] == config.documentdb_collectoion_image))

# %%
# =============================================================================
# Upload ROIs and labels to DocDB
# =============================================================================
print("\nUploading annotations ...\n")

for dirname, dirnames, filenames in os.walk(config.annotated_image_folder):
    for filename in filenames:
        # print path to all filenames.
        # print(os.path.join(dirname, filename))

        filename_split = filename.split(".")
        if filename_split[-1] == "jpg":
            f_t = filename_split[0]
            # file_names.append(f_t)

            # get etag
            f_t_etag = f_t + ".etag.tsv"
            fname_etag = os.path.join(dirname, f_t_etag)
            with open(fname_etag) as f:
                etag = f.readlines()
            etag = etag[0]

            # purpose of annotation: positive, negative, or testImage
            usage = "positive"

            # merge roi and label
            f_t_roi = f_t + ".bboxes.tsv"
            fname_box = os.path.join(dirname, f_t_roi)
            f_t_label = f_t + ".bboxes.labels.tsv"
            fname_label = os.path.join(dirname, f_t_label)
            roi_annotated = merge_roi_label(fname_box, fname_label)

            # annotate source info            
            annotated_by_user = config.annotated_by_user_update
            annotated_by_model = None
            dt = os.path.getmtime(fname_box)
            annotated_date = datetime.datetime.fromtimestamp(
                dt,
                pytz.timezone('US/Eastern')
            ).isoformat()

            document = next((
                doc for doc
                in client.ReadDocuments(collection['_self']) if doc['id'] == f_t
            ))

            if etag == document["_etag"]:
                document["usage"] = usage
                document["annotatedByUser"] = annotated_by_user
                document["annotatedByModel"] = annotated_by_model
                document["annotatedDate"] = annotated_date
                document["roiAnnotated"] = roi_annotated

                document["annotationHistory"].append(
                    {
                        "annotatedByUser": annotated_by_user,
                        "annotatedByModel": annotated_by_model,
                        "annotatedDate": annotated_date,
                        "roiAnnotated": roi_annotated
                    }
                )

                replaced_document = client.ReplaceDocument(document['_self'],
                                                           document)
                print("Update was a success.")
            else:
                print("Error: This document has been updated since your last "
                      + "download. Please download the most recent copy to "
                      + "annotate and then upload.")

print("Done.")