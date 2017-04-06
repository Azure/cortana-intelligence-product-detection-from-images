import sys, os, importlib, random
import PARAMETERS
import json

locals().update(importlib.import_module("PARAMETERS").__dict__)

sub_dir = "C:\\Users\\lixun\\Desktop\\end2end\\trainModel\\data\\grocery\\livestream"
file_name = "908f29bf-b054-4b57-86b8-2f5bf60dcce6"

imgPath = os.path.join(sub_dir, file_name + ".jpg")
vis = os.path.join(sub_dir, file_name + ".visualize.tsv")

labels2, scores2, currRois2, nmsKeepIndices2 = parseDetectionsFile(vis, lutClass2Id)
imgDebug2 = visualizeResults(imgPath, labels2, scores2, currRois2, classes, nmsKeepIndices2,  # identical to imgDebug
                             boDrawNegativeRois=False, boDrawNmsRejectedRois=False)

imshow(imgDebug2, waitDuration=0, maxDim=800)