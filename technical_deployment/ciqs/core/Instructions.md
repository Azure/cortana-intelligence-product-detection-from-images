Congratulations! Your deployment was successful and now you can explore the deployed resources by following the steps below. It is strongly recommended that you save the content on this page to a safe place so that you can refer to them for future usage.

## Information on Azure Resources

### Web service

The following website uses the trained model to score images. The web service will take about 3 minutes complete the setup the first time you use it.

* *Website*: {Outputs.siteHostName}

### Virtual machine

You can access your newly created Data Science Virtual Machine (DSVM) with Remote Desktop:

* *Computer Name*: {Outputs.vmName}
* *Computer URL*: {Outputs.vmUri}
* *User name*: {Outputs.adminUsername}
* *password*: {Outputs.adminPassword}

### CosmosDB and Azure Storage:

The credentials information for CosmosDB and Azure Storage blob can be found below.

* *CosmosDB*: {Outputs.documentdbs}
* *CosmosDB key*: {Outputs.documentdbKeysP}
* *Azure Storage account name*: {Outputs.storagename}
* *Azure Storage account key*: {Outputs.storageKeysP}

## Next Steps

### Train the model manually

To manually train the model, you can follow the following steps after logging onto the provisioned DSVM:

1. Edit the "config.py" file. Open the "config.py" script in the "C:\imageModel\technical_deployment\data_management" folder from a text editor and provide values for the following fields using the informaiton from above. Make sure you are making changes at the END of the script. 

 - `storage_account_name`
 - `storage_account_key`
 - `documentdb_uri`
 - `documentdb_key`
 - `model_version` (use today's date as value for in the format of `yyyymmdd`)
 
2. Open a "Command Prompt" by pressing Windows + X and selecting Command Prompt.
3. Type the following to train the model
```bash
cd C:\imageModel\technical_deployment\train_model
activate cntk-py35
python 1_computeRois.py
python 2_cntkGenerateInputs.py
python 3_runCntk.py
python 4_trainSvm.py
python 5_evaluateResults.py
python 5_visualizeResults.py
```

4. Save the model. Once you're satisfied with the trained model, you can save its parameters to Blob for future reference. You can also save the performance metrics to DocumentDB. To do so, run the following commands from the same Command Prompt in step 2:
```bash
cd C:\imageModel\technical_deployment\data_management
python 3_upload_model.py
python 4_upload_performance.py
```

5. Update the web service with your model. To make use of your trained model for the web service, go to the link {Outputs.siteHostName}/updatemodel/<modelversion>, replacing <modelversion> with the version of your model, which is the date specified in the in the config.py file in the format `yyyymmdd` (e.g., 20170627).

### Track models from Power BI

You can track and compare performance of models using a Power BI template. Details for doing this can be found at the [Monitor Model Performance](https://github.com/Azure/cortana-intelligence-product-detection-from-images/tree/master/technical_deployment#monitor-model-performance) section of the [Solution How-to Guide for Product Detection from Images](https://github.com/Azure/cortana-intelligence-product-detection-from-images/tree/master/technical_deployment). The credential information for CosmosDB can be found above.