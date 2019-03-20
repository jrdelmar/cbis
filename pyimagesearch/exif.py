# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 00:41:34 2019
@author: jrdelmar
Description: Exif utilities
References:
https://motherboard.vice.com/en_us/article/aekn58/hack-this-extra-image-metadata-using-python
https://stackoverflow.com/questions/21697645/how-to-extract-metadata-from-a-image-using-python
"""
# Reference: 
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from pyimagesearch.utils import log, parse


## Helper Functions ##
def extract_exif(image_path, verbose):
    log("[INFO] Extract exif information for {}..".format(image_path), verbose)

    exif_data = get_exif_data(Image.open(image_path))

    # if exif_data is empty, just add resolution (width and height)
    if len(exif_data) == 0:
        exif_data['ExifImageWidth'], exif_data['ExifImageHeight'] = Image.open(image_path).size
    else:
        lat, lon = get_lat_lon(exif_data)
        exif_data['GPSLatitude'] = lat
        exif_data['GPSLongitude'] = lon

    # image full path instead of fname only
    exif_data['FileName'] = image_path

    return exif_data


def parse_exif(file, image_path_list, verbose):
    log("[INFO] Parse exif from {}..".format(file), verbose)
    exif_data_list = []

    if len(image_path_list) > 0:
        # read/parse the file
        df = parse(file)
        image_dir = [convert_to_compare_path(x) for x in image_path_list]
        ## find the exif of this image path
        for idx, row in df.iterrows():
            if convert_to_compare_path(row.FileName) in image_dir:
                exif_data_list.append(row)

    return exif_data_list


def convert_to_compare_path(path):
    return path.replace("\\", "_").replace("/", "_")


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon
