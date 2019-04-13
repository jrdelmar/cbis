from pyimagesearch.utils import *


# ------ is_image ------
def test_is_image_ok():
    img_path = "D:/APP/cbis/tests/img/Bangalore.JPG"
    assert is_image(img_path) == True

def test_is_image_imagetxt():
    img_path = "D:/APP/cbis/tests/img/image.txt"
    assert is_image(img_path) == True

def test_is_image_notanimagetxt():
    img_path = "D:/APP/cbis/tests/img/notanimage.txt"
    assert is_image(img_path) == False

def test_is_image_notanimagejpg():
    img_path = "D:/APP/cbis/tests/img/notanimage.jpg"
    assert is_image(img_path) == False

def test_is_image_dir():
    img_path = "D:/APP/cbis/tests/img/"
    assert is_image(img_path) == False

# ------ get_filenames_in_csv ------
indexPath = "D:/APP/cbis/tests/img/"
ts = "20190317_121317"

def test_get_files():
    names = ['test']
    files = get_filenames_in_csv(indexPath, names, ts)
    assert files[0] == "D:/APP/cbis/tests/img/test_20190317_121317.csv"

def test_get_output_folder():
    folder_out = None
    img_path = "D:/APP/cbis/tests/img/"
    folder = get_output_directory(ts, img_path, folder_out)
    assert folder.replace("\\", "/") == "D:/APP/cbis/output/img_20190317_121317".replace("\\", "/")


def test_get_key_max():
    arr = [3, 6,7,0,12,22,100,9,8]
    assert get_key_of_max_value(arr) == 6

