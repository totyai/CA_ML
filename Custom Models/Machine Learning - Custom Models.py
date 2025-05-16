#!/usr/bin/env python
# coding: utf-8

# # Machine Learning - Training Custom Models

# ### What is a Machine Learning Model?

# In[ ]:





# A machine learning model, in essence, is a very complicated math function. Depending on its application, it takes in a certain type of input, and then returns an output. The "insides" of this model are a set of "layers" which are somewhat analogous to terms in a polynomial function, since each layer's impact on the next can be tweaked by adjusting values.  
# 
# Most off-the-shelf solutions that you'll see in the cloud (such as Amazon Comprehend) are effectively a black box to the consumer. As someone writing the code for the previous lab, you didn't have to worry about data sets, training accuracy, or anything to do with "setting up" the model. However, there are services (like Amazon Rekognition) that allow you to get your hands a little dirty in the machine-learning model training field.  
# 
# In this lab we will:
# + Learn how deep-learning algorithms actually learn
# + Gather data for a dataset
# + Discuss why we split our dataset into training and testing batches
# + Build an image recognition model with Amazon Rekognition

# ## Image Recognition and Deep Learning

# If you have used services like Facebook or Instagram before, you've seen first-hand what *image recognition* can do. When you upload a photo to Facebook, it can immediately detect who from your friend's list or mutual friend's list is in said photo. Facebook then applies these results to the faces in the picture and asks if you'd like to tag the friends detected.
# 
# This is thanks to image recognition algorithms, which in this case, have been specialized to look for faces. Algorithms like these are built using a *deep learning* design philosophy. Deep learning models use the concept of "neurons" in their construction. These neurons use math to decide how much data (if any at all) it will send on to the next "layer" of the model based on the data originally given as input. Deep learning implementations also usually lack the human-based "feature-extraction" phase. Instead, the network does the task of extracting features (like eyes in a face, or letters on a sign) while it learns.
# 
# ![Neural network layout example](./assets/MLvsDL.png)
# 
# The neurons can be tweaked by *training* a model on new pieces of data. For example, a facial-recognition network likely won't be good at detecting differences between skyscrapers and low-rises, so we'd have to train a different network for that.
# 
# Training a neural networks is a fairly simple process, though the math is quite complicated and requires knowledge of calculus. Don't worry, no formulas here! A training dataset is fed to the network one item at a time, and the network's performance is cached and applied at the end of each *epoch*, a fancy word for each iteration, or pass of the training dataset. This happens for a human-defined amount of epochs - too few and the algorithm won't learn, but too many and the algorithm might *over*-learn. A model can become so accustomed to the training set that it fails to recognize outside data, which is exactly what we don't want happening with our data. Luckily, with the tools we're using in this lab, most of this has been abstracted away for us. All we must do is create a dataset!
# 
# When creating or curating a dataset for training, you must consider the fact that you have to test the network once its been trained. This can be accomplished by splitting your dataset into training and testing batches. If you've already uploaded a bunch of images in preparation for this lab, don't worry - Rekognition has a way to automatically do this with your dataset. This is the way we'll be doing it in this lab, so that we don't have to go and label a second set of data.
# 
# With this brief crash course of how neural networks operate and how they learn, let's get started!

# ## Using Amazon Rekognition

# For this preliminary example, a model has been built and trained to detect the difference between a skyscraper and a house.  
# 
# A dataset should consist of a wide range of representations of the classifications you'd like to train your model against. For example, if we fed the network exclusively pictures of houses and skyscrapers in the day, it might get confused if we feed it a picture at night, or if its cloudy, etcetra. When building your dataset, try to keep the images diverse but clear and defined.
# 
# For this skyscraper/house example, the images are stored in an S3 bucket - Amazon Rekognition has great integration with S3 that makes the image labelling process easy. These images are stored in an S3 bucket named `clouda-labs-assets` like so:
# + clouda-labs-assets/
#     + custom-model/
#         + training_data/
#             + suburbs/
#                 + 1.jpeg
#                 + 2.jpeg
#                 + *... and so on*
#             + skyscrapers/
#                 + 1.jpeg
#                 + 2.jpeg
#                 + *... and so on*  
#       
# The same `training_data` folder is in the same directory as this notebook as well. To save time in the labelling process, Amazon Rekognition has a nice feature where it will automatically apply labels to images in our dataset based on the sub-folders of the S3 bucket, so my images were automatically labelled correctly just by placing them in the right folder. However, if you'd like to apply multiple tags to an image (for example, training a dataset to determine the different styles between skyscrapers and houses, like "art-deco skyscraper", or "greco-roman house") you will have to do this manually. For this lab we've stuck with one label to keep it simple.
# 
# ### Creating the Amazon S3 Bucket
# You should upload the images into subfolders named as you would want your images labelled. For example, in the skyscrapers/houses example above, we've put all images of skyscrapers in a folder called `skyscrapers`. Your dataset should consist of at least 10 images, so for our example we've done 10 pictures of each. For better results, more training data is usually a good step, however it will increase the time of your model's learning time. The data for this lab is located under `training_data/skyscrapers` and `training_data/suburbs`.
# 
# View the S3 bucket the Cloud Academy lab environment created for you in [the S3 Console](https://s3.console.aws.amazon.com/s3/home?region=us-west-2#) (it's name will begin with "cloudacademylabs-custommodel").
# 
# 
# ### Creating the Rekognition Project
# 1. [Navigate to Amazon Rekognition's landing page](https://console.aws.amazon.com/rekognition/home?region=us-west-2#/)
# 2. Click "Use Custom Labels" on the sidebar on the left
# 3. Click "Get started"
# 4. In the "First time set up" dialog that appears, click "Create S3 bucket" to create a bucket to store the Rekognition project data
# 5. Click "Projects" on the left side
# 6. Click "Create project"
# 7. Give your project a name
# 
# ### Creating the Dataset
# 1. [Find the "Datasets" section](https://us-west-2.console.aws.amazon.com/rekognition/custom-labels?region=us-west-2#/projects) and click the project you just created followed by "Create Dataset"
# 2. Choose the "Import Images from Amazon S3 Bucket" option. Paste in the S3 link for the folder containing your subfolders:
#    + Get the name of CA created [your S3 bucket here](https://s3.console.aws.amazon.com/s3/home?region=us-west-2#) and substitute it for < your_bucket_name > in the following link you should paste (the final value should look similar to s3://cloudacademylabs-custommodel-1ubs5vu8vkgm9/custom-model/training_data/):
#    + s3://< your_bucket_name >/custom-model/training_data/
# 3. Select the "Automatic labelling" checkbox. This is how we apply labels based on the subfolders we've created.
# 4. A bunch of configuration JSON is displayed in the "Make sure that your S3 bucket is correctly configured" section. Follow the instructions in the section to apply the configuration to your bucket. Otherwise, Rekognition might not be able to connect to your bucket. The configuration is a S3 bucket policy that grants Rekognition the required permissions for accessing the image data. Make sure you click "Save" after pasting the configuration into the S3 bucket's "Bucket Policy" field.
# 5. Click "Submit" to create your Dataset
# 
# ### Training your model
# 1. Navigate to your Rekognition [project page](https://us-west-2.console.aws.amazon.com/rekognition/custom-labels?region=us-west-2#/projects)
# 2. Click "Train new model"
# 3. You can leave the project field as is. Select the newly created dataset in the dataset section
# 4. Click "Train Model"
# 
# The training process will take some time (our skyscraper dataset took 44 minutes to learn), so sit back and relax as your model learns!
# 
# In the labs below replace the modelARN variable with the ARN from your trained model. It can be found under the 'Use your model' section after clicking the name of your model once training has completed:
# ![Model ARN Location](./assets/use_model.png)

# # **Lab:** Integrating with Amazon Rekognition using Python
# Once your model is trained you can start the model in Rekognition using the code below. This step will also take some time to complete. You can check the model starting status in the [Rekognition Custom Labels page.](https://console.aws.amazon.com/rekognition/custom-labels#/projects)  Once the status changes from **STARTING** to **RUNNING** you are able to use the model.
# ![Model is running](./assets/model_running.png)  
# 
# The code to start a model can be found below. It utilizes the `start_project_version` method. Replace the modelARN variable with the ARN from your trained model. Highlight the code block and click run.

# In[60]:


import boto3
import json

client = boto3.client(service_name="rekognition", region_name="us-west-2")
modelARN = "arn:aws:rekognition:us-west-2:065157574059:project/calabs-rekog/version/calabs-rekog.2020-05-15T12.17.29/1589559450299"

print("Starting...")
startResp = client.start_project_version(ProjectVersionArn=modelARN, MinInferenceUnits=1)
print(json.dumps(startResp, sort_keys=True, indent=4)) 


# Once the model's status is **RUNNING**, select your model and scroll until you see *Use your model*. The field you see under *Amazon Resource Name (ARN)* is important to have, since its what you send to the API to specify which model you're using. Be careful - as you'll see in the code examples, the API requires you to send it as `ProjectVersionARN` - this is because a "model" is, in Rekognition's view, an iteration/version of the project it resides in.
# 
# ***Documentation for the Python API can be found here: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html***

# ### Classifying an unknown image against the trained model
# 
# After training, and starting your model you can use an unknown image against it to classify what it is.  Simply specify an S3 bucket and image to see the result!  (Note: If you see ResourceNotReadyException below that means the model has not finished starting yet).
# 
# In the example below, we're giving the model the following images, which it hadn't seen when training (this data is located under `validation/`):  
# 
# ![Model example image](./assets/suburb.jpeg)
# ![Model example image](./assets/skyscraper.jpeg)
# 
# Their outputs are shown respectively (be sure to change the `modelARN` and set `<your_bucket_name>` to the name of your S3 bucket before running the code):

# In[61]:


import boto3
import json

client = boto3.client(service_name="rekognition", region_name="us-west-2")
modelARN = "arn:aws:rekognition:us-west-2:065157574059:project/calabs-rekog/version/calabs-rekog.2020-05-15T12.17.29/1589559450299"
print("Getting labels...")
labels = client.detect_custom_labels(ProjectVersionArn=modelARN, Image={
    'S3Object': {
        'Bucket': '<your_bucket_name>',
        'Name': 'custom-model/validation/2.jpeg'
    }
})
print(json.dumps(labels, sort_keys=True, indent=4))


# In[62]:


import boto3
import json

client = boto3.client(service_name="rekognition", region_name="us-west-2")
modelARN = "arn:aws:rekognition:us-west-2:065157574059:project/calabs-rekog/version/calabs-rekog.2020-05-15T12.17.29/1589559450299"

print("Getting labels...")
labels = client.detect_custom_labels(ProjectVersionArn=modelARN, Image={
    'S3Object': {
        'Bucket': '<your_bucket_name>',
        'Name': 'custom-model/validation/3.jpeg'
    }
})
print(json.dumps(labels, sort_keys=True, indent=4))


# In the code block above try supplying different images to see how the model classifies it.  If an image is not matched nothing will be returned in the `CustomLabels` response.  Try an image that is similar to a skyscraper or suburb and a confidence score will be shown on how well the image matches either classification.
# 
# An example response of a home in the suburbs could be like this
# ```
# {
#     "CustomLabels": [
#         {
#             "Confidence": 94.11199951171875, 
#             "Name": "suburbs"
#         }
#     ], 
#     "ResponseMetadata": {
#         "HTTPHeaders": {
#             "connection": "keep-alive", 
#             "content-length": "68", 
#             "content-type": "application/x-amz-json-1.1", 
#             "date": "Sun, 17 May 2020 14:48:55 GMT", 
#             "x-amzn-requestid": "2ec6c204-7fcb-45bd-8c31-60f9f69aa8cd"
#         }, 
#         "HTTPStatusCode": 200, 
#         "RequestId": "2ec6c204-7fcb-45bd-8c31-60f9f69aa8cd", 
#         "RetryAttempts": 0
#     }
# }
# ```

# ### Cleaning Up the Project
# 
# Rekognition custom label models incur charges while they are running, even if you aren't using them. It's a best practice to stop the model when you are finished using it. In this case you won't use the model again after the lab is finished so you can delete the model and project at once through the Console.
# 
# 1. [Navigate to Amazon Rekognition's project page](https://us-west-2.console.aws.amazon.com/rekognition/custom-labels#/projects)
# 2. Select your project (do not select project version):
# 
# ![Project selection](./assets/project_delete.png) 
# 
# 3. Click "Delete"
# 4. In the "First time set up" dialog that appears, enter *delete* and click "Delete associated models" to confirm you want to delete the model and project together:
# 
# ![Project selection](./assets/confirm_delete.png) 
