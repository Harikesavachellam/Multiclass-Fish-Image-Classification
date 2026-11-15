"""
train.py
--------
This file trains ONE model and saves it.

The loop that trains ALL six models is in train_all_models.py in the
main project folder - that script calls this one, six times.
"""

import json
import os
import time

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from src import config
from src import data_loader
from src import models as model_builder


def train_one_model(model_name, train_generator, val_generator):
    """
    Train a single model and save it as a .h5 file.

    Args:
        model_name:      e.g. "MobileNet"
        train_generator: the conveyor belt of training images
        val_generator:   the conveyor belt of validation images

    Returns:
        history_dict: a dictionary of accuracy/loss for every epoch
        model_path:   where the .h5 file was saved
        train_minutes: how long training took
    """

    print("\n" + "=" * 70)
    print(f"TRAINING: {model_name}")
    print("=" * 70)

    # How many fish species are there? Ask the generator - it counted
    # the folders for us.
    num_classes = train_generator.num_classes
    print(f"Number of classes: {num_classes}")

    # Build the model (see models.py)
    model = model_builder.build_model(model_name, num_classes)

    # Print a table of the layers. Good for the report and for your demo video.
    model.summary()

    # Where this model will be saved
    model_path = os.path.join(config.MODELS_DIR, f"{model_name}.h5")

    # ------------------------------------------------------------------
    # CALLBACKS - little helpers that run automatically during training
    # ------------------------------------------------------------------

    # 1. EarlyStopping: if the validation accuracy stops improving for
    #    3 epochs in a row, stop early and put back the best weights.
    early_stopping = EarlyStopping(
        monitor="val_accuracy",                      # what to watch
        patience=config.EARLY_STOPPING_PATIENCE,     # how long to wait
        restore_best_weights=True,                   # rewind to the best version
        verbose=1,
    )

    # 2. ModelCheckpoint: save the model to disk every time it gets better.
    #    If the computer crashes, the best version is already safe.
    checkpoint = ModelCheckpoint(
        filepath=model_path,
        monitor="val_accuracy",
        save_best_only=True,     # only overwrite when it improves
        verbose=1,
    )

    # ------------------------------------------------------------------
    # THE ACTUAL TRAINING
    # ------------------------------------------------------------------
    start_time = time.time()            # note the clock before we start

    history = model.fit(
        train_generator,                # learn from these images
        validation_data=val_generator,  # check yourself on these images
        epochs=config.EPOCHS,           # repeat this many times
        callbacks=[early_stopping, checkpoint],
        verbose=1,                      # print a progress bar
    )

    train_minutes = (time.time() - start_time) / 60  # how long it took

    print(f"\nFinished {model_name} in {train_minutes:.1f} minutes")
    print(f"Model saved to: {model_path}")

    # history.history is a dictionary like:
    # {"accuracy": [0.4, 0.6, ...], "val_accuracy": [...], "loss": [...], ...}
    history_dict = history.history

    # Save the history as a JSON file so we can draw graphs later
    # without training everything again.
    history_path = os.path.join(config.REPORTS_DIR, f"{model_name}_history.json")
    with open(history_path, "w") as f:
        json.dump(history_dict, f, indent=2)

    return history_dict, model_path, train_minutes


def load_data():
    """
    A tiny shortcut so other scripts do not have to import data_loader
    themselves. Returns the three generators plus the class names.
    """
    train_gen, val_gen, test_gen = data_loader.create_data_generators()
    class_names = data_loader.get_class_names(train_gen)
    return train_gen, val_gen, test_gen, class_names
