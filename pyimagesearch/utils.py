# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 16:17:33 2019
@author: user
Description:
"""
import os
import re
import pandas as pd
from datetime import datetime
import imghdr


def is_image(img_path):
    res = False
    if os.path.isfile(img_path):
        if imghdr.what(img_path) in ['jpg','jpeg','bmp','gif']:
            res = True
    
    return res

# files with timestamp
def get_filenames_in_csv(indexPath, names, ts):
    return list(map(lambda name : os.path.join(indexPath, name + "_" +  ts + ".csv") , names))

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_output_directory(indexPath, ts, img_path, folder_out):
    
    if folder_out == None:
        l = os.path.normpath(img_path).split(os.sep)
        folder_out = l[len(l)-1]
    else:
        folder_out = filter_allowed_characters(folder_out)
   
    return os.path.join(indexPath,"output",folder_out + "_" + ts )   
    

def get_key_of_max_value(l):
    x = [i for (v, i) in sorted(  ((v, i) for (i, v) in enumerate(l)), reverse=True )]
    return x[0]        
 

def log(message, verbose=False):
    if verbose:
        print(message)
        
    write_to_log(message, verbose)
    
    
    
def write_to_log(message, verbose=False):
    
    indexPath = os.path.dirname(__file__) #utils path
    filename = "cbis" + datetime.now().strftime("-%Y%m%d") + ".log"
    filename = os.path.join(indexPath,"..","output",filename)
    #filename = os.path.join(indexPath,"..","output","console",filename) #TODO: debug
    
    with open(filename, 'a') as f:
        if f.tell() == 0:
            msg = "{} [INFO] Log file {} created.\n".format(datetime.now().strftime("%Y-%m-%d %X"), filename)
            f.write(msg)
            if verbose:
                log(msg)
        #else:
        #    print('file existed, appending')
            
        f.write("{} {}".format(datetime.now().strftime("%Y-%m-%d %X"), message + "\n"))
    
#read the file and return df object
def parse(file):
    return pd.read_csv(file,header=0)    


# data should be dataframe, always in verbose mode    
def save(data, outputPath, filenames):
    # files with timestamp
    #create if it doesnt exist
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    for i, df in enumerate(data):
        if len(df) > 0: # only create files when there is a record
            df.to_csv(filenames[i])
            log("[INFO] File created/saved: {}".format(filenames[i]),True)
  
def filter_allowed_characters(s):
    s = s.replace(" ","_")
    return re.sub('[^a-zA-Z0-9_\n\.]', '', s)


def get_filename_from_path(path):
    l = os.path.normpath(path).split(os.sep)
    return l[len(l)-1]
    
def get_foldername_from_path(path):
    l = os.path.normpath(path).split(os.sep)
    return l[len(l)-2]

def clean_filename(file, findMe):
    idx = file.find(findMe) #find the first instance of 'dataset' folder
    return file[idx:]