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

""" Define parameters"""

import os 
import sys

#######################################################################
# Modify these values per the technical deployment guide instructions #
#######################################################################

# Azure blob account info
storage_account_name = "lzimage3"
storage_account_key = "8y7ttvPo3UVEJXgcWt0bLPpzSqEH4isHcElw4w6D4LFVeybdnz9QGq7cKE5zZEZTNAofB4l9KJ3cPlEETQbxSQ=="

# DocumentDB info
documentdb_uri = "https://lzimage3.documents.azure.com:443/"
documentdb_key = "uUJkNr5C7yZx1Gj6W47s4PoC2QpxwKJxja7NyNftv2ZhpVcIQV2E9YRDDB0UTbSi4CL2kgV6HPGfaH9QeCwYXQ=="

# model version
model_version = "20170327"  # format: YYYYMMDD

#######################################
# No need to change the values below! #
#######################################

# reference directory, make sure it exists
# ref_dir = "C:/Users/lixzhan/Desktop/testing"
ref_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# folder where historical data are saved, it should have 3 subfolders: 
#   positive, negative, and testImage; make sure it exists
image_folder_onprem = ref_dir + "/onprem"
# folder where DocDB data and Azure Blob images are downloaded into
dir_download = ref_dir + "/../train_model/data/grocery"
# folder for manually annotated images, make sure it exists
annotated_image_folder = ref_dir + "/../train_model/data/grocery/livestream"
# files that have model performance data, make sure they exist
ap = ref_dir + "/../train_model/evalResults.tsv"
precision_recall = ref_dir + "/../train_model/precisionRecalls.tsv"
# folder where trained model is saved, make sure it exists
model_folder_local_a = ref_dir + "/../train_model/proc/grocery/models"
model_folder_local_b = ref_dir + "/../train_model/proc/grocery/trainedSvm"
# folder where trained model is saved for web service
web_service_a = "proc/grocery/models/"
web_service_b = "proc/grocery/trainedSvm/"
# folder for model training, make sure it exists
train_model_folder = ref_dir + "/../train_model"
# folder for web app, make sure it exists
web_service_folder = ref_dir + "/../web_service/WebApp"

# folder where Azure Blob saved models are downloaded into
model_folder_download = ref_dir + "/modeldownload"

# annotation user
annotated_by_user_history = "power user"
annotated_by_user_update = "user1"

# More Azure blob account info
# container for images
blob_container_image = "images" # no need to change this
# container for models
blob_container_model = "models" # no need to change this

# More DocumentDB info
documentdb_database = "detection_db" # no need to change this
# collection for annotations, labels, metadata
documentdb_collectoion_image = 'image_collection' 
# collection for performance with mAP info
documentdb_collectoion_performance = 'performance_collection' 
