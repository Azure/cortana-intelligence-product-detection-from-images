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

# reference directory, make sure it exists
# ref_dir = "C:\\Users\\lixzhan\\Desktop\\testing"
ref_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# folder where historical data are saved, it should have 3 subfolders: 
#   positive, negative, and testImage; make sure it exists
image_folder_onprem = ref_dir + "\\onprem"
# folder where DocDB data and Azure Blob images are downloaded into
dir_download = ref_dir + "\\..\\trainModel\\data\\grocery"
# folder for manually annotated images, make sure it exists
annotated_image_folder = ref_dir + "\\..\\trainModel\\data\\grocery\\livestream"
# file that has model performance data, make sure it exists
performance_file = ref_dir + "\\..\\trainModel\\performance.txt"
# folder where trained model is saved, make sure it exists
model_folder_local_a = ref_dir + "\\..\\trainModel\\proc\\grocery\\models"
model_folder_local_b = ref_dir + "\\..\\trainModel\\proc\\grocery\\trainedSvm"

# folder where Azure Blob saved models are downloaded into
model_folder_download = ref_dir + "\\modeldownload"

# model version
model_version = "20170327"
# threshold for calculating mAP
threshold = 0.3

# annotation user
annotated_by_user_history = "power user"
annotated_by_user_update = "user1"

# Azure blob account info
# blob_account_name = "lixuntestblob2"
# blob_account_key = "+GJHKY0eOaJZIrusDy2Lt29t6MzWkzMrQTXOPTXZ0WJFHTprMfw6I2qYJ9OMgscb/pf0x3lF07IWJE8bhjwbQw=="
blob_account_name = "lzimages"
blob_account_key = "+aou0UIdgr07gQpZjyHFbPSm5OUqoKHUY9gyTWiyvkxWkmDC7aOem2/rJXgUOtG7H38iEOv53sfT/LE/cSJczw=="

# container for images
blob_container_image = "images" # no need to change this
# container for models
blob_container_model = "models" # no need to change this

# DocumentDB info
documentdb_host = "https://lzimages.documents.azure.com:443/"
documentdb_key = "cc8cWc4sRqqlATisTr5MajSD8a54zggYt9Qy45GemnA5dQNRI7vECIIik3Hev0OTzz971zLTatmcQt3pbOntpw=="
documentdb_database = "detection_db" # no need to change this
# collection for annotations, labels, metadata
documentdb_collectoion_image = 'image_collection' 
# collection for performance with mAP info
documentdb_collectoion_performance = 'performance_collection' 
