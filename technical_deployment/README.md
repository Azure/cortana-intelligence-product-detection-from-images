# Cortana Intelligence Suite Product Detection from Images Solution

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Setup Steps](#setup-steps)
   - [Azure Storage](#storage)
   - [Create Azure DocumentDB](#docdb)
   - [Provision the Microsoft Data Science Virtual Machine](#dsvm)
   - [Create Web App](#webapp)
- [Manage Historic Data](#manage-historic-data)
- [Train a Model on DSVM](#train-a-model-on-dsvm)
- [Monitor Model Performance](#monitor-model-performance)
- [Deploy a Web Service](#deploy-a-web-service)
- [Retrain Models](#retrain-models)

## Introduction
The objective of this Guide is to demonstrate data pipelines for retailers to detect products from images. Retailers can use the detections to detect which product a customer has picked up from the shelf. This information can also help stores manage product stockings. This tutorial shows how to set up the prediciton service as well as retrain models as new data become available.

The end-to-end solution is implemented in the cloud using Microsoft Azure. The flow in this techincal guide is organized to reflect what we expect customers will do to develop their own solutions. Thus this deployment guid will walk you through the following steps:

- Create Azure Resource Group and add DocumentDB, Azure Storage Blob, Data Science Virtual Machine, Web App, Application Insights to the resource group
- Install Python and related packages to copy data from on-prem to DocumentDB and Azure Storage Blob
- Log onto the Data Science Virtual Machine to download data, train a model, save the model and performance information, and deploy a web service
- Monitor model performace from PowerBI
- Consume the web service

## Prerequisites
The steps described in this guide require the following prerequites:

- **An Azure subscription**: To obtain one, see [Get Azure free trial](https://azure.microsoft.com/en-us/free/)
- A **[Microsoft Power BI](https://powerbi.microsoft.com/en-us/)** account
- An installed copy of **[Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/?gated=0&number=0)**

## Architecture
[Figure 1][pic1] illustrates the Azure architecture for this solution.

[![Figure 1][pic1]][pic1] Figure 1

This figure describes two workflows - the numbers in orange circles are for the model training workflow and those in pink are for the consumption workflow. In the model training workflow, the historical data - including boths images and annotations - will be loaded from you local computer onto DocumentDB and Azure Storage Blob, with images being stored at Azure Storage Blob and Annotation information at DocumentDB. The model training process is completed on Data Science Virtual Machine (DSVM) after downloading data form DocumentDB and Azure Storage Blob onto the DSVM. The model will be saved on Azure Storage Blob and performance on DocumentDB. Then the model can be deployed as a web service. New data can be annotated and used for model retraining.

In the consumption workflow, the test-website sends images to the web service which identifies products, saves the images and scores, and returns the scored image back to the users. Application Insights will be used to monitor the web service.

## Setup Steps
The first thing we'll do is to create an Azure Resource Group and add to it DocumentDB, Azure Storage Blob, DSVM, and Web App.

### Choose a Unique String

You will need a unique string to identify your deployment because some Azure services (e.g. Azure Storage)  require a unique name for each instance across the service. We suggest you use only letters and numbers in this string and the length should not be greater than 9.

We suggest you use "[UI]image[N]"  where [UI] is the user's initials and [N] is a random integer that you choose. Characters must be entered in lowercase. Please create a memo file and write down "unique:[unique]" with "[unique]" replaced with your actual unique string.

### Create an Azure Resource Group

1. Log into the [Azure Management Portal](https://ms.portal.azure.com).
2. Click **Resource groups** button on upper left (hover over the buttons to view their names or ), then click **+Add** button to add a resource group.
3. Enter your **unique string** for the resource group and choose your subscription.
4. For **Resource Group Location**, you can choose one that's closest to you.

Please save the information to your memo file in the form of the following table. Replace the content in [] with its actual value.

| **Azure Resource Group** |                     |
|------------------------|---------------------|
| resource group name    |[unique]|
| region              |[region]||


In this tutorial, all resources will be generated in the resource group you just created. You can easily access these resources from the resource group overview page, which can be accessed as follows:

1. Log into the [Azure Management Portal](https://ms.portal.azure.com).
2. Click the **Resource groups** button on the upper-left of the screen.
3. Choose the subscription your resource group resides in.
4. Search for (or directly select) your resource group in the list of resource groups.

<a name="storage"></a>
### Create an Azure Storage Account

In this step as well as all remaining steps, if any entry or item is not mentioned in the instruction, please leave it as the default value.

1. Go to the [Azure Portal](https://ms.portal.azure.com) and navigate to the resource group you just created.
2. In ***Overview*** panel, click **+Add** to add a new resource. Enter **Storage Account** and hit "Enter" key to search.
3. Click on **Storage account - blob, file, table, queue** offered by Microsoft (in the "Storage" category).
4. Click **Create** at the bottom of the description panel.
5. Enter your **unique string** for "Name."
6. Make sure the selected resource group is the one you just created. If not, choose the resource group you created for this solution.
7. Leaving the default values for all other fields, click the **Create** button at the bottom.
8. Go back to your resource group overview and wait until the storage account is deployed. To check the deployment status, click on the Notifications icon on the top right corner as shown in the following figure.

[![Figure 2][pic2]][pic2]

Ater a successful deployment you should see a figure like below.

[![Figure 3][pic3]][pic3]

Get the primary key for the Azure Storage Account which will be used in the Python scripts to upload and download data by following these steps:

1. Click the created storage account. In the new panel, click on **Access keys**.
1. In the new panel, click the "Click to copy" icon next to `key1`, and paste the key into your memo.

| **Azure Storage Account** |                     |
|------------------------|---------------------|
| Storage Account        |[unique string]|
| Access Key     |[key]             ||

<a name="docdb"></a>
### Create Azure DocumentDB

1. Go to the [Azure Portal](https://ms.portal.azure.com) and navigate to the resource group you just created.
2. In ***Overview*** panel, click **+Add** to add a new resource. Enter **documentdb** and hit "Enter" key to search.
3. Click on **NoSQL (DocumentDB)** offered by Microsoft (in the "Storage" category).
4. Click **Create** at the bottom of the description panel.
5. Enter your **unique string** for "ID."
6. Make sure **DocumentDB** is selected for "NoSQL API."
7. Make sure the selected resource group is the one you just created. If not, choose the resource group you created for this solution.
8. Leaving the default values for all other fields, click the **Create** button at the bottom.
9. Go back to your resource group overview and wait until DocumentDB is deployed as reported in the Notifications area.

Get the primary key for the DocumentDB account which will be used in the Python scripts to upload and download data by following these steps:

1. Click the created DocumentDB. In the new panel, click on **keys.**
1. In the new panel, click the "Click to copy" icon next to `URI` and paste the key into your memo. Repeat the same process for `PRIMARY KEY.`

| **DocumentDB Account** |                     |
|------------------------|---------------------|
| URI        |[uri]|
| Access Key     |[key]             ||

<a name="dsvm"></a>
### Provision the Microsoft Data Science Virtual Machine

1. Go to the [Azure Portal](https://ms.portal.azure.com) and navigate to the resource group you just created.
2. In ***Overview*** panel, click **+Add** to add a new resource. Enter **Data Science Virtual Machine** and hit "Enter" key to search.
3. Click on **Data Science Virtual Machine** offered by Microsoft (in the "Compute" category).
4. Click **Create** at the bottom of the description panel.
5. Enter your **unique string** for "Name."
6. Enter a user name and save it to your memo file.
7. Enter your password and confirm it. Then save it to your memo file.
8. Make sure the selected resource group is the one you just created. If not, choose the resource group you created for this solution.
9. Leaving the default values for all other fields, click the **OK** button at the bottom.
10. On the ***Size*** panel that shows up, choose a size and click the **Select** button.
11. On the ***Settings*** panel that shows up, use the default values for all fields and click the **OK** button.
12. On the ***Summary*** panel that shows up, double check it and click the **OK** button.
13. On the ***Buy*** panel that shows up, click the **Purchase** button. You can ignore the warning message `The highlighted Marketplace purchase(s) are not covered by your Azure credits, and will be billed separately.`
14. Go back to your resource group overview and wait until DSVM is deployed as reported in the Notifications area.

Save your credentials to the memo file.

| **DSVM** |                     |
|------------------------|---------------------|
| username        |[username]|
| password     |[password]  ||

Once the VM is created, you can remote desktop into it using the account credentials that you provided. To get access link, follow these steps:

1. From the Resource Group click the created DSVM (type "Virtual machine").
2. In ***Overview*** panel, click on the **Connect** button at the top left corner to download the .rdp file. We'll use this file later.

<a name="webapp"></a>
### Create Web App

1. Go to the [Azure Portal](https://ms.portal.azure.com) and navigate to the resource group you just created.
2. In ***Overview*** panel, click **+Add** to add a new resource. Enter **Web App** and hit "Enter" key to search.
3. Click on **Web App** offered by Microsoft (in the "Web + Mobile" category).
4. Click **Create** at the bottom of the description panel.
5. Enter your **unique string** for "App name."
6. Make sure the selected resource group is the one you just created. If not, choose the resource group you created for this solution.
7. Click on "App Service plan/Location" and then **+Create New**.
8. Enter your **unique string** for "App Service plan."
9. Click on "Pricing tier" and choose "S1 Standard", then click on **Select.**
10. Click **OK** to confirm the App Service plan.
11. Click **On** for "Application Insights."
12. Leaving the default values for all other fields, click the **Create** button at the bottom.

Now that the web app has been created, we'll deploy a web service to this app after training a model.

## Manage Historic Data
As described in the architecture, we assume that there are some data on you local machine and we need to save those images onto DocumentDB and Azure Storage Blob. The demo data are saved in the folder /dataManagement. To download the content of this folder, you can use either of two approaches:

- Open the [DownGit](https://minhaskamal.github.io/DownGit/#/home) site and enter "link to folder" then click on **Download** to download the folder. This approach just downloads the data we need and is faster. Unzip the downloaded file.
- Download the entir repository by clicking on the **Clone or download** button of the GitHub repository and then **Download ZIP**. this approach downloads the entire repositor and takes longer.

Open the "config.py" file and provide the following values from your memo file:

- 

Download Python 3.5.3 from [this site](https://www.python.org/downloads/) and install it. Then go to the command window and type the following:

````bash
cd path-to-dataManagement-folder
pip install -r requirements.txt


````

## Configure DSVM

## Train a Model on DSVM

## Monitor Model Performance

## Deploy a Web Service

## Retrain Models






[pic1]: https://cloud.githubusercontent.com/assets/9322661/24459697/2caf4612-146a-11e7-97e7-3b628cd7f760.PNG
[pic2]: https://cloud.githubusercontent.com/assets/9322661/24463987/738fb9a2-1476-11e7-8273-17107a76cbd5.png
[pic3]: https://cloud.githubusercontent.com/assets/9322661/24463988/739306f2-1476-11e7-811f-f8debc7a59b9.png





