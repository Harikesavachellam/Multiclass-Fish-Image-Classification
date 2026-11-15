"""
data_loader.py
--------------
This file reads the fish images from the folders and gets them ready
for the model.

The folders must look like this:

    data/
      train/
        animal fish/        <- every image of this species goes in this folder
        shrimp/
        trout/
        ...
      val/
        animal fish/
        ...
      test/
        animal fish/
        ...

The FOLDER NAME is the label. Keras reads the folder names automatically,
so we never have to write the class names by hand.
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from src import config


def create_data_generators():
    """
    Build three "generators": one for train, one for validation, one for test.

    A generator is like a conveyor belt. Instead of loading 10,000 images into
    memory at once (your computer would run out of RAM), it loads them in small
    batches of 32, one batch at a time.

    Returns:
        train_generator, val_generator, test_generator
    """

    # ------------------------------------------------------------------
    # STEP 1: the TRAINING generator - with data augmentation
    # ------------------------------------------------------------------
    # Augmentation = slightly changing each image every time the model sees it
    # (rotate it, zoom it, flip it). The fish is still the same fish, but the
    # model sees a new picture each time, so it learns better and memorises less.
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,        # turn pixel values from 0-255 into 0.0-1.0
        rotation_range=20,        # rotate the image randomly up to 20 degrees
        zoom_range=0.2,           # zoom in or out randomly by up to 20%
        width_shift_range=0.2,    # slide the image left/right by up to 20%
        height_shift_range=0.2,   # slide the image up/down by up to 20%
        shear_range=0.2,          # slant the image a little
        horizontal_flip=True,     # mirror the image left-to-right
        fill_mode="nearest",      # fill any empty corners with the nearest pixel
    )

    # ------------------------------------------------------------------
    # STEP 2: the VALIDATION and TEST generators - NO augmentation
    # ------------------------------------------------------------------
    # We only rescale here. We never augment validation or test images,
    # because we want to measure the model on real, untouched pictures.
    val_test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    # ------------------------------------------------------------------
    # STEP 3: point each generator at its folder
    # ------------------------------------------------------------------
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,              # which folder to read
        target_size=config.IMAGE_SIZE,  # resize every image to 224 x 224
        batch_size=config.BATCH_SIZE,   # 32 images per batch
        class_mode="categorical",       # many classes -> one-hot labels
        shuffle=True,                   # mix the images up while training
        seed=config.RANDOM_SEED,        # keep the shuffling repeatable
    )

    val_generator = val_test_datagen.flow_from_directory(
        config.VAL_DIR,
        target_size=config.IMAGE_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        shuffle=False,                  # no shuffling: we just measure
    )

    test_generator = val_test_datagen.flow_from_directory(
        config.TEST_DIR,
        target_size=config.IMAGE_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        shuffle=False,                  # IMPORTANT: keeps predictions lined up
    )                                   # with the true labels

    return train_generator, val_generator, test_generator


def get_class_names(generator):
    """
    Get the species names in the exact order the model uses them.

    generator.class_indices looks like {'shrimp': 0, 'trout': 1}.
    We flip it around into a list: ['shrimp', 'trout'],
    so that position 0 in the model's output means 'shrimp'.
    """
    # sort the dictionary by its number (0, 1, 2, ...) and keep the names
    class_names = sorted(generator.class_indices, key=generator.class_indices.get)
    return class_names


def count_images(generator):
    """How many images did this generator find? (useful for the report)"""
    return generator.samples
