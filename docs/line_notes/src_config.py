"""Line-by-line notes for src/config.py."""

PURPOSE = (
    "This file holds every setting in the project and contains almost no logic. "
    "Change the image size or the number of epochs here once, and all six models "
    "pick it up. Writing a number like 224 into five different files is the most "
    "common way a project becomes impossible to maintain, and this file exists to "
    "stop that happening. Every other module begins by importing it."
)

NOTES = {
    12: "Imports Python's os module. It is the only import this file needs, and it "
        "is used purely to join folder names together into full paths.",

    19: "__file__ is a built-in variable holding the path of this very file. "
        "os.path.abspath() expands it to a full path, and os.path.dirname() then "
        "strips the filename off, leaving the folder. So SRC_DIR ends up pointing "
        "at the src folder, no matter where you were standing when you ran Python.",

    22: "Applies dirname once more to step UP one level, from src to the project "
        "folder itself. Working paths out from __file__ like this is what makes "
        "the project portable - the 'works the same in every environment' "
        "requirement in the brief.",

    25: "Builds the path to the data folder. os.path.join picks the right slash for "
        "the operating system - a backslash on Windows, a forward slash on Mac and "
        "Linux - so the same code runs on all three.",

    27: "The folder of images used to TEACH the model. These are the only images "
        "the model is allowed to learn from.",

    28: "The folder used to CHECK the model after each epoch while it trains. The "
        "model never learns from these, so they give an honest progress reading.",

    29: "The folder used for the FINAL exam, once training is completely finished. "
        "Keeping these three sets separate is what makes the reported accuracy "
        "mean something.",

    32: "Where the trained .h5 model files get saved.",

    35: "The parent folder for everything the program produces.",

    36: "Where the PNG graphs go - training curves, confusion matrices and the "
        "comparison chart.",

    37: "Where text output goes - the CSV comparison table and the per-species "
        "classification reports. Keeping pictures and text apart keeps the results "
        "tidy and easy to hand in.",

    45: "The height every image is resized to. 224 is not arbitrary: VGG16, "
        "ResNet50, MobileNet and EfficientNetB0 were all originally trained on "
        "224x224 pictures, so giving them that size gets the most out of their "
        "pre-trained weights.",

    46: "The width, also 224, so every image ends up square.",

    47: "Bundles the height and width into a tuple. Keras's flow_from_directory "
        "expects the target size in exactly this (height, width) form.",

    50: "Colour images carry three numbers per pixel - Red, Green and Blue. A "
        "black-and-white dataset would use 1 here.",

    53: "The complete shape of ONE image as a model sees it: 224 rows, 224 "
        "columns, 3 colour channels. Every model built in models.py is shaped "
        "around this one constant.",

    61: "How many images the model looks at before it adjusts itself once. A bigger "
        "batch trains faster but needs far more memory; 32 is the usual safe "
        "default and fits comfortably on a laptop with no graphics card.",

    64: "One epoch means the model has seen every training image exactly once. Ten "
        "is the ceiling here - EarlyStopping may stop sooner if progress stalls.",

    68: "The size of each adjustment the model makes while learning. 0.0001 is "
        "deliberately tiny for the pre-trained models, so training nudges what "
        "they already know rather than wiping it out. The from-scratch CNN uses a "
        "larger value because it starts out knowing nothing.",

    72: "How many epochs of no improvement to tolerate before stopping. One poor "
        "epoch is normal noise; three in a row means the model has genuinely "
        "plateaued and further training is just wasting time.",

    75: "Fixes Python's random number generator. The shuffling and the "
        "train/val/test split then come out identical on every run, so your "
        "results are reproducible. Any number works - 42 is a programmer's joke "
        "that became a convention.",

    82: "Opens the list of the six models to train. This list is the backbone of "
        "the whole project: train_all_models.py simply loops over it.",

    83: "The convolutional network built by hand, layer by layer, in models.py.",

    84: "VGG16 - an older, very deep and very heavy pre-trained network.",

    85: "ResNet50 - introduced 'skip connections', which let networks get much "
        "deeper without breaking during training.",

    86: "MobileNet - designed to be small and fast enough for phones. In this "
        "project it turned out to be both the most accurate and the quickest.",

    87: "InceptionV3 - looks at each image at several different scales at once.",

    88: "EfficientNetB0 - scales depth, width and resolution together in a balanced "
        "way. It needs one special fix, explained in models.py.",

    89: "Closes the list. To add a seventh model you add one name here and one line "
        "in models.py. Nothing else in the project changes - that is the payoff "
        "from driving the program off a list instead of six copy-pasted blocks.",

    96: "Defines the only function in this file. It takes no arguments because "
        "every path it needs is already a constant above.",

    103: "Loops over the four folders the program writes into.",

    104: "Creates the folder, including any missing parent folders. exist_ok=True "
         "means 'do not raise an error if it already exists', so this is safe to "
         "call on every single run. It matters because git does not store empty "
         "folders, so a freshly cloned copy of the project would otherwise crash "
         "the first time it tried to save a model.",
}
