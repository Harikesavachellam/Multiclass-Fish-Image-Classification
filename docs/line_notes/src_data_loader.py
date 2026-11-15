"""Line-by-line notes for src/data_loader.py."""

PURPOSE = (
    "This file turns folders full of JPEG files into something a neural network can "
    "actually consume. It never loads the whole dataset into memory - 10,514 images "
    "at 224x224x3 would need gigabytes of RAM. Instead it builds three 'generators', "
    "which read images off the disk in batches of 32, resize them, rescale their "
    "pixels, and (for training only) randomly distort them so the model sees a "
    "slightly different picture every time. The brief specifically requires "
    "ImageDataGenerator, and this is where it is used."
)

NOTES = {
    26: "Imports ImageDataGenerator from Keras. This is the class the project brief "
        "asks for by name. It does two jobs at once: it streams images off the disk "
        "in batches, and it applies the augmentation described below.",

    28: "Imports our own settings file, so the image size, batch size and random "
        "seed all come from the one place rather than being retyped here.",

    31: "Defines the main function of this file. It takes no arguments - everything "
        "it needs comes from config - and hands back all three generators at once.",

    49: "Creates the TRAINING generator's recipe. Everything inside these brackets "
        "describes how to alter each training image before the model sees it. "
        "Nothing is read from disk yet; this is just the set of instructions.",

    50: "Divides every pixel by 255. Images arrive with values from 0 to 255; neural "
        "networks learn far more reliably when numbers are small and sit between "
        "0.0 and 1.0. This single line is the brief's 'rescale images to [0,1]' "
        "requirement.",

    51: "Rotates each image by a random angle of up to 20 degrees in either "
        "direction. A fish photographed at a slight tilt is still that fish, and "
        "teaching the model this stops it relying on the camera angle.",

    52: "Randomly zooms in or out by up to 20%, so the model does not assume the "
        "fish always fills the same amount of the frame.",

    53: "Slides the image left or right by up to 20% of its width, so the fish is "
        "not always dead centre.",

    54: "Slides the image up or down by up to 20% of its height, for the same "
        "reason.",

    55: "Slants the image slightly, as if viewed from a mild angle.",

    56: "Mirrors the image left-to-right at random. A fish facing left is the same "
        "species as one facing right, so this doubles the useful variety for free. "
        "Note there is no vertical flip - an upside-down fish is not a natural "
        "photograph, so teaching that would not help.",

    57: "When rotating or shifting leaves empty corners, fill them by copying the "
        "nearest real pixel. The alternative, leaving black triangles, would teach "
        "the model that black corners are a meaningful feature.",

    58: "Closes the training generator's recipe. Together these six distortions are "
        "the brief's 'rotation, zoom and flipping' augmentation requirement, plus "
        "three extras.",

    65: "Creates the recipe for validation AND test images, and this one rescales "
        "ONLY. This is the most important line in the file to be able to defend: "
        "augmenting test images would mean measuring the model on distorted "
        "pictures that no user would ever upload, so the score would not describe "
        "real-world performance. The same object is reused for both val and test "
        "because their treatment is identical.",

    70: "Now the recipes get pointed at actual folders. flow_from_directory walks "
        "the folder, treats every SUBFOLDER NAME as a class label, and returns an "
        "object that hands out batches of images on demand.",

    71: "Which folder to read - the training images.",

    72: "Resize every image to 224x224 as it is read, regardless of its original "
        "size. The model needs every input to be identical in shape.",

    73: "Hand out 32 images at a time.",

    74: "'categorical' means the labels come back one-hot encoded: for 11 species, "
        "class 3 becomes [0,0,0,1,0,0,0,0,0,0,0]. This is the format that pairs "
        "with a softmax output and categorical_crossentropy loss.",

    75: "Shuffle the training images. Without this the model would see all the "
        "shrimp, then all the trout, and would swing wildly towards whichever "
        "species it saw most recently.",

    76: "Fixes the shuffling order using the seed from config, so two runs of the "
        "program shuffle identically and the results can be reproduced.",

    77: "Closes the training generator. At this point Keras prints how many images "
        "and classes it found.",

    79: "Builds the VALIDATION generator from the rescale-only recipe.",

    80: "Points it at the validation folder.",
    81: "Same 224x224 resize, so validation images match what the model expects.",
    82: "Same batch size of 32.",
    83: "Same one-hot label format.",

    84: "No shuffling. There is nothing to gain from shuffling data you are only "
        "measuring, and keeping a fixed order makes results repeatable.",

    85: "Closes the validation generator.",

    87: "Builds the TEST generator - the final exam set, used only after training "
        "has completely finished.",

    88: "Points it at the test folder.",
    89: "Same resize.",
    90: "Same batch size.",
    91: "Same one-hot label format.",

    92: "shuffle=False here is not a preference, it is REQUIRED for correctness. "
        "evaluate.py compares the model's predictions against test_generator.classes, "
        "which is a plain list of the true labels in folder order. If the generator "
        "shuffled, the predictions would come back in a different order from the "
        "labels and every metric in the project would be silently wrong - not "
        "crashed, just wrong. This is the single easiest place to introduce a bug "
        "that nobody notices.",

    93: "Closes the test generator.",

    95: "Hands all three generators back to whoever called this function, as a "
        "tuple that train.py unpacks into three variables.",

    98: "A small helper that answers the question 'which species does output "
        "number 4 mean?'",

    107: "generator.class_indices is a dictionary like {'shrimp': 8, 'trout': 10}. "
         "sorted() with key=class_indices.get sorts the species NAMES by their "
         "NUMBER, producing a list where position 0 holds the name of class 0. "
         "Getting this order wrong would mislabel every prediction in the app, "
         "which is why it is derived from Keras rather than typed out by hand.",

    108: "Returns that ordered list of species names.",

    111: "A one-line helper reporting how many images a generator found.",

    113: ".samples is a number Keras fills in when it scans the folder. It is used "
         "in the printed summary and in the report.",
}
