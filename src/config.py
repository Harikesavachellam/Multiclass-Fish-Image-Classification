"""
config.py
---------
All the settings for the whole project live in this one file.

Why a config file?
If you want to change the image size or the number of epochs, you change it
HERE in one place, instead of hunting for it inside five different scripts.
Every other file in this project imports its settings from here.
"""

import os

# ----------------------------------------------------------------------
# 1. FOLDER PATHS
# ----------------------------------------------------------------------

# The folder this file is in  ->  .../multiclass_fish_classification/src
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# One level up  ->  .../multiclass_fish_classification
PROJECT_DIR = os.path.dirname(SRC_DIR)

# Where the fish images live (train / val / test folders go inside this)
DATA_DIR = os.path.join(PROJECT_DIR, "data")

TRAIN_DIR = os.path.join(DATA_DIR, "train")  # images used to teach the model
VAL_DIR = os.path.join(DATA_DIR, "val")      # images used to check it while training
TEST_DIR = os.path.join(DATA_DIR, "test")    # images used for the final exam

# Where trained models (.h5 files) are saved
MODELS_DIR = os.path.join(PROJECT_DIR, "models")

# Where pictures (graphs) and reports are saved
OUTPUTS_DIR = os.path.join(PROJECT_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUTS_DIR, "plots")
REPORTS_DIR = os.path.join(OUTPUTS_DIR, "reports")

# ----------------------------------------------------------------------
# 2. IMAGE SETTINGS
# ----------------------------------------------------------------------

# Every image is resized to 224 x 224 pixels before it goes into a model.
# 224 is the size the pre-trained models (VGG16, ResNet50, ...) were built for.
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_SIZE = (IMAGE_HEIGHT, IMAGE_WIDTH)

# Colour images have 3 channels: Red, Green, Blue.
CHANNELS = 3

# The full shape of one image as the model sees it: (height, width, channels)
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS)

# ----------------------------------------------------------------------
# 3. TRAINING SETTINGS
# ----------------------------------------------------------------------

# How many images the model looks at before it updates itself once.
# Smaller batch = less memory needed. 32 is a safe default.
BATCH_SIZE = 32

# One "epoch" = the model has seen every training image one time.
EPOCHS = 10

# How big a step the model takes when it learns. 0.0001 is small and safe
# for transfer learning (we do not want to destroy what the model already knows).
LEARNING_RATE = 0.0001

# If the model stops improving for this many epochs in a row, stop training.
# This saves time and prevents overfitting.
EARLY_STOPPING_PATIENCE = 3

# Fix the random numbers so that running the code twice gives the same result.
RANDOM_SEED = 42

# ----------------------------------------------------------------------
# 4. THE LIST OF MODELS WE WILL TRAIN
# ----------------------------------------------------------------------

# The project asks for a CNN built from scratch PLUS five pre-trained models.
MODEL_NAMES = [
    "CNN_Scratch",      # we build this one ourselves, layer by layer
    "VGG16",            # pre-trained model 1
    "ResNet50",         # pre-trained model 2
    "MobileNet",        # pre-trained model 3
    "InceptionV3",      # pre-trained model 4
    "EfficientNetB0",   # pre-trained model 5
]

# ----------------------------------------------------------------------
# 5. A SMALL HELPER
# ----------------------------------------------------------------------


def create_output_folders():
    """
    Make sure the models / outputs / plots / reports folders exist.

    os.makedirs(..., exist_ok=True) means:
    "create this folder, and do not complain if it is already there".
    """
    for folder in [MODELS_DIR, OUTPUTS_DIR, PLOTS_DIR, REPORTS_DIR]:
        os.makedirs(folder, exist_ok=True)
