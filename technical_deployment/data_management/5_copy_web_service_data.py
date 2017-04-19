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

"""Copy files for setting up web service"""

# =============================================================================
# import packages
# =============================================================================
import os 
import config
from distutils.dir_util import copy_tree
from shutil import copyfile

# =============================================================================
# copy files and clean up
# =============================================================================
source = config.train_model_folder
curr = config.ref_dir
dest = config.web_service_folder
f = "config.py"

print("\nCopying files for web service ...\n")

# all files in model training folder
myfiles = copy_tree(source, dest)

# config file
copyfile(os.path.join(curr, f), os.path.join(dest, f)) 

# clean up
files_to_keep = ["config.py", "model.py", "runserver.py", "helpers.py", "helpers_cntk.py", "imdb_data.py", "PARAMETERS.py"]

files_all = []
for f in os.listdir(dest):
    if f.endswith('.py') or f.endswith('.tsv') or f.endswith('.md'):
        files_all.append(f)   

for f in files_all:
    if f not in files_to_keep:
        os.remove(os.path.join(dest, f))    
assert os.path.isfile(os.path.join(config.web_service_folder +  "/../cntk.zip")), "File cntk.zip does not exist in folder /web_service."  
print("Done.")