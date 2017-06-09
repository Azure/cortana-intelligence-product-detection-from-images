 # Product Detection from Images - A Cortana Intelligence Solution How-to Guide

In today’s highly competitive and connected environment, retail stores are increasingly finding it imperative to make use of artificial intelligence in their daily operations. Image detection - a technique which can locate and classify objects in images - is a technique that has the potential to bring huge rewards for such stores. For example, retailers can use this technique to determine which product a customer has picked up from the shelf. This information in turn helps stores manage product inventory.

The objective of this Guide is to demonstrate data pipelines for retailers to detect products from images.  This tutorial shows how to set up the prediction service as well as retrain models using newly available data.

## Solution Demo
The snapshot below shows the products detected from an image using the [demo website](http://cntkimages.azurewebsites.net/). You'll be able to deploy the same website using your own Azure subscription by the end of the Guide.

![demo](https://cloud.githubusercontent.com/assets/9322661/25716462/1c50db4e-30cd-11e7-89e1-208dad46b4c6.PNG)

## Solution Dashboard

The snapshot below shows an example PowerBI dashboard showing the performance of the model. It compares precision vs recall for different threshold levels. The performance is near perfect for the sample data, as indicated by the fact that the area under the curve is close to 1. Actual performance for you own data will differ. The provided dashboard template supports comparing model performance for multiple models.  
![dashboard](https://cloud.githubusercontent.com/assets/9322661/25718651/d99fdb12-30d4-11e7-9b71-ab83b4adfc36.PNG)

Below is another dashboard snapshot that shows average precision by class. Users can select the classes that are important and this helps focus on select classes as  the number of classes increases. Performance for multiple models can be compared as well.
![dashboard2](https://cloud.githubusercontent.com/assets/9322661/25718065/bb6a6dd0-30d2-11e7-8cc3-30bc9d5e74ef.PNG)

## Solution Architecture

![Solution Diagram Picture](https://cloud.githubusercontent.com/assets/9322661/24459697/2caf4612-146a-11e7-97e7-3b628cd7f760.PNG)

## What's Under the Hood

The end-to-end solution is implemented in the cloud, using Microsoft Azure. The solution is composed of several Azure components, including data ingest, data storage, data movement, advanced analytics and visualization. The advanced analytics are implemented using [CNTK](https://github.com/Microsoft/CNTK/wiki), a unified deep-learning toolkit by Microsoft. With data ingest, the solution can make predictions based on data that being transferred to Azure from an on-premises environment.

## Getting Started

This solution package contains materials to help both technical and business audiences understand our Product Detection from Images Solution built on the [Cortana Intelligence Suite](https://www.microsoft.com/en-us/server-cloud/cortana-intelligence-suite/Overview.aspx).

## Business Audiences (Coming Soon)

For information on how to tailor Cortana Intelligence to your needs [connect with one of our partners](http://aka.ms/CISFindPartner).

## Technical Audiences

See the [*technical_deployment*](https://github.com/Azure/cortana-intelligence-product-detection-from-images/tree/master/technical_deployment) folder for a full set of instructions on how to put together and deploy a Product Detection from Images Solution using the Cortana Intelligence Suite. For technical problems or questions about deploying this solution, please post in the issues tab of the repository.

## Related Resources
[ObjectDetectionUsingCntk](https://github.com/Azure/ObjectDetectionUsingCntk) offers more details of the model used in this solution.

## Microsoft Open Source Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
