# =============================================================================
# Copyright 2017 Microsoft. All Rights Reserved.
# =============================================================================

"""Upload performance to DocCB"""

#%%
# =============================================================================
# import packages
# =============================================================================
import config
import pydocumentdb.document_client as document_client

#%%
# =============================================================================
# Establish links to DocDB
# =============================================================================
# Establish a link to DocDB
client = document_client.DocumentClient(config.documentdb_host, 
                                        {'masterKey': config.documentdb_key})
                                        
# Read databases and take first since id should not be duplicated.
db = next((data for data in client.ReadDatabases() 
           if data['id'] == config.documentdb_database))

# Read collections and take first since id should not be duplicated.
collection = next((coll for coll in client.ReadCollections(db['_self']) 
             if coll['id'] == config.documentdb_collectoion_performance))

#%%
# =============================================================================
# upload performance to DocDB
# =============================================================================
# read performance file
with open(config.performance_file) as f:
    perf = f.readlines()
perf = [x.strip() for x in perf]

# convert performance info into a dictionary
mylist = []
for _, item in enumerate(perf):
    # print(item)
    row = [v for v in item.split("\t")]
    # print(row)
    mylist.append(row)

m_ap = dict(mylist)
# m_ap

# create the document
entry = {
    "modelVersion": config.model_version,
    "threshold": config.threshold,
    "mAP": m_ap
}

# upload the document   
document = client.CreateDocument(collection['_self'], entry)

