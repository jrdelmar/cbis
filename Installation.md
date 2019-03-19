
<!-- HEADER -->
<hr style="border-top: 3px solid #1a082a;margin:0em" />
<div style="width:100%;background-color:#;">
<div style="display:table;width:100%">
    <img src="static/img/logo_sm1.png" style="margin:10px;float:left" /> 
    <span style="text-align:center;display:table-cell;vertical-align:top">
        <h1 style="color:#a03377">Content-Based Image Search</h1>
        <h2 style="color:#a03377">Using Pre-trained Models in Machine Learning as a Digital Forensic Tool</h2>
        <h5 style="color:#e54d86">InceptionV3 | ImageNet | Tensorflow | Keras | Python3</h5>
    </span>
</div><span style="color:#a03377;padding-left:10px">@jrdelmar(2019)</span></div>
<hr style="border-top: 3px solid #1a082a;margin:0em" />

# Installation Notes

## Pre-requisites

The user is expected to know how to install and troubleshoot python-related installations. 
A Virtualbox file is provided a semblance of a ready-to-use application. Skip the installation steps if you prefer the Ubuntu Vbox file.

* [python 3](https://www.python.org/downloads/)
* [anaconda](https://www.anaconda.com/distribution/#linux)
* source code in [github](https://github.com/jrdelmar/cbis.git):  `git clone https://github.com/jrdelmar/cbis.git`
* Ubuntu Virtualbox - The Ubuntu pre-built .ova file can be downloaded from one-drive. The file is too large to be uploaded into github-lfts. Get the ova file [here](http://bit.ly/2HFXnkv)
* [virtual environment](https://virtualenv.pypa.io/en/latest/) - Optional

### Python 3
This project uses python 3.X, developed under 3.6.X. Install Python 3 in your development by following the official documentation.

### Anaconda
Anaconda is a package management and deployment environment. Installation via Anaconda is by far the simplest because cartopy, the module used to create offline maps has the simplest installation in the conda environment. 

#### _Cartopy_
Pip is another popular option for installing python packages from the python package index. You can also opt to install pip to install dependencies to run the console. However, the _cartopy_ module used for the offline map is a little painful to install outside of the Anaconda environment. See some of the issues [here](https://www.pythonanywhere.com/forums/topic/9366/) (You had been warned, haha). The recommended installation is through [conda](https://scitools.org.uk/cartopy/docs/v0.15/installing.html)

### Virtual environment - Optional
virtualenv is a module used by the python community to isolate python environments. This is beneficial for a variety of reasons:
* allows installation of packages without affecting the global/system site-packages
* allows downgrade/upgrade of packages and modules to evaluate the application

Completely (hopefully) isolating python environments allows us to create a complete copy of our Python program that works with the dependencies installed.

Reference: https://virtualenv.pypa.io/en/latest/

---
_This section discusses a fresh installation from an Ubuntu box in Virtualbox._


## Install with Ubuntu 18.04.1 LTS Fresh (VirtualBox)
Reference: https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/

Make sure system is updated
`sudo apt-get update`
`sudo apt-get upgrade`

Install PIP because Ubuntu is already shipped with Python 3.6
`sudo apt-get install python-pip`
`sudo apt-get install python3-pip`

Build essentials/developer tools `sudo apt-get install build-essential libssl-dev libffi-dev python-dev`

To solve issues with wheel: `sudo -H pip3 install setuptools --upgrade`

Install the Virtualbox extensions (optional) to allow sharing between host and guest machines such as copy-paste and shared mounted drive. To mount, you can follow this [guide](https://www.smarthomebeginner.com/mount-virtualbox-shared-folder-on-ubuntu-linux/).


### _Optional_
Install virtualenvironment `sudo apt-get install -y python3-venv`

Create virtualenvironment `python3 -m venv cbis`

Activate virtual environment (directory /home/cbis/cbis)
```
cbis@cbis-Virtualbox:~$ source ~/cbis/bin/activate
(cbis) cbis@cbis-Virtualbox:/venv$ which python3
/home/cbis/cbis/bin/python3
(cbis) cbis@cbis-Virtualbox:~$
```

To deactivate:
`deactivate`


## Download the Source code

Download the source code from github `git clone https://github.com/jrdelmar/cbis.git`

```
cbis@cbis-VirtualBox:~/app$ git clone https://github.com/jrdelmar/cbis.git
Cloning into 'cbis'...
remote: Enumerating objects: 404, done.
remote: Counting objects: 100% (404/404), done.
remote: Compressing objects: 100% (294/294), done.
```

Let's install using the Anaconda environment.

## Installation via Anaconda

### Download
To install, choose the correct architecture (use Anaconda3 for Python3) and download the anaconda installation from the repository: https://repo.anaconda.com/archive/
```
(base) cbis@cbis-VirtualBox:~$ wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
--2019-03-18 15:56:52--  https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.131.3, 104.16.130.3, 2606:4700::6810:8203, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.131.3|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 684237703 (653M) [application/x-sh]
Saving to: ‘Anaconda3-2018.12-Linux-x86_64.sh’

Anaconda3-2018.12-Linu 100%[==========================>] 652.54M  2.14MB/s    in 10m 1s  

2019-03-18 16:06:54 (1.08 MB/s) - ‘Anaconda3-2018.12-Linux-x86_64.sh’ saved [684237703/684237703]
```

### Verify
Compare the installation to ensure integrity of the file. Check the md5 hash against the published hash from the repository.
```
(base) cbis@cbis-VirtualBox:~$ md5sum Anaconda3-2018.12-Linux-x86_64.sh 
c9af603d89656bc89680889ef1f92623  Anaconda3-2018.12-Linux-x86_64.sh
```

### Run 
Run the bash file to proceed with the installation package.
```
bash Anaconda3-2018.12-Linux-x86_64.sh 
```

The output will be something like this:
```
Welcome to Anaconda3 2018.12

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>> 
```

When the installation completes, add the installation to the PATH file. Type `yes` so we can use the `conda` command.

```
installation finished.
Do you wish the installer to initialize Anaconda3
in your /home/cbis/.bashrc ? [yes|no]
[no] >>> 
```

### Activate
Activate the installation and the virtual environment by running `source ~/.bashrc`.

### Load Dependencies
Let's install the dependencies using conda install from the requirements file found in github. 
From the terminal, install each dependencies using conda install command. 
`while read requirement; do conda install --yes $requirement; done < requirements.txt`

Reference: https://www.technologyscout.net/2017/11/how-to-install-dependencies-from-a-requirements-txt-file-with-conda/

_Now, let's try to check if the installation works._

## Run the Code

Test with running the python code: (no trailing `/` for the paths) 

From the cbis/ directory:

`python3 predict.py -i dataset/sample -v`

**Predict**

`python3 predict.py -i dataset/sample -v`

```
cbis@cbis-VirtualBox:~/app/cbis$ python3 predict.py -i dataset/sample -v
Using TensorFlow backend.
[INFO] Argument List:
-->image_path: dataset/sample
-->model: inception
-->output_folder: None
-->verbose: True
[INFO] Starting to load and index the path dataset/sample ...
[INFO] inception model used.
[INFO] Weight models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5 used
[INFO] Analyzing directory dataset/sample...
[INFO] Number of files found for analysis: 53
[INFO] Model and weights loaded...
[INFO] Classifying image pictures%2Fgun%2Fgun1(1).jpg
1. revolver: 77.64%
2. holster: 8.81%
3. rifle: 4.35%
4. assault_rifle: 2.87%
...
[INFO] Extract exif information for dataset/sample/facebook(1).jpg..
[INFO] File created/saved: output/sample_20190318_171951/predictions_20190318_171951.csv
[INFO] File created/saved: output/sample_20190318_171951/exif_20190318_171951.csv
[INFO] Completed Loading and Indexing of Results
cbis@cbis-VirtualBox:~/app/cbis$
```

**Search**

`python3 search.py --prediction "output/sample_20190318_171951/predictions_20190318_171951.csv" --exif "output/sample_20190318_171951/exif_20190318_171951.csv" -v`


```
cbis@cbis-VirtualBox:~/app/cbis$ python3 search.py --prediction "output/sample_20190318_171951/predictions_20190318_171951.csv" --exif "output/sample_20190318_171951/exif_20190318_171951.csv" -v
[INFO] Argument List:
-->prediction_file: output/sample_20190318_171951/predictions_20190318_171951.csv
-->exif_file: output/sample_20190318_171951/exif_20190318_171951.csv
-->search_list: gun
-->verbose: True
-->top_k: 20
-->threshold: None
[INFO] Starting to load prediction file output/sample_20190318_171951/predictions_20190318_171951.csv and exif file output/sample_20190318_171951/exif_20190318_171951.csv ...
[INFO] Start parsing prediction file output/sample_20190318_171951/predictions_20190318_171951.csv
	dataset/sample/pictures%2Fgun%2Fgun1(1).jpg | revolver | 77.64%
	dataset/sample/pictures%2Fgun%2Fgun3.jpg | revolver | 60.09%
	dataset/sample/gun2.jpg | revolver | 91.55%
	dataset/sample/pictures%2Fgun%2Fgun2(1).jpg | revolver | 91.55%
	dataset/sample/gun1.jpg | revolver | 77.64%
	dataset/sample/gun2(1).jpg | revolver | 91.55%
	dataset/sample/pictures%2Fgun%2Fgun3(1).jpg | revolver | 60.09%
	dataset/sample/gun3.jpg | revolver | 60.09%
	dataset/sample/pictures%2Fgun%2Fgun1.jpg | revolver | 77.64%
	dataset/sample/pictures%2Fgun%2Fgun2.jpg | revolver | 91.55%
[INFO] Total images found: 10
[INFO] Parse exif from output/sample_20190318_171951/exif_20190318_171951.csv..
[INFO] Total exif information: 10
[INFO] Completed Search 
cbis@cbis-VirtualBox:~/app/cbis$
```

**Report**

`python3 report.py --prediction  "output/sample_20190318_171951/predictions_20190318_171951.csv" -v  -k 20 -t 0.50`

```
cbis@cbis-VirtualBox:~/app/cbis$ python3 report.py --prediction  "output/sample_20190318_171951/predictions_20190318_171951.csv" -v  -k 20 -t 0.50
[INFO] Argument List:
-->prediction_file: output/sample_20190318_171951/predictions_20190318_171951.csv
-->verbose: True
-->top_k: 20
-->threshold: 0.5
[INFO] Parsing file output/sample_20190318_171951/predictions_20190318_171951.csv for report
[INFO] File created/saved: summary_predictions
[INFO] Total labels:7
[INFO] Completed Report
```

---
# The Application

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


---
# The Application (Console)

The application needed for the console is structured this way:
```
root
 |---cbis/
       |---models/        
               |--- contains the model weights pre-trained in imagenet         
       |---pyimagesearch/ 
               |--- contains the classes
       |---output/       
               |--- contains the output files 
       |---predict.py
       |---search.py       
       |---report.py  
       |---requirements.txt # pip installation requirements
```

## 1) Running the console application

_This section discusses how to run the python script from the command line_

### Step 1.1 Load and Predict
This module traverses the directory of images, loads the pretrained machine learning model and predicts the top-20 labels as an output. The output is stored as a csv file under the /output directory

predict.py
Parameters: 
* `-i [Location of Image Path]` _required, location of images, folder directories will be traversed_
* `-o [Location of Output Path]` _optional, location of prediction and exif files (default: APPLICATION_PATH/output/_
* `-v` _verbose flag_

Example:
`python predict.py --image [IMAGE PATH LOCATION] -v`

### Step 1.2 Parse and Search
After the directory has been indexed, search for guns or objects by parsing the csv files and the exif data. Returns the top-k predictions based on a certain threshold (probability values). Default is search for guns with top-20 predictions and no threshold value (return everything).


search.py
Parameters: 
* `--prediction [Location of Prediction File Path]` _location of images, folder directories will be traversed_
* `--exif [Location of Exif File Path]` _location of images, folder directories will be traversed_
* `--search` _search values, delimited by comma, default is search for guns_
* `-k` _top k values, default is 20_
* `-t` _threshold value_
* `-v` _verbose flag_

Example: 
* search for guns and return top 5 results with probabilities higher than or equal to 85%

`python D:\APP\cbis\search.py --prediction  "output\\predictions.csv" --exif "output\\exif.csv" -v  -k 5 -t 0.85`

* search for images with the words: _guns, water, and scuba_ in the predictions and return top 10 results with probabilities higher than or equal to 85%

`python D:\APP\cbis\search.py --prediction  "output\\predictions.csv" --exif "output\\exif.csv" -s "gun,water,scuba" -v -k 10 -t 0.85`

### Step 1.3 Report
Summary of predictions, gives the results in labels and the count of images with that labels

report.py Parameters

* `--prediction [Location of Prediction File Path]` _location of images, folder directories will be traversed_
* `-k` _top k values, default is 20_
* `-t` _threshold value_
* `-v` _verbose flag_

Example: `python D:\APP\cbis\report.py --prediction  'D:\\APP\\cbis\\output\\predictions.csv' -v`

Filename: e.g. summary_predictions_20190226_124946.csv

label | count | 
--- | --- | ---
lakeside |	31
web_site |	28
altar |	23
palace |	23
assault_rifle |	11
sandbar |	9
vault |	9
revolver |	9
castle |	8
packet |	8




---
# The Application (Web via Flask)

The application structure is explained below:
```
root
 |---cbis/
       |---dataset/ 
               |--- contains the images for searching  
       |---maps/ 
               |--- contains the maps when the GPS coordinates are found

       |---models/                         -> contains the model weights pre-trained in imagenet   
            |---imagenet_class_index.json
            |---inception_v3_weights_tf_dim_ordering_tf_kernels.h5
            |---resnet50_weights_tf_dim_ordering_tf_kernels.h5
            |---vgg16_weights_tf_dim_ordering_tf_kernels.h5
            |---xception_weights_tf_dim_ordering_tf_kernels.h5

       |---pyimagesearch/
            |---loader.py
            |---searcher.py
            |---exif.py
            |---utils.py

        |---static/       
               |--- contains the css, javascript image files for rendering the website
        
        |---templates/       
               |--- contains the html files      
        
        |---output/          # contains the output files 
               |---predictions.csv         -> contains the output predictions for each image 
               |---exif.csv                -> contains the exif data for each processed image
               |---summary_predictions.csv -> contains the predicted labels and the count 
               |---unprocessed.csv         -> contains the files that were not processed           
        |---app.py                  # flask application         
        |---predict.py
        |---search.py       
        |---report.py  
        |---report.py  
        |---requirements.txt   # pip installation requirements
```


## 2) Running the Flask-powered web application

_This section discusses how to run the parser and visual tool from the web_


References:
* https://www.pyimagesearch.com/2014/12/08/adding-web-interface-image-search-engine-flask/
* https://pythonspot.com/flask-web-app-with-python/
* https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html

Run the web application using this command from the terminal and from the virtual environment:
`source ~/.bashrc`

Run the application directly from the cbis/ directory
cd
```
(base) cbis@cbis-VirtualBox:~/$ cd /home/cbis/app/cbis
(base) cbis@cbis-VirtualBox:~/app/cbis$ python3 app.py
```


To run in debug mode:

* Unix: 
```
export FLASK_DEBUG=1
python3 app.py```

* Windows: 
```
set FLASK_DEBUG=1
python3 app.py```

Output should show the following:
```
(base) cbis@cbis-VirtualBox:~/app/cbis$ python3 app.py 
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 119-505-411
127.0.0.1 - - [18/Mar/2019 20:41:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 20:41:30] "GET /load HTTP/1.1" 200 -
```

Open http://localhost:5000 from your favorite web browser. 

---
# Pre-installed Ubuntu Virtualbox 
_This section discusses how to run the ready-to-use version using virtualbox's ova file_

To skip the installation process, this virtualbox image contains pre-installed dependencies needed to run the application. 


## Instructions
* Download the .ova file from the download link (see Pre-requisites)
* Import the .ova file (File -> Import Appliance)
* Run/Start the Virtual Machine

### Credentials
cbis/password123



## The structure
The application needed for the console is structured this way:

```
 /home/cbis/app
             |---cbis/
                   |---dataset/ 
                   |---maps/ 

                   |---models/                         -> contains the model weights pre-trained in imagenet   
                        |---imagenet_class_index.json
                        |---inception_v3_weights_tf_dim_ordering_tf_kernels.h5
                   |---pyimagesearch/                  
                           |--- contains python classes

                   |---static/       
                          |--- contains the css, javascript image files for rendering the website

                   |---templates/       
                          |--- contains the html files      

                   |---output/          # contains the output files 
                          |---predictions.csv         -> contains the output predictions for each image 
                          |---exif.csv                -> contains the exif data for each processed image
                          |---summary_predictions.csv -> contains the predicted labels and the count 
                          |---unprocessed.csv         -> contains the files that were not processed           
                    |---app.py                  # flask application         
                    |---predict.py
                    |---search.py       
                    |---report.py  
                    |---report.py  
                    |---requirements.txt   # pip installation requirements
```

## Update Git
Update the git repository in `/home/cbis/app/cbis` and make sure the code is updated: `git pull`

```
(base) cbis@cbis-VirtualBox:~/app/cbis$ git pull
Updating c343b06..806f6bc
Fast-forward
 requirements.venv.txt   |  94 ++++++++--
 static/README.txt       |   4 +
 static/js/main.js       |   8 +-
 templates/howtouse.html | 554 ++++++++++++++++++++++++++++++++++++++--------------------
 templates/index.html    |   8 +-
 templates/report.html   |   6 +-
 6 files changed, 457 insertions(+), 217 deletions(-)
 create mode 100644 static/README.txt
(base) (cbis) cbis@cbis-VirtualBox:~/app/cbis$
```

## Run the Flask Web Application
Run the flask application: `python3 app.py ` from `home/cbis/app/cbis`
```
(base) cbis@cbis-VirtualBox:~$ cd ~/app/cbis
(base) cbis@cbis-VirtualBox:~/app/cbis$ python3 app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 319-255-407



```




-----
## Instructions:

### Step 1: Load and Index the image directories from the console.
- The images for prediction should reside in `APPLICATION_PATH/cbis/dataset`
- This allows the application to load and identify the top-20 predictions for each and every image in the directory. The filename and path will be displayed. 
- Run the prediction from the console
```python prediction.py --image dataset/FOLDER -v ```
- After the prediction completes (depending on the number of files,it might take a while), the file will be saved in the output directory `APPLICATION_PATH/cbis/output`. 

### Step 2: Open the web application and parse/visualise results 
- Run the flask ``` python app.py ```
- From the browser, open: ```localhost:5000```
- The files are taken from `APPLICATION_PATH/cbis/output`. Choose any of the files and parse the results. 
- Start searching! 

