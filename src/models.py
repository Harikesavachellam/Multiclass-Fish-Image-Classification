"""
models.py
---------
This file BUILDS the models. It does not train them - training happens in
train.py. Here we only describe the shape of each model.

There are two kinds of model in this project:

1. A CNN we build from scratch  (we stack the layers ourselves)
2. Five pre-trained models       (already trained on millions of photos,
                                  we just teach them about fish)
"""

from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import (
    VGG16,
    ResNet50,
    MobileNet,
    InceptionV3,
    EfficientNetB0,
)

from src import config


# ======================================================================
# PART 1: THE CNN WE BUILD OURSELVES
# ======================================================================


def build_cnn_from_scratch(num_classes):
    """
    Build a simple Convolutional Neural Network (CNN) from nothing.

    The idea: each Conv2D layer looks for patterns in the image.
    - the first layers find simple things (edges, colours)
    - the later layers find complicated things (fins, tails, scales)
    Each MaxPooling2D layer shrinks the image, so the next layer can look
    at a bigger area with the same amount of work.

    Args:
        num_classes: how many fish species we have (e.g. 11)

    Returns:
        a compiled Keras model, ready to train
    """

    # Sequential means: "stack these layers one after another, top to bottom"
    model = models.Sequential(name="CNN_Scratch")

    # --- tell the model what size picture to expect ---
    model.add(layers.Input(shape=config.INPUT_SHAPE))  # (224, 224, 3)

    # --- block 1: 32 filters ---
    # Conv2D(32, (3,3)) = slide 32 small 3x3 windows over the image,
    # each window learns to spot one kind of pattern.
    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same"))
    # MaxPooling2D((2,2)) = keep only the strongest pixel in every 2x2 square,
    # which halves the width and height (224 -> 112)
    model.add(layers.MaxPooling2D((2, 2)))

    # --- block 2: 64 filters (deeper = more patterns) ---
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D((2, 2)))                      # 112 -> 56

    # --- block 3: 128 filters ---
    model.add(layers.Conv2D(128, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D((2, 2)))                      # 56 -> 28

    # --- block 4: 128 filters ---
    model.add(layers.Conv2D(128, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D((2, 2)))                      # 28 -> 14

    # --- flatten the 3D block of numbers into one long 1D list ---
    model.add(layers.Flatten())

    # --- a normal "fully connected" layer that mixes all the patterns ---
    model.add(layers.Dense(256, activation="relu"))

    # Dropout(0.5) randomly switches off half the neurons during training.
    # This stops the model from simply memorising the training pictures.
    model.add(layers.Dropout(0.5))

    # --- the output layer: one neuron per fish species ---
    # softmax turns the numbers into probabilities that add up to 1.0,
    # e.g. [0.02, 0.91, 0.07] -> "91% sure it is class number 1"
    model.add(layers.Dense(num_classes, activation="softmax"))

    # Compiling = choosing how the model learns
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),  # Adam = a good default
        loss="categorical_crossentropy",   # the standard loss for many classes
        metrics=["accuracy"],              # what we want printed while training
    )

    return model


# ======================================================================
# PART 2: THE FIVE PRE-TRAINED MODELS (TRANSFER LEARNING)
# ======================================================================

# A small dictionary: model name -> the Keras function that builds it.
# This lets us write ONE function instead of five almost identical ones.
PRETRAINED_MODELS = {
    "VGG16": VGG16,
    "ResNet50": ResNet50,
    "MobileNet": MobileNet,
    "InceptionV3": InceptionV3,
    "EfficientNetB0": EfficientNetB0,
}


def build_pretrained_model(model_name, num_classes):
    """
    Take a model that is already trained on ImageNet (1.2 million photos)
    and teach it about fish instead.

    This is called TRANSFER LEARNING. The model already knows what edges,
    textures and shapes look like, so it learns fish much faster than a
    model starting from zero.

    Args:
        model_name: one of "VGG16", "ResNet50", "MobileNet",
                    "InceptionV3", "EfficientNetB0"
        num_classes: how many fish species we have

    Returns:
        a compiled Keras model, ready to train
    """

    # Look up the builder function for the name we were given
    base_model_function = PRETRAINED_MODELS[model_name]

    # Build the base model:
    #   weights="imagenet"  -> download the already-learned weights
    #   include_top=False   -> throw away its old 1000-class output layer,
    #                          because we want our own fish output layer
    base_model = base_model_function(
        weights="imagenet",
        include_top=False,
        input_shape=config.INPUT_SHAPE,
    )

    # FREEZE the base model.
    # trainable = False means "do not change these layers while training".
    # We only train the new layers we add on top. This is fast and avoids
    # ruining the knowledge the model already has.
    base_model.trainable = False

    # Now stack: input -> (fix pixels if needed) -> base model -> our new layers
    model = models.Sequential(name=model_name)
    model.add(layers.Input(shape=config.INPUT_SHAPE))

    # SPECIAL CASE for EfficientNetB0:
    # our generator already divided the pixels by 255 (so they are 0.0-1.0),
    # but EfficientNet contains its own rescaling and expects 0-255.
    # So we multiply by 255 again to give it what it wants.
    if model_name == "EfficientNetB0":
        model.add(layers.Rescaling(255.0))

    model.add(base_model)

    # GlobalAveragePooling2D squeezes the base model's output into one
    # number per filter. It is a lighter alternative to Flatten().
    model.add(layers.GlobalAveragePooling2D())

    model.add(layers.Dense(256, activation="relu"))  # our own thinking layer
    model.add(layers.Dropout(0.3))                   # a little anti-memorising
    model.add(layers.Dense(num_classes, activation="softmax"))  # fish output

    model.compile(
        # a SMALL learning rate, because we do not want big, clumsy changes
        optimizer=optimizers.Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# ======================================================================
# PART 3: ONE FUNCTION THAT BUILDS ANY MODEL BY NAME
# ======================================================================


def build_model(model_name, num_classes):
    """
    The only function the rest of the project needs to call.

    Give it a name from config.MODEL_NAMES and it returns the right model.
    """
    if model_name == "CNN_Scratch":
        return build_cnn_from_scratch(num_classes)

    if model_name in PRETRAINED_MODELS:
        return build_pretrained_model(model_name, num_classes)

    # If someone types a name we do not know, say so clearly.
    raise ValueError(
        f"Unknown model name: '{model_name}'. "
        f"Choose one of: {config.MODEL_NAMES}"
    )
