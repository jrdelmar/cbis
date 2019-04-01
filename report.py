# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 15:15:35 2019
@author: user
Description:
    Analyzes the results and provides output list
"""

import argparse

from pyimagesearch.utils import log, parse, save, get_filenames_in_csv, get_timestamp
from pyimagesearch.report import parse_for_report
from pyimagesearch.config import *

def report():
    # --- argument list --- #
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-prediction", "--prediction_file", required=True,
                    help="path to the prediction file to be parsed")
    ap.add_argument('-v', '--verbose', action='store_true',
                    help="Print lots of debugging statements")
    ap.add_argument("-k", "--top_k", type=int, default=20,
                    help="retrieve the top-k predictions, default is 20")
    ap.add_argument("-t", "--threshold", type=float, default=0.50,
                    help="probability threshold value in decimals ex. 0.75, default is 0.50")

    args = vars(ap.parse_args())

    # --- validation --- #
    # ensure that the arguments supplied are pathnames
    if not os.path.isfile(args["prediction_file"]):
        raise AssertionError("The --prediction_file command line argument should exist and should be write-able.")
    verbose = False
    if args["verbose"]:
        verbose = True

    threshold = None
    if args["threshold"]:
        threshold = args["threshold"]

    top_k = 20
    if args["top_k"]:
        top_k = args["top_k"]

    pred_file = args["prediction_file"]
    verbose = False
    if args["verbose"]:
        verbose = True

    always_verbose = True
    # show argument list
    s = "[INFO] Argument List:\n" + "\n".join([("-->{}: {}".format(x, args[x])) for x in args])
    log(s, always_verbose)  # always display

    log("[INFO] Parsing file {} for report".format(pred_file), always_verbose)
    # read/parse the file
    df = parse(pred_file)
    results = parse_for_report(df, verbose, top_k, threshold)

    # save the file 
    # save in the same folder as the prediction file
    output_path = os.path.dirname(os.path.abspath(pred_file))
    filenames = get_filenames_in_csv(output_path, ["summary_predictions"], get_timestamp())

    save([results], output_path, filenames)

    log("[INFO] Total labels:{}".format(len(results['label'])), always_verbose)
    log("[INFO] Completed Report ", always_verbose)


# One reason for doing this is that sometimes you write a module (a .py file) 
# where it can be executed directly. Alternatively, it can also be imported and 
# used in another module. By doing the main check, you can have that code only 
# execute when you want to run the module as a program and not have it execute 
# when someone just wants to import your module and call your functions themselves.
# ref: https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == '__main__':
    report()
