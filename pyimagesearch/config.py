import os
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

print(cfg['folders']['output'])
INDEX_PATH = os.getcwd()

OUTPUT_FOLDER = os.path.join(INDEX_PATH, cfg['folders']['output'])
DATASET_FOLDER = os.path.join(INDEX_PATH, cfg['folders']['dataset'])
MAPS_FOLDER = os.path.join(INDEX_PATH, cfg['folders']['maps'])
MAPS_RELATIVE_FOLDER = cfg['folders']['maps']
ALLOWED_FILENAMES = cfg['files']['allowed_filenames']

IMAGENET_GUNS = cfg['imagenet']['guns']
IMAGENET_LIST_CLASSES_JSON = cfg['imagenet']['list_classes_json']

# ALLOWED_EXTENSIONS = ['csv']
# ALLOWED_FILENAMES = ['predictions_', 'exif_']
# DATASET_FOLDER = os.path.join(INDEX_PATH, "dataset")
# MAPS_FOLDER = os.path.join(INDEX_PATH, "maps")
