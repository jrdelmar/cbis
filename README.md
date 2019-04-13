# cbis
Content-based Image Search using pre-trained Keras model with Python3 and Flask
---
Running demo here: https://cbis.jrdelmar.dev/
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
