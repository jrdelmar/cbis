from pyimagesearch.loader import Loader
from pyimagesearch.utils import *
import pytest

indexPath = "D:/APP/cbis/"
output_dir = "D:/APP/cbis/tests/out"
ts = get_timestamp()
verbose = True
imagenet_guns = ["revolver","assault_rifle","rifle","muzzle"]
model = 'inception'

#test Loader class
@pytest.fixture
def loader():
    return Loader( indexPath = indexPath,
                    output = output_dir,
                    timestamp = ts,
                    verbose = verbose)

def test_loader_load( loader ):
    img_path = 'D:/APP/cbis/tests/img/'
    loader.load(image_path=img_path,
                model=model)
    assert len(loader.image_list) == 7
    assert loader.weight == "D:/APP/cbis/models\inception_v3_weights_tf_dim_ordering_tf_kernels.h5"


def test_loader_gun_image( loader ):
    img_path = 'D:/APP/cbis/tests/img/sub_folder/gun.jpg'
    loader.load(image_path=img_path,model=model)

    assert len(loader.image_list) == 1
    out_files_count = len(os.listdir(output_dir))
    loader.process()
    loader.save_predictions()

    # test the prediction
    P = loader.decoded_predictions
    is_gun = False
    for (j, (imagenetID, label, prob)) in enumerate(P[0]):
        if label in imagenet_guns:
            assert label == "revolver"
            is_gun = True
            break
    # file should be created
    assert len(os.listdir(output_dir)) == out_files_count + 2
    assert is_gun == True

def test_loader_not_gun_image( loader ):
    img_path = 'D:/APP/cbis/tests/img/sub_folder/not_gun.jpg'
    loader.load(image_path=img_path, model=model)

    assert len(loader.image_list) == 1
    loader.process()

    # test the prediction
    P = loader.decoded_predictions
    not_gun = True
    for (j, (imagenetID, label, prob)) in enumerate(P[0]):
        if label in imagenet_guns:
            not_gun = False
            break

    assert not_gun == True

#run for the search.py

"""
def test_loader_test_image( loader ):
    img_path = 'D:/APP/cbis/tests/img/'
    loader.load(image_path=img_path,model=model)

    assert len(loader.image_list) == 7
    out_files_count = len(os.listdir(output_dir))
    loader.process()
    loader.save_predictions()

    # file should be created
    assert len(os.listdir(output_dir)) == out_files_count + 2
"""