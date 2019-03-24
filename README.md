# cbis
Content-based Image Search using pre-trained Keras model with Python3 and Flask
---
## Overview
In the field of computer vision research, machine learning has gained significant traction in different industries such as medicine, entertainment, commercial products and services. Similarly, in digital forensics, re-formulation of traditional questions into either a regression or a classification problem are already being studied. The research area of multimedia forensics  has gained solid ground due to the ubiquitous use of multimedia (digital pictures and videos) and hence, potential evidentiary value. 

Since 2016, classifiers that won ImageNet competitions have already exceeded the human-level accuracy. Technology and algorithm development have improved significantly that we see automated classification quite commonly deployed in applications such as Pinterest, Google Photos, Facebook and Amazon. Sadly, in a typical digital forensic analysis, image classification is still manually performed. 

Discussions with forensic analysts in a renowned digital forensics firm revealed that although analysing photos is such an integral part of forensic analysis that almost all digital forensic toolkits have some form of photo analysis functionality, there is no automated way to categorise the images using non-proprietary tools. They lamented the lack of open-source tools that could (1) automate categorisation, as well as (2) provide information that will be relevant in a forensic analysis. 

This tool aims to:
* Perform  a machine-learning based categorisation of images using pre-trained networks from Imagenet
* Provide relevant information such as EXIF
* Usable in a Digital Forensic Investigation


---
The source code can be used from the: 
* console (python3)
* web browser (via python-flask)

The console performs indexing and prediction, search and report.
The web browser performs a more user-friendly parser and a visualisation option. 

_console_
* loads the pretrained keras model. For this project, I use the InceptionV3 model that is pre-trained on the ImageNet dataset. 
* indexes the image directory by performing a prediction per image 
* stores the prediction for each image in a csv file. The _prediction.csv_ file is stored in the output folder
* extracts the exif information for each image and stores that infromation in a csv file. The _exif.csv_ file is stored in the output folder

_web_
* parses the prediction and exif files
* creates a visual representation of the data
