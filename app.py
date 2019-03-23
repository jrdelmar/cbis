# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:23:58 2019
@author: jrdelmar
Description:
    References: http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
"""
from flask import Flask, render_template
from flask import request, jsonify, send_from_directory

from pyimagesearch.utils import get_filename_from_path, clean_filename
from pyimagesearch.searcher import Searcher, validate_search_items, search_exif_from_list
from pyimagesearch.map import create_map
from pyimagesearch.utils import log, parse, get_foldername_from_path
from pyimagesearch.report import parse_for_report_graph, get_random_images
from pyimagesearch.report import get_random_from_list
from pyimagesearch.heatmap import parse_dir
from pyimagesearch.config import *

import operator
from functools import reduce
from PIL import Image
import json

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route('/dataset/<path:filename>')
def display_image(filename):
    return send_from_directory(DATASET_FOLDER, filename, as_attachment=True)


@app.route('/maps/<path:filename>')
def display_map(filename):
    return send_from_directory(MAPS_FOLDER, filename, as_attachment=True)


@app.route("/load")
def load():
    # structure
    # files = {
    #    'foldername':{
    #        'predictions' = [],
    #        'exif'=[]
    #    }
    # }

    if request.method == "GET":
        files = {}
        # list the directory
        # -----------------------
        dir_contents = os.listdir(OUTPUT_FOLDER)
        for d in dir_contents:
            _content = os.path.join(OUTPUT_FOLDER, d)
            l = os.path.normpath(_content).split(os.sep)
            folder_name = l[len(l) - 1]
            if os.path.isdir(_content):  # if directory then find files

                for f in os.listdir(_content):
                    p, e = allowed_file(f)
                    files = find_files(files, folder_name, f, p, e)

            else:  # file
                p, e = allowed_file(folder_name)
                files = find_files(files, "-", folder_name, p, e)

        results = {"results": files}
        return jsonify(results)


@app.route('/display', methods=['POST'])
def display():
    # retrieves information per image
    if request.method == "POST":

        verbose = True
        # threshold = None
        # top_k = 20

        # get url
        img_src = request.form.get('img')
        pred_file = request.form.get('pred_file')
        exif_file = request.form.get('exif_file')

        # search for the predictions..
        pred_file = os.path.join(INDEX_PATH, pred_file)
        exif_file = os.path.join(INDEX_PATH, exif_file)

        # print('pred_file',pred_file)
        # print('exif_file',exif_file)

        s = Searcher(INDEX_PATH, verbose)
        predictions = s.display_predictions(pred_file, img_src)

        exif_info, gps_info = s.display_exif(exif_file, img_src)

        # print(gps_info[0], gps_info[1])
        lat = gps_info[0]
        lon = gps_info[1]
        map_path = ""

        # create only when there is something to generate
        if is_valid_gps(lat, lon):

            fname = get_filename_from_path(exif_file).split(".")[0]
            fname = fname + "_" + get_filename_from_path(img_src).split(".")[0]

            folder = get_foldername_from_path(pred_file)

            map_path = os.path.join(MAPS_FOLDER, folder, fname + '.png')
            # if the folder doesnt exist, create the folder
            if not os.path.exists(os.path.join(MAPS_FOLDER, folder)):
                os.makedirs(os.path.join(MAPS_FOLDER, folder))

            # create a map only when the file doesnt exist
            if not (os.path.isfile(map_path)):
                # generate map
                create_map(img_src, map_path, lat, lon)

            #change to relative directory when returning to screen
            map_path = os.path.join(MAPS_RELATIVE_FOLDER, folder, fname + '.png')

        # print("map_path=",map_path)
        results = {"predictions": predictions,
                   "exif_info": exif_info,
                   "map_path": map_path ,
                   "gps_coordinates": [lat, lon]}

        return jsonify(results)


@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":

        verbose = True
        threshold = None
        top_k = 20

        # get the argument list
        json = request.get_json()
        search_list = json['search_list']
        search_exif = json['search_exif']

        image_list = []
        image_path_list = []
        result_list = {'predictions': [], 'exif': []}

        # TODO: validation check
        # for each row of prediction and exif file
        for j in json['files']:
            # folder location

            pred_file = ""
            exif_file = ""

            # TODO: if there are multiple files
            path = OUTPUT_FOLDER
            if j != "-":
                path = os.path.join(OUTPUT_FOLDER, j)

            pred_file = json['files'][j]['predictions'][0]
            exif_file = json['files'][j]['exif'][0]

            # prediction files
            pred_file = os.path.join(path, pred_file)
            exif_file = os.path.join(path, exif_file)

            # image_path_list, image_list
            a, b = search_predictions(pred_file, exif_file,
                                      search_list, search_exif,  top_k, threshold)

            image_path_list.append(a)
            image_list.append(b)

            _a = list(map(lambda x: clean_filename(x, 'dataset'), a))
            result_list['predictions'].append({pred_file: _a})
            result_list['exif'].append({exif_file: _a})

        image_path_list = reduce(operator.concat, image_path_list)
        image_list = reduce(operator.concat, image_list)

        # TODO: if no results
        # change the directory to display on screen
        # sort by probability
        image_list_new = []
        if len(image_list) > 0:

            for img in image_list:
                # idx = img[0].find("dataset") #find the first instance of 'dataset' folder
                fname = clean_filename(img[0], 'dataset')
                # get the filename resolution
                # print(os.path.abspath(img[0]))
                w, h = Image.open(img[0]).size
                icon_size = ""
                if w * h > 30000:
                    icon_size = "-2x"
                # 0: filename, 1:search label, 2:search probability, 3:icon size
                # 4:prediction file used, 5: exif file used
                image_list_new.append([fname, img[1], img[2], img[3],
                                       icon_size])

            # sort by highest probabilities
            image_list_new.sort(key=lambda k: (-k[2]))

        # print("result_list=>", result_list)

        # return list of images and label predictions first
        results = {"results": image_list_new, "result_list": result_list}
        return jsonify(results)
        # return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
        # return jsonify({"results": request.form.get('img')})


# @app.route("/report_data1")
# def report_data1():
#    return jsonify(get_report_data())

# get the list of imagenet classes
@app.route("/imagenet", methods=['GET'])
def imagenet():
    # get the class list
    imagenet_classes = []
    print(IMAGENET_LIST_CLASSES_JSON)
    with open(IMAGENET_LIST_CLASSES_JSON) as j:
        data = json.load(j)

    for d in data:
        # print(data[d][1])
        imagenet_classes.append(data[d][1])

    return jsonify(sorted(imagenet_classes))


# visualise all files
@app.route("/visualise", methods=['GET', 'POST'])
def visualise():
    threshold = None
    top_k = 20
    if request.method == "POST":  # not working
        # get the argument list
        json = request.get_json()
        pred_file_list = json['prediction_files']

        if json['top_k']:
            top_k = json['top_k']

        # re-create the path
        arr = []
        for f in pred_file_list:
            l = [os.path.join(OUTPUT_FOLDER, f, x) for x in pred_file_list[f]['predictions']]
            arr.append(l)
        path_list = [i[0] for i in arr]

    if request.method == "GET":
        # get the argument list
        pfiles = request.args.get('pfiles').split(",")
        folders = request.args.get('folders').split(",")

        path_list = [os.path.join(OUTPUT_FOLDER, f, pfiles[i]) for i, f in enumerate(folders)]

        if request.args.get('k'):
            top_k = int(request.args.get('k'))

    # DEBUG
    # pred_file = "output/WEAPON-DB11_20190226_180745/predictions_.csv" #args["prediction_file"]
    # pred_file = path_list[0]

    verbose = False
    always_verbose = True

    dataset = []
    img_list_rand = []
    for pred_file in path_list:
        log("[INFO] Parsing file {} for report".format(pred_file), always_verbose)
        # read/parse the file
        df = parse(pred_file)
        results = parse_for_report_graph(df, verbose, top_k, threshold)
        img_list_rand.append(get_random_images(parse(pred_file)))
        # dataset.append( { 'folder': get_foldername_from_path(pred_file),
        #                 'file': get_filename_from_path(pred_file),
        #                 'dataset': {'children': results} })
        dataset.append(results)

    # random images
    image_list = reduce(operator.concat, img_list_rand)
    image_list = get_random_from_list(image_list)

    # summarise all
    labels = []
    values = []
    categories = []
    imagenet_guns = ["revolver", "assault_rifle", "rifle", "muzzle"]
    for x in dataset:
        for y in x:
            if y['label'] in labels:
                idx = labels.index(y['label'])
                values[idx] = int(values[idx]) + int(y['value'])
            else:
                labels.append(y['label'])
                values.append(y['value'])
                if y['label'] in imagenet_guns:
                    categories.append("gun")
                else:
                    categories.append("not_gun")

    ds = []
    for i, label in enumerate(labels):
        ds.append({'label': label,
                   'value': values[i],
                   'category': categories[i]})

    results = {'children': ds, 'random_images': image_list}  # display this by wrapping in jsonify

    return jsonify(results)


"""
@app.route("/report_data", methods=['GET'])
def report_data():
    
    verbose = False
    threshold = None
    top_k = 20 
    if (request.args.get('k')):
        top_k = int(request.args.get('k'))
    
    #DEBUG
    pred_file = "output/WEAPON-DB11_20190226_180745/predictions_.csv" #args["prediction_file"]
    verbose = False
    always_verbose = True
    
    log("[INFO] Parsing file {} for report".format(pred_file), always_verbose)
    # read/parse the file
    df = parse(pred_file)
    results = parse_for_report_graph(df, verbose, top_k, threshold)
    
    results ={'children': results}

    return jsonify(results)
"""


@app.route("/heatmap", methods=['GET'])
def heatmap():
    arr_folders, arr_images, arr_values = parse_dir()
    # d = {'x': arr_folders, 'y': arr_images, 'value': arr_values}
    children = []

    for i, f in enumerate(arr_folders):
        children.append({'x': f, 'y': arr_images[i], 'value': arr_values[i]})

    return jsonify({'children': children})


def is_valid_gps(lat, lon):
    valid = True
    if lat == 0 and lon == 0:
        valid = False
    elif lat == "" or lon == "":
        valid = False
    return valid


# TODO: not enough
def allowed_file(f):
    predictions = False
    exif = False
    if f[:12] == ALLOWED_FILENAMES[0]:  # predictions_
        predictions = True
    elif f[:5] == ALLOWED_FILENAMES[1]:  # exif_
        exif = True

    return predictions, exif


def find_files(files, folder_name, f, p, e):
    if p or e:
        if folder_name not in files.keys():  # initialise if not found
            files[folder_name] = {'predictions': [], 'exif': []}

        if p:
            files[folder_name]['predictions'].append(f)
        if e:
            files[folder_name]['exif'].append(f)
    return files


def search_predictions(pred_file, exif_file, search_list, search_exif, top_k, threshold):
    verbose = True
    always_verbose = True

    log("[INFO][FLASK] Starting to load prediction file {} and exif file {} ...".format(pred_file, exif_file),
        always_verbose)
    s = Searcher(INDEX_PATH, verbose)
    _image_list = []
    _image_path_list = []

    mode, search_list = validate_search_items(search_list)
    # print("pred_file=", pred_file)
    # print("file size=", os.path.getsize(pred_file))

    ## --------------- prediction --------------- ##
    if 1 == mode:  # guns
        _image_list = s.search_gun(pred_file, top_k, threshold)

    elif (2 == mode):  # others
        _image_list = s.search_list(pred_file, search_list, top_k, threshold)

    else:
        print("[INFO][FLASK] Dont waste my time, nothing to search so no results found")

    if len(_image_list) > 0:
        _image_path_list = list(map(lambda x: x[0], _image_list))
        if verbose:
            for img in _image_list:
                log("\t{} | {} | {:.2f}%".format(img[0], img[1], float(img[2]) * 100), verbose)

    log("[INFO][FLASK] Total images found: {}".format(len(_image_path_list)), always_verbose)

    # if the exif information is found, search for the info
    if search_exif:
        _image_path_list, _image_list = search_exif_from_list(exif_file, search_exif, _image_path_list, _image_list)

    # image_path_list => only images
    # image_list => predictions top based on search items
    return _image_path_list, _image_list



# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
