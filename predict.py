# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 21:03:21 2019
@author: jrdelmar
Description:
"""
import argparse
import os

from pyimagesearch.loader import Loader
from pyimagesearch.utils import log, get_timestamp, get_output_directory


def predict():
    # --- argument list --- #
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image_path", required=True,
                    help="path to the input image or image directory")
    ap.add_argument("-model", "--model", type=str, default="inception",
                    choices=['inception', 'vgg16', 'xception', 'resnet'],
                    help="name of pre-trained network to use(not implemented)")
    ap.add_argument("-o", "--output_folder", type=str,
                    help="folder name saved in cbis/output/ where prediction files will be saved")
    ap.add_argument('-v', '--verbose', action='store_true',
                    help="Print lots of debugging statements")
    args = vars(ap.parse_args())

    model_list = ["vgg16", "inception", "xception", "resnet"]

    # --- validation --- #
    # ensure a valid model name was supplied via command line argument
    if args["model"] not in model_list:
        raise AssertionError(
            "The --model command line argument should be one from this list [vgg16,inception,xception,resnet].")

    # ensure that the path is write-able or exists
    if not os.path.isdir(args["image_path"]) | os.path.isfile(args["image_path"]):
        raise AssertionError("The --image_path command line argument should exist and should be write-able.")

    model = args["model"]
    img_path = args["image_path"]
    folder_out = args["output_folder"]
    verbose = False
    if args["verbose"]:
        verbose = True

    always_verbose = True
    # show argument list
    s = "[INFO] Argument List:\n" + "\n".join([("-->{}: {}".format(x, args[x])) for x in args])
    log(s, always_verbose)  # always display

    log("[INFO] Starting to load and index the path {} ...".format(img_path), always_verbose)
    index_path = os.path.dirname(__file__)

    # define the folder name
    ts = get_timestamp()
    output_dir = get_output_directory(index_path, ts, img_path, folder_out)

    # load the model and index the results
    loader = Loader(index_path=index_path,
                    output=output_dir,
                    timestamp=ts,
                    verbose=verbose)

    loader.load(image_path=img_path,
                model=model)

    loader.process()
    loader.save_predictions()

    log("[INFO] Completed Loading and Indexing of Results", always_verbose)


# One reason for doing this is that sometimes you write a module (a .py file)
# where it can be executed directly. Alternatively, it can also be imported and
# used in another module. By doing the main check, you can have that code only
# execute when you want to run the module as a program and not have it execute
# when someone just wants to import your module and call your functions themselves.
# ref: https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == '__main__':
    predict()
