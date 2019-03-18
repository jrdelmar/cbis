# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 01:43:26 2019
@author: jrdelmar
Description: The searcher class performs the following actions
    1) Parse the prediction file
    2) Search for guns or whatever you like to find
    3) Search results returns the file path 
    4) Find the exif information based on the exif file
    
"""
from pyimagesearch.utils import log, parse, get_filename_from_path
import numpy as np

class Searcher:
    def __init__(self, indexPath, verbose = False):
        # store the index path
        self.indexPath = indexPath
        self.verbose = verbose
        
        self.imagenet_guns = ["revolver","assault_rifle","rifle","muzzle"]  # => see 1_baselining-pre-trained-models

    # Search gun function works by taking the classification from imagenet
    # Based on initial testing, the following are the descriptions of imagenet 
    # for guns: revolver","assault_rifle","rifle","muzzle"
    # muzzle can be the dog's muzzle or a gun's muzzle (false positives)
    # returns predictions and percentages
    def search_gun(self, file, top_k = 20, probability_threshold = 0.50):
        log ("[INFO] Start parsing prediction file {}".format(file), self.verbose)
        
        # read/parse the file
        df = parse(file)
        gun_list = self._search_gun( df, file, 
                                    top_k , probability_threshold )
                        
        return gun_list
        
    def _search_gun(self, df, file, top_k , probability_threshold):
        
        imagenet_guns = self.imagenet_guns
    
        # TODO: ensure the rows are sorted
        gun_list = []
        for idx, row in df.iterrows():
            filename = row[1]
            
            if (isvalid_prediction(row[2])):
                for p in range(2,top_k + 2): #columns start from 2 onwards
                    pred_arr = parse_prediction(row[p])
                
                    foundIt = find_in_list(pred_arr[1], imagenet_guns, 
                                           pred_arr[2], probability_threshold) 
                            
                    if (foundIt):
                        label = "gun"
                        gun_list.append([filename,pred_arr[1], pred_arr[2], label]) 
                        break #take the highest(sorted) prediction from gun list
        return gun_list

    
    # find objects based on multiple search criteria and return with the list
    # use the find command, not necessarily the exact word
    #def search(df,findMeList, top_k = 20, probability_threshold=None):
    def search_list(self, file, findMeList, top_k = 20, probability_threshold = 0.50):
        log ("[INFO] Start parsing prediction file {}".format(file), self.verbose)
        
        # read/parse the file
        df = parse(file)
        
        gun_list = []
        if(is_gun_in_list(findMeList)):
            #if there is a gun in the list, reuse gun search function
            gun_list = self._search_gun( df, file, 
                                    top_k , probability_threshold )
       
        #no-guns
        findMeList = extract_non_gun_items(findMeList)
        img_list = []
        if findMeList: #not empty
            img_list = self._search_list(df, file, findMeList, 
                                top_k, probability_threshold)
        
        return gun_list + img_list


    def _search_list(self, df, file, findMeList, top_k, probability_threshold):
        img_list = []
        for idx, row in df.iterrows():
            filename = row[1]
            
            if (isvalid_prediction(row[2])):
                for p in range(2, top_k + 2): #columns start from 2 onwards
                    
                    pred_arr = parse_prediction(row[p])
                    for findMe in findMeList:
                        
                        foundIt = find_string (pred_arr[1], findMe, 
                                               pred_arr[2], probability_threshold) 
                        
                        if (foundIt):
                            label = findMe
                            img_list.append([filename,pred_arr[1], pred_arr[2], label]) 
                            break
        return img_list
    
    #display all the labels
    def display_predictions(self, file, img_filename):
        log ("[INFO][FLASK] Start parsing prediction file {}".format(file), self.verbose)
        
        # read/parse the file
        df = parse(file)
        top_k = 20
        img_filename = get_filename_from_path (img_filename) 
        
        
        #predictions = []
        labels = []
        probabilities = []
        for idx, row in df.iterrows():
            filename = get_filename_from_path (row[1])
            #print("FILENAME=",filename, " img_filename=", img_filename)
            if (img_filename == filename):
                
                if (isvalid_prediction(row[2])):
                    for p in range(2, top_k + 2): #columns start from 2 onwards
                        pred_arr = parse_prediction(row[p])
                        print(pred_arr[1], pred_arr[2] ) #label and probability
                        labels.append(pred_arr[1])
                        probabilities.append(pred_arr[2])
                            
        #expected: data = [['church','house'],[0.9967,0.8909]];
        return [labels, probabilities]
    
    def display_exif(self, file, img_filename):
        
        # read/parse the file
        df = parse(file)
        img_filename = get_filename_from_path (img_filename) 
        df = df.fillna('')
        row = (df[ df['FileName'].str.contains(img_filename, regex=False) ])
        
        col = []
        values = []
        for i, r in enumerate(row):
            if( row[r].values[0]!="" and r != 'Unnamed: 0' and r != 'MakerNote'):
                v = row[r].values[0]
                if(row[r].dtype == np.int64):
                    v = int(v)
                col.append(r)
                values.append(v)
                #print("col=",r, " val=",v)
                    
        try:
            lat = row['GPSLatitude'].values[0]
            lon = row['GPSLongitude'].values[0]
        except:
            lat = 0
            lon = 0
            
            
        #[col,values],[lat,lon]
        return [col,values], [lat,lon]
    
    
    
    
    
    
    
    
    
    
    
#pred_arr[2]  probability
#pred_arr[1] source_string       
def find_string(source_string, findMe, probability, threshold):
    
    foundIt = False
    if(source_string.find(findMe) >= 0):
        foundIt = False  #verify only when there is no threshold
        if threshold == None:
            foundIt = True
        else: #if there is a threshold, use it
            #if the prediction is higher than/eq to the threshold, add
            #take the highest prediction only
            if(probability >= float(threshold)):
                foundIt = True

    return foundIt

def find_in_list(source_string, findMeList, probability, threshold):
    
    foundIt = False
    if(source_string in findMeList):
        foundIt = False  #verify only when there is no threshold
        if threshold == None:
            foundIt = True
        else: #if there is a threshold, use it
            #if the prediction is higher than/eq to the threshold, add
            #take the highest prediction only
            if(probability >= float(threshold)):
                foundIt = True

    return foundIt                    
                    

def extract_non_gun_items(a):
    return [k for k in a if 'gun' not in k and 'guns' not in k]

def is_gun_in_list(a):
    is_gun = False
    for x in a:
        if x in ['gun','guns']:
            is_gun = True
            break
    
    return is_gun

##TODO: Security breach
def parse_prediction(pred):
     pred_arr = eval(pred)
     return pred_arr
 
    
def isvalid_prediction(row):
    is_valid = False
    if (row.find("[0, '---', 0]") == -1):
        is_valid = True
    return is_valid


def validate_search_items(search_list):
    search_list = [item.strip().replace(" ","_").lower() for item in search_list.split(',')]   
    search_list = list(set(filter(None, search_list)))  #removes empty strings, set makes it unique
    
    mode = 0 #none, do not process
    if(len(search_list) == 1 and search_list[0] in ["gun","guns"]):
        mode = 1 #gun
    elif(len(search_list) >= 1):
        mode = 2 #others
    
    return mode, search_list       
    