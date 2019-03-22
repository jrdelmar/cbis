# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 12:45:02 2019
@author: jrdelmar
Description: The loader class performs the following actions:
    1) Loads the inception model
    2) Loads the directory path 
    3) Predicts using the InceptionV3 model
    4) Saves the prediction in csv file
    5) Extracts the EXIF file
    6) Saves the exif data in csv file
"""
# import the necessary packages
from keras.applications import ResNet50
from keras.applications import InceptionV3
from keras.applications import Xception  # TensorFlow ONLY
from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

import numpy as np
import pandas as pd
import os
from pathlib import Path
# from datetime import datetime

from pyimagesearch.exif import extract_exif
from pyimagesearch.utils import log, save, get_filenames_in_csv
from pyimagesearch.utils import is_image, get_key_of_max_value


## References:
# * https://www.pyimagesearch.com/2017/03/20/imagenet-vggnet-resnet-inception-xception-keras/
# * https://gogul09.github.io/software/flower-recognition-deep-learning
# * https://keras.io/applications/
class Loader:
    def __init__(self, index_path, output, timestamp, verbose=False):
        # store the index path
        self.index_path = index_path
        self.output_path = output
        self.verbose = verbose
        self.timestamp = timestamp

        self.model = None
        self.weight = None
        self.image_dir = []

        self.image_list = None

    def _preprocess_data(self, model):

        # this code uses default inception so switch the if-else
        # if we are using the InceptionV3 or Xception networks, then we
        # need to set the input shape to (299x299) [rather than (224x224)]
        # and use a different image processing function
        # if args["model"] in ("inception", "xception"):

        input_shape = (299, 299)
        preprocess = preprocess_input

        # initialize the input image shape (224x224 pixels) along with
        # the pre-processing function (this might need to be changed
        # based on which model we use to classify our image)
        if model not in ("inception", "xception"):
            input_shape = (224, 224)
            preprocess = imagenet_utils.preprocess_input

        return input_shape, preprocess

    def _load_image(self, image_path):
        # load the input image using the Keras helper utility while ensuring
        # the image is resized to `input_shape`, the required input dimensions
        # for the ImageNet pre-trained network
        # log("[INFO] loading and pre-processing image...")
        image = load_img(image_path, target_size=self.input_shape)
        image = img_to_array(image)

        # our input image is now represented as a NumPy array of shape
        # (input_shape[0], input_shape[1], 3) however we need to expand the
        # dimension by making the shape (1, input_shape[0], input_shape[1], 3)
        # so we can pass it through thenetwork
        image = np.expand_dims(image, axis=0)

        # pre-process the image using the appropriate function based on the
        # model that has been loaded (i.e., mean subtraction, scaling, etc.)
        return self.preprocess(image)

    def _load_model(self):

        # load the model - for now use inceptionV3 because testing shows this 
        # model has better performance than ResNet, Xception and VGG16 
        log("[INFO] Model and weights loaded...", self.verbose)

        Network = self.model
        return Network(weights=self.weight)

    # load model
    # load the image path
    def load(self, image_path, model="inception"):

        index_path = self.index_path

        # ----- load model -----
        # define a dictionary that maps model names to their classes
        models = {
            "vgg16": VGG16,
            "inception": InceptionV3,
            "xception": Xception,  # TensorFlow ONLY
            "resnet": ResNet50}

        weights = {
            "vgg16": os.path.join(index_path, 'models', 'vgg16_weights_tf_dim_ordering_tf_kernels.h5'),
            "inception": os.path.join(index_path, 'models', 'inception_v3_weights_tf_dim_ordering_tf_kernels.h5'),
            "xception": os.path.join(index_path, 'models', 'xception_weights_tf_dim_ordering_tf_kernels.h5'),
        # TensorFlow ONLY
            "resnet": os.path.join(index_path, 'models', 'resnet50_weights_tf_dim_ordering_tf_kernels.h5')}

        self.model = models[model]
        self.weight = weights[model]

        self.input_shape, self.preprocess = self._preprocess_data(model)

        log("[INFO] {} model used.".format(model), self.verbose)
        log("[INFO] Weight {} used".format(self.weight), self.verbose)

        # ----- load the image list -----
        img_list = [image_path]  # single image path
        # if(os.path.isdir(image_path)): # directory of images for prediction
        #    img_list = list( map(lambda x : os.path.join(image_path, x) , os.listdir(image_path) ))

        # iterate through everything in the directory including subfolders
        if os.path.isdir(image_path):  # directory of images for prediction
            img_list = []
            pathlist = Path(image_path).glob('**/*')
            for path in pathlist:
                img_list.append(str(path))  # because path is object not string

        self.image_list = img_list

        log("[INFO] Analyzing directory {}...".format(image_path), self.verbose)
        log("[INFO] Number of files found for analysis: {}".format(len(img_list)), self.verbose)

    # predict
    # extract exif information        
    def process(self):

        # process top-20 predictions
        k = 20

        # load the model and its weights
        model = self._load_model()

        img_list = self.image_list

        predictions = [None] * len(img_list)
        exif_list = []
        keys_list = []
        unprocessed = []

        for i, image_path in enumerate(img_list):

            # get filename
            l = os.path.normpath(image_path).split(os.sep)
            img_fname = l[len(l) - 1]

            # save predictions
            # predictions[i] = [img_fname]
            # image full path instead of fname only
            predictions[i] = [image_path]
            try:
                if not is_image(image_path):
                    raise Exception
                else:  # allow only valid images
                    image = self._load_image(image_path)
                    # classify the image
                    log("[INFO] Classifying image {}".format(img_fname), self.verbose)

                    # predict the image
                    preds = model.predict(image)
                    P = imagenet_utils.decode_predictions(preds, top=k)

                    # for unit test
                    self.decoded_predictions = P

                    # save predictions
                    for (j, (imagenetID, label, prob)) in enumerate(P[0]):
                        predictions[i].append([imagenetID, label, prob])
                        # loop over the predictions and display the rank-k predictions +
                        # probabilities to our terminal
                        # print in terminal only, do not log because this is already in predictions file
                        if self.verbose:
                            print("{}. {}: {:.2f}%".format(j + 1, label, prob * 100))

                    # extract the exif information
                    exif_data = extract_exif(image_path, self.verbose)

                    # store exif data per image
                    exif_list.append(exif_data)

                    # needed to know which key has the max columns for the df 
                    keys_list.append(len(exif_data.keys()))
            except:
                # unprocessed, separate into its own file
                unprocessed.append(image_path)
                predictions[i].append([0, "---", 0])
                # error in prediction
                log("[ERROR] Cannot process image {}".format(img_fname), self.verbose)

        # we dont know which key has the most number of columns (exif data)
        # so take the key with the max value and use this as reference
        max_k = get_key_of_max_value(keys_list)

        # # convert to df to be saved
        df1 = pd.DataFrame(predictions)
        df2 = pd.DataFrame(exif_list, columns=exif_list[max_k].keys())
        df3 = pd.DataFrame(unprocessed)
        self.data = [df1, df2, df3]
        # transfered to another method
        # names =  ["predictions", "exif", "unprocessed"]
        #
        # filenames = get_filenames_in_csv(self.output_path, names, self.timestamp)
        #
        # save( data, self.output_path, filenames)

    def save_predictions(self):
        names = ["predictions", "exif", "unprocessed"]
        filenames = get_filenames_in_csv(self.output_path, names, self.timestamp)
        save(self.data, self.output_path, filenames)
