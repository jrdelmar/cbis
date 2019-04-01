"""
Created on Wed Feb 20 16:17:33 2019
@author: user
Description:
"""
import os
import re
import pandas as pd
from datetime import datetime
from pyimagesearch.utils import clean_filename, log
import random


def _parse_for_report(df, verbose, top_k=20, threshold=None, ascending=False):
    content = {}
    for idx, row in df.iterrows():
        if row[2].find("[0, '---', 0]") == -1:

            for p in range(2, top_k + 2):  # columns start from 2 onwards
                pred_arr = eval(row[p])
                # check probabilities and threshold
                addMe = False
                if threshold and pred_arr[2] >= threshold:
                    addMe = True
                if not threshold:
                    addMe = True

                # add the label
                if addMe:
                    label = pred_arr[1]
                    if label in content.keys():
                        content[label] = content[label] + 1
                    else:
                        content[label] = 1

        else:
            content['Unprocessed'] = +  1

    return content


def parse_for_report(df, verbose, top_k=20, threshold=None, ascending=False):
    content = _parse_for_report(df, verbose, top_k, threshold, ascending)

    results = pd.DataFrame(list(content.items()), columns=['label', 'count'])
    results = results.sort_values(['count'], ascending=ascending)

    if verbose:
        log("[INFO] Top-20 labels sorted in descending order (highest first)", verbose)
        log(results.head(20), verbose)

    return results


def parse_for_report_graph(df, verbose, top_k=20, threshold=None, ascending=False):
    content = _parse_for_report(df, verbose, top_k, threshold, ascending)

    # content is incompatible with graph, so change it
    # {
    # "Afghan_hound": 4,
    # "African_chameleon": 2,
    # "African_crocodile": 5..
    # expected
    # {
    #  "label": "Afghan_hound",
    #  "count": "4"
    # },
    # {
    #  "label": "African_chameleon",
    #  "count": "2",
    # },
    _list = []
    for x in list(content.keys()):
        _list.append({'label': x, 'value': content[x]})

    return _list


def get_random_from_list(arr):
    sample_size = int(len(arr) * 0.50)
    if sample_size > 50:
        sample_size = 50

    return random.sample(arr, sample_size)


def get_random_images(df):
    # read the csv file and get the image list
    # df = parse(pred_file)
    img_list = []
    for idx, row in df.iterrows():
        if row[2].find("[0, '---', 0]") == -1:
            # strip for display
            img_list.append(clean_filename(row[1], 'dataset'))

    # sample_size = int( len(img_list) * 0.80 )
    # if sample_size > 50:
    #     sample_size = 50
    #
    # img_list_rand = random.sample(img_list, sample_size)

    return get_random_from_list(img_list)
