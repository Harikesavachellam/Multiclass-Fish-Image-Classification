"""Line-by-line notes for src/models.py."""

PURPOSE = (
    "This file BUILDS the models; it never trains them. Think of it as drawing the "
    "blueprints. There are two kinds here: a CNN stacked up by hand layer by layer, "
    "and five pre-trained networks that already know what edges, textures and shapes "
    "look like from a million ImageNet photographs. One dictionary and one dispatcher "
    "function mean the five pre-trained models share a single piece of code instead "
    "of being copy-pasted five times."
)

NOTES = {
    14: "Imports the three Keras pieces this file needs: 'layers' for the building "
        "blocks, 'models' for the container that holds them, and 'optimizers' for "
        "the algorithm that does the learning.",

    15: "Opens a bracketed import of the five pre-trained architectures. Keras ships "
        "these as ready-made functions.",
    16: "VGG16 - deep, simple and heavy, from 2014.",
    17: "ResNet50 - uses skip connections so very deep networks still train.",
    18: "MobileNet - built to be small and fast enough to run on a phone.",
    19: "InceptionV3 - examines each image at several scales at once.",
    20: "EfficientNetB0 - balances depth, width and resolution together.",
    21: "Closes the import.",

    23: "Imports our settings, so the input shape and learning rate come from "
        "config rather than being written again here.",

    31: "Defines the from-scratch CNN builder. num_classes is passed in rather than "
        "hard-coded, so the same function works whether the dataset has 11 species "
        "or 50.",

    49: "Creates an empty Sequential model. 'Sequential' means the layers run in a "
        "straight line, each feeding the next. The name is used later for the "
        "filenames of the saved model and its graphs.",

    52: "Declares the shape of one incoming image: 224x224x3. The model needs to "
        "know this up front so it can work out the size of every layer that follows.",

    57: "Block 1. Conv2D(32, (3,3)) slides thirty-two separate 3x3 windows across "
        "the image, each learning to react to one kind of pattern - a vertical "
        "edge, a patch of colour, a texture. 'relu' turns any negative result into "
        "zero, which is what lets the network learn non-straight-line relationships. "
        "padding='same' keeps the output the same width and height as the input.",

    60: "Halves the picture from 224x224 to 112x112 by keeping only the strongest "
        "pixel in each 2x2 square. This throws away precise positions but keeps "
        "whether a pattern was present, and it cuts the work for every later layer "
        "to a quarter.",

    63: "Block 2 doubles the filters to 64. The deeper you go, the more different "
        "patterns there are to recognise, because they are combinations of the "
        "simpler ones found earlier.",
    64: "Halves the picture again, 112 to 56.",

    67: "Block 3 with 128 filters, now spotting larger structures such as fin "
        "shapes.",
    68: "Halves again, 56 to 28.",

    71: "Block 4, also 128 filters, working on the most abstract patterns.",
    72: "Halves a final time, 28 to 14. The picture is now a 14x14 grid, 128 "
        "channels deep.",

    75: "Flatten unrolls that 14x14x128 block of numbers into one long line of "
        "25,088 values, because the Dense layers that follow only accept a flat "
        "list. This single step is responsible for most of this model's 6.6 million "
        "parameters.",

    78: "A fully connected layer of 256 neurons, each of which looks at ALL the "
        "flattened values at once and mixes them together.",

    82: "Dropout randomly switches off half the neurons on each training step. It "
        "sounds destructive, and that is the point: the model cannot lean on any "
        "one neuron, so it is forced to learn patterns that generalise rather than "
        "memorising individual training photographs. It is switched off "
        "automatically when predicting.",

    87: "The output layer - exactly one neuron per fish species. 'softmax' squeezes "
        "the eleven numbers so they are all positive and add up to 1.0, which lets "
        "you read them as percentages of confidence.",

    90: "Compiling fixes HOW the model will learn. Nothing has been trained yet.",

    91: "Adam is the optimiser - the algorithm that decides how to adjust each "
        "weight. 0.001 is used here, ten times larger than the pre-trained models "
        "use, because this network starts from random values and has a long way to "
        "travel.",

    92: "categorical_crossentropy is the standard loss function when there are many "
        "mutually exclusive classes and the labels are one-hot encoded. It "
        "punishes the model more heavily the more confidently it is wrong.",

    93: "Asks Keras to print accuracy as it trains, so progress is visible.",
    94: "Closes the compile call.",

    96: "Returns the finished, compiled model, ready for train.py to fit.",

    105: "A dictionary mapping each model's NAME to the Keras FUNCTION that builds "
         "it. In Python a function can be stored in a dictionary like any other "
         "value. This is the trick that replaces five near-identical functions with "
         "one.",
    106: "The entry for VGG16.",
    107: "The entry for ResNet50.",
    108: "The entry for MobileNet.",
    109: "The entry for InceptionV3.",
    110: "The entry for EfficientNetB0.",
    111: "Closes the dictionary.",

    114: "One function that builds ANY of the five pre-trained models. The name "
         "decides which, so adding a sixth means adding one dictionary entry above "
         "and nothing else.",

    133: "Looks the name up in the dictionary and gets back the builder function "
         "itself - not a result, the function. The next lines then call it.",

    139: "Calls that builder to create the pre-trained base.",

    140: "weights='imagenet' downloads the weights learned from 1.2 million "
         "photographs. This is the entire point of transfer learning: the model "
         "arrives already knowing how to see.",

    141: "include_top=False discards the original 1,000-category output layer, "
         "which was built to recognise ImageNet classes like 'dog' and 'teapot'. We "
         "want our own eleven-species layer instead.",

    142: "Tells it to expect our 224x224x3 images.",
    143: "Closes the base model call.",

    149: "Freezes the base. 'trainable = False' means these millions of weights will "
         "NOT change during training - only the new layers we add will learn. This "
         "is what makes training finish in minutes instead of hours. Be ready to "
         "discuss this line: strictly speaking, freezing the whole base makes this "
         "FEATURE EXTRACTION rather than FINE-TUNING, which would involve "
         "unfreezing some layers and training them at a very low learning rate.",

    152: "Starts a new Sequential container to hold the base plus our own layers.",
    153: "Declares the input shape again for this outer model.",

    159: "A special case, and the single most dangerous line in the project to "
         "remove. EfficientNetB0 contains its own rescaling step and expects pixels "
         "in the 0-255 range, but our generator has already divided them by 255.",

    160: "So we multiply by 255 again to undo that, giving EfficientNet exactly what "
         "it expects. Without these two lines the model still trains, still reports "
         "no error, and still scores close to random - a bug that fails silently.",

    162: "Adds the whole frozen pre-trained network as a single layer in our stack.",

    166: "GlobalAveragePooling2D replaces Flatten here. Instead of unrolling "
         "everything, it takes the average of each filter's output, turning a "
         "7x7x1280 block into just 1280 numbers. That is far fewer parameters, "
         "which means less memory and much less overfitting.",

    168: "Our own 256-neuron thinking layer, which learns to combine the "
         "pre-trained features into something fish-specific.",

    169: "Dropout of 0.3 here rather than 0.5, because there are fewer parameters "
         "to overfit with when the base is frozen.",

    170: "The output layer: one neuron per species, softmax for probabilities. "
         "Identical in purpose to line 87.",

    172: "Compiles the assembled model.",

    174: "Uses config.LEARNING_RATE, which is 0.0001 - ten times SMALLER than the "
         "from-scratch CNN's. Large updates would wreck the carefully learned "
         "ImageNet weights feeding into this head.",

    175: "The same loss function as before, for the same reason.",
    176: "Print accuracy during training.",
    177: "Closes the compile call.",
    179: "Returns the finished model.",

    187: "The dispatcher - the only function the rest of the project ever calls. "
         "train.py does not know or care whether a model is hand-built or "
         "pre-trained; it just passes a name.",

    193: "If the name is the from-scratch CNN...",
    194: "...build and return that one.",

    196: "Otherwise, if the name is one of the five keys in the dictionary...",
    197: "...build and return the pre-trained version.",

    200: "If the name matches nothing, raise an error rather than returning None. "
         "Returning None would cause a confusing crash much later, somewhere else "
         "entirely.",
    201: "The message states exactly which name was not recognised...",
    202: "...and lists the valid choices, so the fix is obvious without reading the "
         "source.",
    203: "Closes the error.",
}
