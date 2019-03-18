from pyimagesearch.searcher import Searcher
from pyimagesearch.utils import *
import pytest

indexPath = "D:/APP/cbis/"
verbose = True

#test Search class
@pytest.fixture
def searcher():
    return Searcher(indexPath, verbose)

pred_file =  "D://APP//cbis//tests//out//predictions_test.csv"
top_k = 20

def test_search_gun( searcher ):
    threshold = 0.50
    image_list = searcher.search_gun(pred_file, top_k, threshold)

    assert len(image_list) == 1
    assert image_list[0][3] == 'gun'

def test_search_not_gun(searcher):
    threshold = 0.70
    search_list = ['wooden_spoon']
    image_list = searcher.search_list(pred_file,search_list, top_k, threshold)
    assert len(image_list) == 2
    assert image_list[0][3] == 'wooden_spoon'

def test_search_not_gun1(searcher):
    threshold = 0.80
    search_list = ['wooden_spoon', 'revolver']
    image_list = searcher.search_list(pred_file,search_list, top_k, threshold)
    assert len(image_list) == 1
    assert image_list[0][3] == 'revolver'

def test_search_not_gun2(searcher):
    threshold = 0.70
    search_list = ['wooden_spoon', 'revolver']
    image_list = searcher.search_list(pred_file,search_list, top_k, threshold)
    assert len(image_list) == 3
    assert image_list[0][3] == 'wooden_spoon'
    assert image_list[2][3] == 'revolver'
