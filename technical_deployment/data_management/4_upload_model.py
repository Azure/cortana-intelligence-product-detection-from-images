# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# =============================================================================

"""Upload model to Azure Blob"""

#%%
# =============================================================================
# import packages
# =============================================================================
import os
import config
from azure.storage.blob import BlockBlobService

#%%
# =============================================================================
# Establish links to Azure Blob
# =============================================================================
block_blob_service = BlockBlobService(account_name=config.blob_account_name, 
                                      account_key=config.blob_account_key)

#%% 
# =============================================================================
# Upload model
# =============================================================================
print("Uploading ...")

for dirname, dirnames, filenames in os.walk(config.model_folder_local_a):
    for filename in filenames:
        # print path to all filenames.
        # print(os.path.join(dirname, filename))
         
        local_file = os.path.join(dirname, filename)
        blob_name = config.model_version + "\\" + filename
        block_blob_service.create_blob_from_path(
            config.blob_container_model,
            blob_name,
            local_file
        )
        print(filename + " uploaded.")

for dirname, dirnames, filenames in os.walk(config.model_folder_local_b):
    for filename in filenames:
        # print path to all filenames.
        # print(os.path.join(dirname, filename))
         
        local_file = os.path.join(dirname, filename)
        blob_name = config.model_version + "\\" + filename
        block_blob_service.create_blob_from_path(
            config.blob_container_model,
            blob_name,
            local_file
        )  
        print(filename + " uploaded.")