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

"""Define helper functions."""

import copy


def merge_roi_label(fname_box, fname_label):
    """Merge boundaries and labels for each ROI.

    Args:
        fname_box: full path to file with boundary info.
        fname_label: full path to file with label info.

    Returns:
        roi_annotated: a list of dictionaries with ROI coords and labels.
    """
    # initiate list and dictionary
    roi_annotated = []
    label_dict = {}

    # get rois
    with open(fname_box) as f:
        coords = f.readlines()
    coords = [x.strip() for x in coords]

    # get labels
    with open(fname_label) as f:
        labels = f.readlines()
    labels = [x.strip() for x in labels]

    # merge rois with labels
    for i, label in enumerate(labels):
        label_dict_copy = copy.deepcopy(label_dict)
        label_dict_copy[label] = 1
        roi_entry = {
            "coords": [float(v) for v in coords[i].split("\t")],
            "label": label_dict_copy
        }
        # print(roi_entry)
        roi_annotated.append(roi_entry)

    return roi_annotated


def merge_roi_label_score(fname_box, fname_label, fname_score, fname_vis):
    """Merge boundaries, labels, and scores for each ROI.

    Args:
        fname_box: full path to file with boundary info.
        fname_label: full path to file with label info.
        fname_score: full path to file with score info.
        fname_vis: full path to output file.

    Returns:
        None.
    """

    with open(fname_vis, 'w') as f_vis, \
            open(fname_box, 'r') as f_box, \
            open(fname_label, 'r') as f_label, \
            open(fname_score, 'r') as f_score:
        f_vis.write("label\tscore\tnms\tleft\tbottom\tright\ttop\n")
        for box, label, score in zip(f_box, f_label, f_score):
            # print(box.strip() + "\t" + label.strip() + "\t" + score.strip())
            f_vis.write(label.strip() + "\t" + score.strip()
                        + "\tTRUE\t" + box.strip() + "\n")


def save_roi_label(roi, f_box, f_label):
    """Save boundaries and labels for ROIs into separate files.

    Args:
        roi: dictionary with boundary and label info.
        f_box: destination file for saving boundaries.
        f_label: destination file for saving labels.

    Returns:
        None.
    """
    f_box.write("\t".join(str(int(item)) for item in roi['coords']))
    f_box.write("\n")
    label_d = roi["label"]
    label = max(label_d, key=label_d.get)
    f_label.write("%s\n" % label)


def save_roi_label_score(roi, f_box, f_label, f_score):
    """Save boundaries, labels, and scores for ROIs into separate files.

    Args:
        roi: dictionary with boundary and label info.
        f_box: destination file for saving boundaries.
        f_label: destination file for saving labels.
        f_score: destination file for saving scores.

    Returns:
        None.
    """
    f_box.write("\t".join(str(int(item)) for item in roi['coords']))
    f_box.write("\n")
    label_d = roi["label"]
    key, value = max(label_d.items(), key=lambda x: x[1])
    f_label.write("%s\n" % key)
    f_score.write("%s\n" % value)    
