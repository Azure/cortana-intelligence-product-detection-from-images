# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# =============================================================================

"""Upload performance to DocCB"""

# %%
# =============================================================================
# import packages
# =============================================================================
import config
import pydocumentdb.document_client as document_client

# %%
# =============================================================================
# Establish links to DocDB
# =============================================================================
# Establish a link to DocDB
client = document_client.DocumentClient(config.documentdb_uri,
                                        {'masterKey': config.documentdb_key})

# Read databases and take first since id should not be duplicated.
db = next((data for data in client.ReadDatabases()
           if data['id'] == config.documentdb_database))

# Read collections and take first since id should not be duplicated.
collection = next((coll for coll in client.ReadCollections(db['_self'])
                   if coll['id'] == config.documentdb_collectoion_performance))

# %%
# =============================================================================
# upload performance to DocDB
# =============================================================================
print("\nUploading performance data ...\n")

# read AP file
with open(config.ap) as f:
    perf = f.readlines()
perf = [x.strip() for x in perf]

# remove header
perf = perf[1:]

# convert performance info into a dictionary
mylist = []
for _, item in enumerate(perf):
    # print(item)
    row = [v for v in item.split("\t")]
    # print(row)
    mylist.append(row)

m_ap = dict(mylist)
# m_ap

average = sum(float(v) for v in m_ap.values()) / len(m_ap)
m_ap["average"] = str(average)

# read precision recall file
with open(config.precision_recall) as f:
    prec_recall = f.readlines()
prec_recall = [x.strip().split("\t") for x in prec_recall]

# remove header
prec_recall = prec_recall[1:]

# save threshold, precision and recall to different lists
prec_recall_list = [list(a) for a in zip(*prec_recall)]
threshold = prec_recall_list[0] + ["0", "10"]
precision = prec_recall_list[1] + ["0", "1"]
recall = prec_recall_list[2] + ["1", "0"]

# create the document
entry = {
    "modelVersion": config.model_version,
    "mAP": m_ap,
    "precisionRecall": {"threshold": threshold, "precision": precision, "recall": recall}
}

# upload the document   
document = client.CreateDocument(collection['_self'], entry)

print("Done.")