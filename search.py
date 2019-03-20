# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 01:33:05 2019
@author: user
Description:
"""
import argparse
import os

from pyimagesearch.utils import log
from pyimagesearch.searcher import Searcher, validate_search_items
from pyimagesearch.exif import parse_exif


# TODO: Unit test

def search():
    # --- argument list --- #
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-prediction", "--prediction_file", required=True,
                    help="path to the prediction file to be parsed")
    ap.add_argument("-exif", "--exif_file", required=True,
                    help="path to the exif file to be parsed")
    # mode to search for guns or just objects
    ap.add_argument("-s", "--search_list", type=str, default="gun",
                    help="list of search items delimited by comma")
    ap.add_argument('-v', '--verbose', action='store_true',
                    help="Print lots of debugging statements")
    ap.add_argument("-k", "--top_k", type=int, default=20,
                    help="retrieve the top-k predictions, default is 20")
    ap.add_argument("-t", "--threshold", type=float,
                    help="probability threshold value in decimals ex. 0.75, default is 0.50")

    args = vars(ap.parse_args())

    # --- validation --- #
    # ensure that the arguments supplied are pathnames
    if not os.path.isfile(args["prediction_file"]):
        raise AssertionError("The --prediction_file command line argument should exist and should be write-able.")

    # ensure that the path is write-able or exists
    if not os.path.isfile(args["exif_file"]):
        raise AssertionError("The --exif_file command line argument should exist and should be write-able.")

    pred_file = args["prediction_file"]
    exif_file = args["exif_file"]
    verbose = False
    if args["verbose"]:
        verbose = True

    threshold = None
    if args["threshold"]:
        threshold = args["threshold"]

    top_k = 20
    if args["top_k"]:
        top_k = args["top_k"]

    always_verbose = True
    # show argument list
    s = "[INFO] Argument List:\n" + "\n".join([("-->{}: {}".format(x, args[x])) for x in args])
    log(s, always_verbose)  # always display

    # TODO - list suggestion from imagenet 1000 classes
    # DEBUG:
    # args["search_list"] = "gun,water,SCUBA diver, van" 
    mode, search_list = validate_search_items(args["search_list"])

    log("[INFO] Starting to load prediction file {} and exif file {} ...".format(pred_file, exif_file), always_verbose)
    index_path = os.path.dirname(__file__)
    s = Searcher(index_path, verbose)
    image_list = []
    image_path_list = []

    ## --------------- prediction --------------- ##
    if 1 == mode:  # guns
        image_list = s.search_gun(pred_file, top_k, threshold)

    elif 2 == mode:  # others
        image_list = s.search_list(pred_file, search_list, top_k, threshold)

    else:
        print("[INFO] Dont waste my time, nothing to search so no results found")

    if len(image_list) > 0:
        image_path_list = list(map(lambda x: x[0], image_list))
        if verbose:
            for img in image_list:
                log("\t{} | {} | {:.2f}%".format(img[0], img[1], float(img[2]) * 100), verbose)

    log("[INFO] Total images found: {}".format(len(image_path_list)), always_verbose)

    ## --------------- exif info --------------- ##
    exif_info = parse_exif(exif_file, image_path_list, verbose)
    log("[INFO] Total exif information: {}".format(len(exif_info)), always_verbose)

    # print("length exif_info=",len(exif_info))
    # print(image_list)
    # TODO: Convert to json results 

    log("[INFO] Completed Search ", always_verbose)


# One reason for doing this is that sometimes you write a module (a .py file) 
# where it can be executed directly. Alternatively, it can also be imported and 
# used in another module. By doing the main check, you can have that code only 
# execute when you want to run the module as a program and not have it execute 
# when someone just wants to import your module and call your functions themselves.
# ref: https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == '__main__':
    search()
