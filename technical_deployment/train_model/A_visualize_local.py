import sys, os, importlib, random
import PARAMETERS
import json

locals().update(importlib.import_module("PARAMETERS").__dict__)

sub_dir = "./data/grocery/livestream"

# Change this value to the name of an image file in "sub_dir" (no extension)
file_name = "908f29bf-b054-4b57-86b8-2f5bf60dcce6"

if not os.path.exists(os.path.join(sub_dir, file_name + ".jpg")):
	print('''
Exiting: could not find a file named '{}.jpg' in the
./data/grocery/livestream directory. Have you run the script
../data_management/6_annotation_download_data.py and updated the
'file_name' variable definition in ./A_visualize_local.py?
'''.format(file_name))
	sys.exit(1)

imgPath = os.path.join(sub_dir, file_name + ".jpg")
vis = os.path.join(sub_dir, file_name + ".visualize.tsv")

labels2, scores2, currRois2, nmsKeepIndices2 = parseDetectionsFile(vis, lutClass2Id)
imgDebug2 = visualizeResults(imgPath, labels2, scores2, currRois2, classes, nmsKeepIndices2,  # identical to imgDebug
                             boDrawNegativeRois=False, boDrawNmsRejectedRois=False)

imshow(imgDebug2, waitDuration=0, maxDim=800)