# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# =============================================================================

"""Download annotations from DocDB and images from Azure Blob"""

# %%
# =============================================================================
# import packages
# =============================================================================
import os
import re
import config
import pydocumentdb.document_client as document_client
from azure.storage.blob import BlockBlobService
from helper import save_roi_label_score, merge_roi_label_score

# %% 
# =============================================================================
# Establish links to Azure Blob and DocDB
# =============================================================================
# Establish a link to blob
block_blob_service = BlockBlobService(account_name=config.storage_account_name,
                                      account_key=config.storage_account_key)

# Establish a link to DocDB
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
# Download images, ROIs, labels, and ETags
# =============================================================================
print("\nDownloading data ...\n")

# four possible values ["testImages", "positive", "negative", "livestream"]
download_group = ["livestream"]

for _, document in enumerate((
        doc for doc in client.ReadDocuments(collection['_self'])
        if doc['usage'] in download_group
)):

    folder = document["usage"]
    sub_dir = os.path.join(config.dir_download, folder)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    # get image info    
    image_id = document["id"]
    f_box = image_id + ".bboxes.tsv"
    f_label = image_id + ".bboxes.labels.tsv"
    f_score = image_id + ".bboxes.scores.tsv"
    f_etag = image_id + ".etag.tsv"
    f_vis = image_id + ".visualize.tsv"

    fname_box = os.path.join(sub_dir, f_box)
    fname_label = os.path.join(sub_dir, f_label)
    fname_score = os.path.join(sub_dir, f_score)
    fname_etag = os.path.join(sub_dir, f_etag)
    fname_vis = os.path.join(sub_dir, f_vis)

    # download rois 
    # if folder in ["positive", "testImages"]:
    with open(fname_box, 'w') as f_box, \
            open(fname_label, 'w') as f_label, \
            open(fname_score, 'w') as f_score, \
            open(fname_etag, 'w') as f_etag:
        f_etag.write(document["_etag"])
        for _, roi in enumerate(document["roiAnnotated"]):
            save_roi_label_score(roi, f_box, f_label, f_score)

            # download an image to a local folder
    blob_url = document["azureBlobUrl"]
    blob_url_header = ("https://" + config.storage_account_name
                       + ".blob.core.windows.net/"
                       + config.blob_container_image + "/")
    print(blob_url_header)
    print(blob_url)
    match = re.search(r'({0})([-\d\w]+)'.format(blob_url_header), blob_url)
    blob_name = match.group(2) + ".jpg"
    f_image = image_id + ".jpg"
    local_image = os.path.join(sub_dir, f_image)
    block_blob_service.get_blob_to_path(config.blob_container_image,
                                        blob_name, local_image)

    merge_roi_label_score(fname_box, fname_label, fname_score, fname_vis)

print("Download complete.")    