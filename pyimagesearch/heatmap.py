# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 15:15:35 2019
@author: user
Description:
    Analyzes the results and provides output list
"""
from pyimagesearch.utils import get_filename_from_path, get_timestamp, log
import os
from pathlib import Path
import pandas as pd

#parse the dataset directory folder
#list of extensions supported
#TODO:
EXTENSIONS_SUPPORTED = ['CRDOWNLOAD','ICS','MSI','PART','TORRENT','BAK','TMP','C','CLASS','CPP','CS','DTD','FLA','H','JAVA','LUA','M','PL','PY','SH','SLN','SWIFT','VB','VCXPROJ','XCODEPROJ','BIN','CUE','DMG','ISO','MDF','TOAST','VCD','7Z','CBR','DEB','GZ','PKG','RAR','RPM','SITX','TARGZ','ZIP','ZIPX','HQX','MIM','UUE','CFG','INI','PRF','CAB','CPL','CUR','DESKTHEMEPACK','DLL','DMP','DRV','ICNS','ICO','LNK','SYS','FNT','FON','OTF','TTF','CRX','PLUGIN','ASP','ASPX','CER','CFM','CSR','CSS','DCR','HTM','HTML','JS','JSP','PHP','RSS','XHTML','GPX','KML','KMZ','DWG','DXF','B','DEM','GAM','NES','ROM','SAV','APK','APP','BAT','CGI','COM','EXE','GADGET','JAR','WSF','ACCDB','DB','DBF','MDB','PDB','SQL','XLR','XLS','XLSX','INDD','PCT','PDF','AI','EPS','PS','SVG','BMP','DDS','GIF','HEIC','JPG','PNG','PSD','PSPIMAGE','TGA','THM','TIF','TIFF','YUV','3DM','3DS','MAX','OBJ','3G2','3GP','ASF','AVI','FLV','M4V','MOV','MP4','MPG','RM','SRT','SWF','VOB','WMV','AIF','IFF','M3U','M4A','MID','MP3','MPA','WAV','WMA','CSV','DAT','GED','KEY','KEYCHAIN','PPS','PPT','PPTX','SDF','TAR','TAX2016','TAX2018','VCF','XML','DOC','DOCX','LOG','MSG','ODT','PAGES','RTF','TEX','TXT','WPD','WPS']

def parse_dir():

    DATASET_DIR = "dataset"
    OUTPUT_DIR = "output"
    folders = os.listdir(DATASET_DIR)  # get folders only

    arr = {}
    # read only from the dataset folders
    for f in folders:
        image_path = os.path.join(DATASET_DIR, f)
        if os.path.isdir(image_path):

            arr_ext = {}

            pathlist = Path(image_path).glob('**/*')
            for path in pathlist:
                if os.path.isfile(path):
                    filename, file_extension = os.path.splitext(str(path))
                    ext = file_extension.replace(".", "").lower()
                    if ext == '':
                        ext = 'None'  # some files might not have extensions like some carved images
                    elif ext.upper() not in EXTENSIONS_SUPPORTED:
                        ext = 'Others'
                    if ext in arr_ext:
                        # if the extension already exists in the list, then add
                        arr_ext[ext] = arr_ext[ext] + 1
                    else:  # create
                        arr_ext[ext] = 1

            arr[get_filename_from_path(image_path)] = arr_ext

    arr_folders = []
    arr_images = []
    arr_values = []

    for k in arr:
        for i in arr[k]:
            arr_folders.append(k)
            arr_images.append(i)
            arr_values.append(arr[k].get(i))

    d = {'x': arr_folders, 'y': arr_images, 'value': arr_values}
    df = pd.DataFrame(d)

    ts = get_timestamp()
    heatmap_file = os.path.join(OUTPUT_DIR, "file_extensions_" + ts + ".csv")

    #show displayed file for download
    #df.to_csv(heatmap_file, index=False)
    log("[INFO] File created/saved: {}".format(heatmap_file), True)

    return arr_folders, arr_images, arr_values


if __name__ == '__main__':
    parse_dir()
