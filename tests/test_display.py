from pyimagesearch.loader import Loader
from pyimagesearch.utils import *
from pyimagesearch.report import *
import pytest
import random
indexPath = "D:/APP/cbis/"
output_dir = "D:/APP/cbis/tests/out"
ts = get_timestamp()
verbose = True
imagenet_guns = ["revolver","assault_rifle","rifle","muzzle"]
model = 'inception'
pred_file =  "D://APP//cbis//tests//out//predictions_test.csv"
top_k = 20

def test_show_random_images():
    # #read the csv file and get the image list
    # df = parse(pred_file)
    # img_list = []
    # for idx, row in df.iterrows():
    #     if (row[2].find("[0, '---', 0]") == -1):
    #         print(row[1])
    #         img_list.append(row[1])
    #
    # sample_size = int( len(img_list) * 0.5 )
    # if sample_size > 50:
    #     sample_size = 50
    #
    # img_list_rand = random.sample(img_list, sample_size)
    # print("PRINT=>",img_list_rand[0],img_list_rand[1])
    # print("img_list=>", img_list)
    df = parse(pred_file)
    img_list = get_random_images(df)
    assert len(img_list) == 2 ## there are 4 images in the list, returns 50% sample data, expected 2 items
