"""
walkthrough_content.py
----------------------
All the WORDS that go into the documentation PDF live here.

make_code_pdf.py reads this file for the explanations, and reads the real
.py files for the code. Keeping them apart means the code in the PDF is
always the code that actually runs.

How a file entry is shaped:

    {
        "path":    "src/config.py",          <- where the file is
        "role":    "Settings",               <- a two-word label
        "purpose": "One paragraph ...",       <- why the file exists
        "blocks": [
            {
                "start":   "import os",       <- the EXACT first line of the block
                "title":   "Imports",
                "explain": ["line 14 - ...", "line 15 - ..."],
            },
        ],
    }
"""

DOCUMENT_TITLE = "Multiclass Fish Image Classification"
DOCUMENT_SUBTITLE = "The complete code, explained line by line"
DOCUMENT_AUTHOR = "Project documentation"

COVER_FACTS = [
    ("Domain", "Image Classification"),
    ("Problem", "Predict the species of a fish from a photograph"),
    ("Models", "1 CNN built from scratch + 5 pre-trained models"),
    ("Pre-trained", "VGG16, ResNet50, MobileNet, InceptionV3, EfficientNetB0"),
    ("Framework", "TensorFlow / Keras"),
    ("Deployment", "Streamlit web application"),
    ("Metrics", "Accuracy, Precision, Recall, F1-score, Confusion matrix"),
    ("Language", "Python 3"),
]


# ======================================================================
# THE CHAPTERS THAT COME BEFORE THE CODE
# ======================================================================

INTRO_SECTIONS = [
    (
        "What this project does",
        [
            "The project takes a photograph of a fish and predicts which species it "
            "belongs to. It does this with deep learning: a computer program that "
            "learns the difference between species by looking at thousands of example "
            "photographs, instead of being told any rules by a human.",

            ("The three business goals",),

            [
                "Enhanced accuracy - find out which model architecture classifies fish "
                "best, by training six different ones on exactly the same data.",
                "Deployment ready - wrap the winning model in a web application so a "
                "non-technical person can upload a photo and get an answer immediately.",
                "Model comparison - measure every model with the same four metrics so "
                "the choice of model is based on numbers, not on opinion.",
            ],

            ("What gets built",),

            [
                "A CNN (Convolutional Neural Network) built from scratch, layer by layer.",
                "Five pre-trained models - VGG16, ResNet50, MobileNet, InceptionV3 and "
                "EfficientNetB0 - adapted to fish through transfer learning.",
                "A full evaluation: accuracy, precision, recall, F1-score, a confusion "
                "matrix and training graphs for every one of the six models.",
                "A Streamlit web app that loads the best model and predicts from an "
                "uploaded image, showing a confidence score for every species.",
            ],
        ],
    ),
    (
        "The dataset",
        [
            "The dataset is a single 261 MB zip from the project's Google Drive link. It "
            "unpacks into a data/ folder that is already divided into train, val and test, "
            "with one subfolder per species. The folder name is the label - there is no "
            "separate CSV of answers to keep in step with the images.",

            ("The numbers",),
            [
                "11 species, 10,514 JPEG images in total.",
                "6,225 training images - what the models learn from.",
                "1,092 validation images - checked after every epoch, used by EarlyStopping "
                "to decide when to stop.",
                "3,197 test images - the final exam, used once.",
            ],

            ("The species",),
            [
                "animal fish - 1096 train / 187 val / 527 test",
                "animal fish bass - 30 train / 10 val / 13 test",
                "fish sea_food black_sea_sprat - 569 / 105 / 298",
                "fish sea_food gilt_head_bream - 566 / 94 / 305",
                "fish sea_food hourse_mackerel - 573 / 97 / 286",
                "fish sea_food red_mullet - 579 / 90 / 291",
                "fish sea_food red_sea_bream - 571 / 113 / 273",
                "fish sea_food sea_bass - 538 / 97 / 327",
                "fish sea_food shrimp - 576 / 100 / 292",
                "fish sea_food striped_red_mullet - 547 / 101 / 293",
                "fish sea_food trout - 580 / 98 / 292",
            ],

            ("The one thing to notice",),
            [
                "Ten of the eleven classes are well balanced, at roughly 550 training "
                "images each. 'animal fish bass' is the exception: 30 training images, "
                "about 5% of a normal class.",
                "This single imbalance shapes how the results must be read. A model can "
                "ignore that class almost entirely and still score well on plain accuracy, "
                "because it is only 0.5% of the test set.",
                "That is exactly why the project reports weighted precision, recall and F1 "
                "as well as accuracy, and why the per-species classification report and the "
                "confusion matrix matter more here than the single headline number.",
                "Expect 'animal fish bass' to have the weakest recall of the eleven. If an "
                "evaluator asks how you would fix it, the honest answers are: collect more "
                "images of that species, use class weights in model.fit(), or merge it into "
                "'animal fish' if the distinction does not matter for the use case.",
            ],
        ],
    ),
    (
        "The ideas you need to follow the code",
        [
            "You do not need advanced mathematics to read this project, but these eight "
            "ideas appear everywhere in the code, so it is worth knowing what each one "
            "means before you start.",

            ("1. An image is just numbers",),
            [
                "A colour photo of 224x224 pixels is a block of numbers with the shape "
                "(224, 224, 3): height, width, and 3 colour channels (Red, Green, Blue).",
                "Each number is a brightness from 0 to 255. We divide every number by 255 "
                "so they all sit between 0.0 and 1.0. Neural networks learn much more "
                "steadily from small numbers than from large ones. This is called rescaling "
                "or normalisation.",
            ],

            ("2. What a CNN actually does",),
            [
                "A Convolutional Neural Network slides small windows (filters) across the "
                "image looking for patterns. Early layers find simple things such as edges "
                "and colour changes; later layers combine those into complicated things "
                "such as a fin, a tail or a scale pattern.",
                "A pooling layer shrinks the picture between those steps (224 becomes 112, "
                "then 56, then 28). Less detail, but a wider view and far less work.",
                "At the end, the block of numbers is flattened into one long list and fed "
                "to ordinary Dense layers, which make the final decision.",
            ],

            ("3. Transfer learning",),
            [
                "Training a model from zero needs millions of pictures. Instead we take a "
                "model that was already trained on ImageNet - 1.2 million photographs of "
                "1000 everyday objects - and reuse everything it learned about shapes and "
                "textures.",
                "We remove its old output layer (include_top=False), freeze the rest so it "
                "cannot be damaged (base_model.trainable = False), and attach our own small "
                "output layer that knows about fish species.",
                "Result: far less training time, far fewer images needed, and usually much "
                "better accuracy than a from-scratch CNN.",
            ],

            ("4. Train, validation and test",),
            [
                "Train set - the images the model learns from. It sees these over and over.",
                "Validation set - images the model never learns from, checked after every "
                "epoch to see whether it is still improving. Used to decide when to stop.",
                "Test set - the final exam. Used exactly once, at the end, to report honest "
                "scores. Never used for any decision during training.",
            ],

            ("5. Epoch, batch and learning rate",),
            [
                "Epoch - one complete pass through all the training images.",
                "Batch - the small group of images (32 here) the model looks at before it "
                "adjusts itself once. Smaller batches use less memory.",
                "Learning rate - how big each adjustment is. We use 0.001 for the "
                "from-scratch CNN, but a much smaller 0.0001 for the pre-trained models, "
                "because large steps would wreck the knowledge they already have.",
            ],

            ("6. Overfitting, and the two defences used here",),
            [
                "Overfitting is when a model memorises the training photos instead of "
                "learning what a species looks like. You spot it on the graphs: the "
                "training accuracy keeps climbing while the validation accuracy stalls or "
                "falls.",
                "Defence 1 - data augmentation. Every time the model sees a training image, "
                "it is randomly rotated, zoomed, shifted or flipped. The fish is the same, "
                "the picture is not, so there is nothing fixed to memorise.",
                "Defence 2 - dropout. During training a Dropout(0.5) layer switches off a "
                "random half of the neurons, so the model cannot rely on any single one.",
            ],

            ("7. Softmax and confidence",),
            [
                "The last layer has one neuron per species and uses the softmax activation, "
                "which turns raw numbers into probabilities that add up to 1.0.",
                "An output of [0.02, 0.91, 0.07] means the model is 91% confident the "
                "answer is species number 1. np.argmax() picks the position of the largest "
                "number, and that position is the predicted species.",
            ],

            ("8. The four metrics",),
            [
                "Accuracy - of all the test images, what fraction did the model get right? "
                "Misleading on its own when some species have many more images than others.",
                "Precision - when the model says 'shrimp', how often is it really shrimp? "
                "Low precision means false alarms.",
                "Recall - of all the real shrimp photos, how many did the model find? Low "
                "recall means it missed some.",
                "F1-score - a single number balancing precision and recall. This is the "
                "metric to quote when the dataset is unbalanced.",
            ],
        ],
    ),
    (
        "How to run the whole project",
        [
            "Four commands, in this order. Each one is explained in full in the chapter "
            "for the file it runs.",

            ("Step 0 - install the libraries",),
            ["pip install -r requirements.txt"],

            ("Step 1 - arrange the images",),
            [
                "python prepare_dataset.py --source \"C:/path/to/the/unzipped/dataset\"",
                "This creates data/train, data/val and data/test, with one subfolder per "
                "species, and prints how many images are in each.",
            ],

            ("Step 2 - train and evaluate all six models",),
            [
                "python train_all_models.py",
                "To test quickly first: python train_all_models.py --model MobileNet --epochs 2",
                "This writes the .h5 model files, the graphs, the confusion matrices, the "
                "per-species reports and the comparison CSV.",
            ],

            ("Step 2b - write the comparison report",),
            [
                "python make_report.py",
                "Builds outputs/reports/comparison_report.md from the CSV and fills in "
                "the Results section of README.md automatically.",
            ],

            ("Step 3 - launch the web app",),
            [
                "streamlit run app.py",
                "Then open http://localhost:8501 and upload a fish photo.",
            ],

            ("Optional - rebuild this document",),
            ["python make_code_pdf.py"],
        ],
    ),
    (
        "How the files fit together",
        [
            "The project separates reusable code from the scripts you run. Everything "
            "inside src/ is a library: it defines functions but never does anything on its "
            "own. The three scripts in the main folder are the things you actually run. "
            "This separation is what 'modular programming' means in practice, and it is why "
            "no piece of logic is written twice.",

            ("The library - src/",),
            [
                "config.py - every setting in the project: paths, image size, batch size, "
                "epochs, learning rate, the list of model names. Changed in one place only.",
                "data_loader.py - reads the images off the disk, rescales them, augments the "
                "training ones, and hands out batches.",
                "models.py - builds the six model architectures. Builds only; never trains.",
                "train.py - trains one model, saves it as .h5, saves its history as JSON.",
                "evaluate.py - scores a saved model on the test set and draws its confusion "
                "matrix.",
                "visualize.py - every graph in the project: training curves, the comparison "
                "bar chart, the class distribution chart.",
            ],

            ("The scripts you run",),
            [
                "prepare_dataset.py - run once, to arrange the downloaded images.",
                "train_all_models.py - the main script. Calls train.py, evaluate.py and "
                "visualize.py six times and picks the winner.",
                "make_report.py - writes the comparison report and fills in the "
                "Results section of the README.",
                "app.py - the Streamlit web application that serves the winning model.",
                "make_code_pdf.py - builds this document.",
            ],

            ("The order things happen in",),
            [
                "prepare_dataset.py puts images into data/train, data/val, data/test.",
                "train_all_models.py asks data_loader.py for three generators.",
                "For each of the six names in config.MODEL_NAMES it calls train.py, which "
                "asks models.py to build that architecture, then fits it and saves "
                "models/<name>.h5.",
                "evaluate.py loads that .h5 file back, predicts on the test set and returns "
                "a dictionary of scores.",
                "visualize.py draws the graphs; the scores are written to "
                "outputs/reports/model_comparison.csv.",
                "The highest-accuracy model is copied to models/best_model.h5.",
                "app.py loads models/best_model.h5 and models/class_names.json and serves "
                "predictions in the browser.",
            ],
        ],
    ),
]


# ======================================================================
# THE CODE CHAPTERS
# ======================================================================

FILES = [
    # ------------------------------------------------------------------
    {
        "path": "src/config.py",
        "role": "Settings - read by every other file",
        "purpose": (
            "This file holds every setting in the project and contains no logic at all. "
            "If you want to change the image size, the batch size or the number of epochs, "
            "you change it here once and all six models pick it up. Hard-coding a number "
            "such as 224 in five different files is the single most common way a project "
            "becomes impossible to maintain, and this file exists to prevent that."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "The triple-quoted text at the top of a file is called a module "
                    "docstring. Python stores it, and tools such as help() can print it.",
                    "Every file in this project starts with one, which is part of the PEP 8 "
                    "coding standard the project is graded against.",
                ],
            },
            {
                "start": "import os",
                "title": "The only import",
                "explain": [
                    "os is Python's standard library for working with the operating system. "
                    "Here it is used only to join folder names into paths.",
                    "Using os.path.join instead of writing \"data/train\" by hand means the "
                    "project runs unchanged on Windows, Mac and Linux, which is the "
                    "'portable' requirement in the evaluation metrics.",
                ],
            },
            {
                "start": "# 1. FOLDER PATHS",
                "title": "Section 1 - working out where everything lives",
                "explain": [
                    "__file__ is a built-in variable holding the path of this file.",
                    "os.path.abspath(__file__) turns it into a full path; "
                    "os.path.dirname(...) then strips the file name off, leaving the folder. "
                    "So SRC_DIR is .../multiclass_fish_classification/src.",
                    "PROJECT_DIR applies dirname once more to step up one level, to "
                    ".../multiclass_fish_classification.",
                    "Because both are worked out from __file__, the project runs correctly "
                    "no matter which folder you are standing in when you launch it.",
                    "DATA_DIR, TRAIN_DIR, VAL_DIR and TEST_DIR point at the three image "
                    "folders Keras will read.",
                    "MODELS_DIR is where the .h5 files are saved.",
                    "PLOTS_DIR holds the PNG graphs; REPORTS_DIR holds the CSV and text "
                    "reports. Separating pictures from text keeps the outputs tidy.",
                ],
            },
            {
                "start": "# 2. IMAGE SETTINGS",
                "title": "Section 2 - image settings",
                "explain": [
                    "IMAGE_HEIGHT and IMAGE_WIDTH are both 224. That is not an arbitrary "
                    "choice: VGG16, ResNet50, MobileNet and EfficientNetB0 were all trained "
                    "on 224x224 images, so feeding them that size gets the most out of their "
                    "pre-trained weights.",
                    "IMAGE_SIZE is the pair (224, 224). Keras's flow_from_directory expects "
                    "the size as a tuple in exactly this form.",
                    "CHANNELS = 3 because the images are colour: Red, Green and Blue.",
                    "INPUT_SHAPE = (224, 224, 3) is the shape of ONE image as the model sees "
                    "it. Every model in models.py is built around this constant.",
                ],
            },
            {
                "start": "# 3. TRAINING SETTINGS",
                "title": "Section 3 - training settings",
                "explain": [
                    "BATCH_SIZE = 32 - the model looks at 32 images, then adjusts itself "
                    "once. Larger batches are faster but need much more memory; 32 is the "
                    "usual safe default and works on a laptop without a graphics card.",
                    "EPOCHS = 10 - how many times the model goes through the entire training "
                    "set. EarlyStopping may cut this short if the model stops improving.",
                    "LEARNING_RATE = 0.0001 - the size of each adjustment, used by the five "
                    "pre-trained models. It is deliberately small so that fine-tuning nudges "
                    "the model rather than overwriting what it already knows.",
                    "EARLY_STOPPING_PATIENCE = 3 - wait three epochs with no improvement "
                    "before stopping. One bad epoch is normal, three in a row is a plateau.",
                    "RANDOM_SEED = 42 - fixes the random number generator. Shuffling and the "
                    "train/val/test split then come out identical every run, so results are "
                    "reproducible. Any number works; 42 is a convention.",
                ],
            },
            {
                "start": "# 4. THE LIST OF MODELS WE WILL TRAIN",
                "title": "Section 4 - the list of six models",
                "explain": [
                    "MODEL_NAMES is the heart of the project's structure: train_all_models.py "
                    "simply loops over this list.",
                    "'CNN_Scratch' is the network built by hand in models.py.",
                    "The other five names - VGG16, ResNet50, MobileNet, InceptionV3 and "
                    "EfficientNetB0 - are the pre-trained models required by the brief.",
                    "To add a seventh model you add one name here and one line to the "
                    "PRETRAINED_MODELS dictionary in models.py. Nothing else changes. That is "
                    "the benefit of driving the program from a list instead of from six "
                    "copy-pasted blocks of code.",
                ],
            },
            {
                "start": "# 5. A SMALL HELPER",
                "title": "Section 5 - creating the output folders",
                "explain": [
                    "create_output_folders() is the one function in this file.",
                    "The for loop walks through the four output folders.",
                    "os.makedirs(folder, exist_ok=True) creates a folder including any "
                    "missing parent folders. exist_ok=True means 'do not raise an error if it "
                    "is already there', so the function is safe to call on every run.",
                    "train_all_models.py calls this once at the start, so a freshly cloned "
                    "copy of the repository works immediately even though git does not store "
                    "empty folders.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "src/data_loader.py",
        "role": "Reads and augments the images",
        "purpose": (
            "This file turns folders full of JPEG files into something a neural network can "
            "consume. It never loads the whole dataset into memory - that would need many "
            "gigabytes of RAM. Instead it builds three generators, which read images off the "
            "disk in batches of 32, resize them, rescale their pixels, and (for training "
            "only) randomly distort them so the model sees a slightly different picture "
            "every time."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header and the folder layout",
                "explain": [
                    "The docstring draws the folder layout the code depends on, because "
                    "getting it wrong is the number one reason this project fails to run.",
                    "The key idea: the FOLDER NAME is the label. A file inside "
                    "data/train/shrimp/ is a picture of a shrimp. Keras reads the folder "
                    "names itself, so the species list is never typed by hand and can never "
                    "fall out of step with the data.",
                ],
            },
            {
                "start": "from tensorflow.keras.preprocessing.image import ImageDataGenerator",
                "title": "Imports",
                "explain": [
                    "ImageDataGenerator is the Keras class that reads images from folders and "
                    "applies augmentation. The project brief names it specifically.",
                    "'from src import config' pulls in the settings file. Because the import "
                    "is written this way, the code must be run from the project folder - "
                    "which is exactly how the README tells you to run it.",
                ],
            },
            {
                "start": "def create_data_generators():",
                "title": "The main function and its docstring",
                "explain": [
                    "create_data_generators() takes no arguments: everything it needs comes "
                    "from config.py, so there is only one source of truth.",
                    "The docstring explains the conveyor-belt idea. A generator yields one "
                    "batch at a time, so memory use stays flat no matter how big the dataset "
                    "is.",
                    "It returns three generators: train, validation and test.",
                ],
            },
            {
                "start": "train_datagen = ImageDataGenerator(",
                "title": "The training generator - with augmentation",
                "explain": [
                    "rescale=1.0 / 255 divides every pixel by 255, turning the range 0-255 "
                    "into 0.0-1.0. This single line is the 'rescale images to [0,1] range' "
                    "requirement from the brief.",
                    "rotation_range=20 rotates the image by a random angle up to 20 degrees "
                    "in either direction - a fish photographed at a slight tilt.",
                    "zoom_range=0.2 randomly zooms in or out by up to 20% - a fish closer to "
                    "or further from the camera.",
                    "width_shift_range=0.2 and height_shift_range=0.2 slide the image "
                    "sideways and up or down by up to 20% - the fish is not always centred.",
                    "shear_range=0.2 slants the image, as if photographed from an angle.",
                    "horizontal_flip=True mirrors the image left to right. A fish facing left "
                    "is still the same species, so this is a safe doubling of the data. Note "
                    "that vertical_flip is deliberately NOT used: an upside-down fish is "
                    "unnatural and would teach the model nothing useful.",
                    "fill_mode=\"nearest\" decides what to put in the corners left empty by a "
                    "rotation or shift: it copies the nearest real pixel, which is the least "
                    "distracting option.",
                    "Important: these transformations are applied randomly and on the fly. "
                    "The files on disk are never changed, and the model sees a different "
                    "version of each image in every epoch.",
                ],
            },
            {
                "start": "val_test_datagen = ImageDataGenerator(rescale=1.0 / 255)",
                "title": "The validation and test generator - no augmentation",
                "explain": [
                    "Only rescale is applied here - no rotation, no zoom, no flipping.",
                    "This is a rule, not a preference. Augmenting validation or test images "
                    "would mean measuring the model on distorted pictures, and the reported "
                    "accuracy would not describe how it performs on real photographs.",
                    "The same generator object is reused for both validation and test, "
                    "because they need identical treatment.",
                ],
            },
            {
                "start": "train_generator = train_datagen.flow_from_directory(",
                "title": "Pointing each generator at its folder",
                "explain": [
                    "flow_from_directory() is the method that walks a folder, finds the "
                    "subfolders, treats each subfolder name as a class, and starts producing "
                    "batches. When it runs it prints a line such as 'Found 6250 images "
                    "belonging to 11 classes.'",
                    "config.TRAIN_DIR tells it which folder to read.",
                    "target_size=config.IMAGE_SIZE resizes every image to 224x224 as it is "
                    "loaded, so photos of any original size can be mixed together.",
                    "batch_size=config.BATCH_SIZE hands out 32 images per batch.",
                    "class_mode=\"categorical\" produces one-hot labels - for 11 species, "
                    "class 2 becomes [0,0,1,0,0,0,0,0,0,0,0]. This is what pairs with the "
                    "softmax output layer and the categorical_crossentropy loss.",
                    "shuffle=True mixes the training images. Without it the model would see "
                    "every image of species 1, then every image of species 2, and learn very "
                    "badly.",
                    "seed=config.RANDOM_SEED makes that shuffle repeatable.",
                    "The validation generator repeats the same settings but with "
                    "shuffle=False, because there is nothing to gain from shuffling data you "
                    "are only measuring.",
                    "The test generator also uses shuffle=False, and here it is critical: "
                    "evaluate.py compares the model's predictions against "
                    "test_generator.classes, which is in folder order. If the generator "
                    "shuffled, predictions and labels would be lined up wrongly and the "
                    "accuracy would be nonsense.",
                    "The three generators are returned together as a tuple.",
                ],
            },
            {
                "start": "def get_class_names(generator):",
                "title": "Getting the species names in model order",
                "explain": [
                    "generator.class_indices is a dictionary built by Keras, for example "
                    "{'shrimp': 0, 'trout': 1}.",
                    "The model's output is a list of numbers, so to turn position 0 back into "
                    "the word 'shrimp' the dictionary must be flipped into a list.",
                    "sorted(generator.class_indices, key=generator.class_indices.get) sorts "
                    "the dictionary's keys by their value - that is, by 0, 1, 2 ... - "
                    "producing ['shrimp', 'trout'].",
                    "This list is saved to models/class_names.json and read back by the "
                    "Streamlit app, which guarantees the app labels predictions exactly the "
                    "way the model was trained.",
                ],
            },
            {
                "start": "def count_images(generator):",
                "title": "A one-line helper",
                "explain": [
                    "generator.samples is the total number of images the generator found.",
                    "Wrapping it in a named function makes the calling code read as English "
                    "and gives one place to change if the counting ever needs to be smarter.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "src/models.py",
        "role": "Builds all six architectures",
        "purpose": (
            "This file describes the shape of every model, and nothing else - it builds them "
            "and compiles them, but never trains them. Keeping 'what the model looks like' "
            "apart from 'how the model is trained' means you can change an architecture "
            "without touching the training loop, and vice versa."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "States the one responsibility of this file and the two kinds of model it "
                    "produces: one built by hand, five borrowed and adapted.",
                ],
            },
            {
                "start": "from tensorflow.keras import layers, models, optimizers",
                "title": "Imports",
                "explain": [
                    "layers gives the building blocks: Conv2D, MaxPooling2D, Dense, Dropout "
                    "and so on.",
                    "models gives Sequential, the container that stacks layers in a line.",
                    "optimizers gives Adam, the algorithm that decides how to adjust the "
                    "model after each batch.",
                    "The five names imported from tensorflow.keras.applications are the "
                    "pre-trained architectures. Importing them does not download anything - "
                    "the weights are fetched later, the first time a model is built, and are "
                    "then cached in your home folder.",
                ],
            },
            {
                "start": "def build_cnn_from_scratch(num_classes):",
                "title": "The from-scratch CNN - the idea",
                "explain": [
                    "num_classes is passed in rather than read from config, because the number "
                    "of species is discovered from the data at run time.",
                    "The docstring explains the pattern the layers follow: each Conv2D looks "
                    "for patterns, each MaxPooling2D shrinks the image so the next Conv2D "
                    "sees a wider area for the same cost.",
                ],
            },
            {
                "start": 'model = models.Sequential(name="CNN_Scratch")',
                "title": "Stacking the layers",
                "explain": [
                    "Sequential means the layers run strictly one after another, each feeding "
                    "the next. The name is used later in printouts and file names.",
                    "layers.Input(shape=config.INPUT_SHAPE) declares that each image arrives "
                    "as 224x224x3. Declaring the input explicitly lets model.summary() print "
                    "the shapes immediately.",
                    "Conv2D(32, (3, 3), activation=\"relu\", padding=\"same\") slides 32 "
                    "different 3x3 windows over the image. Each window learns to react to one "
                    "kind of pattern. 'relu' turns any negative result into zero, which is "
                    "what lets the network learn non-linear things. padding=\"same\" keeps "
                    "the width and height unchanged so only pooling shrinks the image.",
                    "MaxPooling2D((2, 2)) keeps only the largest value in each 2x2 square, "
                    "halving width and height: 224 becomes 112.",
                    "The second block uses 64 filters and halves again, 112 to 56. The number "
                    "of filters grows as the image shrinks - a standard CNN design, because "
                    "later layers need to recognise more kinds of pattern but each one covers "
                    "a smaller grid.",
                    "The third block uses 128 filters: 56 becomes 28.",
                    "The fourth block uses 128 filters again: 28 becomes 14. The output at "
                    "this point is a 14x14x128 block of numbers.",
                    "Flatten() unrolls that block into one long list of 14 x 14 x 128 = 25088 "
                    "numbers, because Dense layers can only accept a flat list.",
                    "Dense(256, activation=\"relu\") is a fully connected layer: all 25088 "
                    "numbers feed all 256 neurons. This is where the patterns found by the "
                    "convolutions get combined into a decision.",
                    "Dropout(0.5) randomly switches off half the neurons on every training "
                    "step. The model cannot lean on any single neuron, so it is forced to "
                    "learn redundant, general features. Dropout is active during training "
                    "only; at prediction time all neurons are used.",
                    "Dense(num_classes, activation=\"softmax\") is the output: one neuron per "
                    "species, and softmax converts the numbers into probabilities summing to "
                    "1.0.",
                ],
            },
            {
                "start": "model.compile(",
                "title": "Compiling the from-scratch CNN",
                "explain": [
                    "Compiling attaches the three things the model needs in order to learn.",
                    "optimizer=optimizers.Adam(learning_rate=0.001) - Adam adapts the step "
                    "size per weight and is the standard first choice. 0.001 is Adam's usual "
                    "default and is appropriate here because this model starts from random "
                    "weights and has everything to learn.",
                    "loss=\"categorical_crossentropy\" - the loss is the number the model "
                    "tries to make smaller. This particular loss is the correct partner for "
                    "softmax plus one-hot labels in a multi-class problem.",
                    "metrics=[\"accuracy\"] - accuracy is not used for learning, only "
                    "reported, so that the progress bar means something to a human.",
                    "The compiled model is returned, ready for train.py to fit.",
                ],
            },
            {
                "start": "PRETRAINED_MODELS = {",
                "title": "The lookup table of pre-trained models",
                "explain": [
                    "This dictionary maps a name to the Keras function that builds that "
                    "architecture. Note that the values are the functions themselves, not "
                    "calls to them - there are no brackets after VGG16.",
                    "Because of this table, one build_pretrained_model() function handles all "
                    "five models instead of five near-identical functions. That is the "
                    "'code reusability / modular programming' the project is marked on.",
                ],
            },
            {
                "start": "def build_pretrained_model(model_name, num_classes):",
                "title": "Transfer learning - the idea",
                "explain": [
                    "The docstring explains why transfer learning works: the model already "
                    "knows edges, textures and shapes from ImageNet, so it only needs to "
                    "learn which combinations mean which fish.",
                    "base_model_function = PRETRAINED_MODELS[model_name] looks up the builder "
                    "for the requested name. If the name is not in the dictionary this raises "
                    "a KeyError, which build_model() below turns into a friendly message.",
                ],
            },
            {
                "start": "base_model = base_model_function(",
                "title": "Loading and freezing the pre-trained base",
                "explain": [
                    "weights=\"imagenet\" downloads the weights learned from 1.2 million "
                    "ImageNet photographs. The download happens once and is cached in "
                    "~/.keras/models, so later runs are instant.",
                    "include_top=False throws away the original 1000-category output layer. "
                    "We do not want to know whether the photo is a goldfish or a teapot - we "
                    "want our own fish species, so we attach our own output layer instead.",
                    "input_shape=config.INPUT_SHAPE tells it to expect 224x224x3 images.",
                    "base_model.trainable = False freezes every layer in the borrowed model. "
                    "Frozen layers are not updated during training, which does two things: it "
                    "makes each epoch much faster (only the new layers are learning), and it "
                    "protects the ImageNet knowledge from being destroyed by large early "
                    "gradients coming from a randomly-initialised head.",
                ],
            },
            {
                "start": "model = models.Sequential(name=model_name)",
                "title": "Attaching our own classifier head",
                "explain": [
                    "A new Sequential model is started, named after the architecture so that "
                    "saved files and printouts are self-explanatory.",
                    "layers.Input declares the 224x224x3 input again for the outer model.",
                    "The 'if model_name == \"EfficientNetB0\"' block handles a genuine trap. "
                    "EfficientNet contains its own normalisation and expects pixels in the "
                    "0-255 range, but our generator has already divided by 255. "
                    "layers.Rescaling(255.0) multiplies them back up. Without this one line "
                    "EfficientNetB0 scores close to random and looks broken - this is the "
                    "single most common bug in projects that use it.",
                    "model.add(base_model) inserts the entire frozen pre-trained network as "
                    "if it were a single layer.",
                    "GlobalAveragePooling2D() takes the average of each feature map, turning "
                    "a block such as 7x7x1280 into a flat list of 1280 numbers. It is used "
                    "instead of Flatten() because it produces far fewer numbers, which means "
                    "far fewer weights in the next layer and much less overfitting.",
                    "Dense(256, activation=\"relu\") is our own thinking layer - the first "
                    "layer in the whole stack that knows anything about fish.",
                    "Dropout(0.3) is gentler than the 0.5 used in the from-scratch CNN, "
                    "because there are fewer trainable weights here and therefore less risk "
                    "of memorising.",
                    "Dense(num_classes, activation=\"softmax\") produces the species "
                    "probabilities.",
                    "model.compile uses config.LEARNING_RATE, which is 0.0001 - ten times "
                    "smaller than the from-scratch CNN's rate. Small steps are the whole "
                    "point of fine-tuning: we are adjusting a good model, not building one.",
                ],
            },
            {
                "start": "def build_model(model_name, num_classes):",
                "title": "One door into this file",
                "explain": [
                    "build_model() is the only function the rest of the project calls. The "
                    "caller passes a name and gets a compiled model, and does not need to "
                    "know whether it was built by hand or borrowed.",
                    "If the name is 'CNN_Scratch', build_cnn_from_scratch() is used.",
                    "If the name is in the PRETRAINED_MODELS dictionary, "
                    "build_pretrained_model() is used.",
                    "Otherwise a ValueError is raised that prints the misspelled name and the "
                    "list of valid names. Failing loudly with a helpful message is far better "
                    "than failing deep inside Keras twenty minutes into a training run.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "src/train.py",
        "role": "Trains one model and saves it",
        "purpose": (
            "This file trains exactly one model. It deliberately does not know that there are "
            "six of them - the loop lives in train_all_models.py. Keeping 'train one thing "
            "well' separate from 'do it six times' means you can train a single model for "
            "debugging without touching any other code."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Explains the one-model scope and points the reader at "
                    "train_all_models.py for the loop.",
                ],
            },
            {
                "start": "import json",
                "title": "Imports",
                "explain": [
                    "json is used to save the training history so the graphs can be redrawn "
                    "later without retraining anything.",
                    "os builds the output file paths; time measures how long training takes, "
                    "which goes into the comparison report.",
                    "EarlyStopping and ModelCheckpoint are callbacks - small objects Keras "
                    "runs automatically at the end of every epoch.",
                    "The three 'from src import ...' lines bring in the settings, the data "
                    "loader and the model builder. models is imported 'as model_builder' to "
                    "avoid confusion with the Keras module of the same name.",
                ],
            },
            {
                "start": "def train_one_model(model_name, train_generator, val_generator):",
                "title": "The function signature",
                "explain": [
                    "The generators are passed IN rather than created here. They are built "
                    "once in train_all_models.py and reused for all six models, which saves "
                    "scanning the folders six times and guarantees every model is trained on "
                    "exactly the same data.",
                    "The function returns three things: the history dictionary, the path the "
                    "model was saved to, and how many minutes it took.",
                ],
            },
            {
                "start": "num_classes = train_generator.num_classes",
                "title": "Building the model",
                "explain": [
                    "num_classes is read from the generator, which counted the folders. The "
                    "number of species is never hard-coded anywhere in the project, so the "
                    "same code works on a dataset with 9 species or 11.",
                    "model_builder.build_model(model_name, num_classes) returns a compiled "
                    "model - see models.py.",
                    "model.summary() prints a table of every layer, its output shape and its "
                    "parameter count. For the pre-trained models this is where you can see "
                    "'Non-trainable params' is a very large number, which proves the base is "
                    "frozen. It is worth showing in a demo video.",
                    "model_path builds the save location, for example models/MobileNet.h5. "
                    "The .h5 extension is the format the project brief asks for.",
                ],
            },
            {
                "start": "early_stopping = EarlyStopping(",
                "title": "Callback 1 - EarlyStopping",
                "explain": [
                    "monitor=\"val_accuracy\" - watch accuracy on the validation set, not on "
                    "the training set. Training accuracy almost always keeps rising, so "
                    "watching it would never trigger a stop.",
                    "patience=config.EARLY_STOPPING_PATIENCE waits three epochs with no new "
                    "best score before stopping. This tolerates the normal bumpiness of "
                    "training while still catching a real plateau.",
                    "restore_best_weights=True rewinds the model to its best epoch. Without "
                    "it you would keep the final, slightly worse version.",
                    "verbose=1 prints a message when it fires, so the log explains why "
                    "training ended early.",
                ],
            },
            {
                "start": "checkpoint = ModelCheckpoint(",
                "title": "Callback 2 - ModelCheckpoint",
                "explain": [
                    "filepath=model_path is where the .h5 file is written.",
                    "monitor=\"val_accuracy\" with save_best_only=True means the file is "
                    "overwritten only when the model beats its own record. The file on disk "
                    "is therefore always the best version seen so far, not the latest.",
                    "This is real insurance: if the machine crashes during epoch 9 of a long "
                    "run, the best model up to epoch 8 is already safely on disk.",
                ],
            },
            {
                "start": "history = model.fit(",
                "title": "The training itself",
                "explain": [
                    "start_time = time.time() records the clock before training starts; the "
                    "difference afterwards gives the duration.",
                    "model.fit() is the line that actually trains. Everything before it was "
                    "preparation.",
                    "The first argument, train_generator, supplies batches to learn from. "
                    "Keras knows the epoch has ended when the generator has produced every "
                    "image once.",
                    "validation_data=val_generator is run at the end of every epoch, on "
                    "un-augmented images, and produces val_accuracy and val_loss.",
                    "epochs=config.EPOCHS sets the maximum; EarlyStopping may end it sooner.",
                    "callbacks=[early_stopping, checkpoint] hands Keras the two helpers.",
                    "verbose=1 prints the familiar progress bar with live loss and accuracy.",
                    "train_minutes converts the elapsed seconds into minutes, which is "
                    "reported in the comparison table - a genuinely useful column, because a "
                    "model that is 1% better but takes ten times longer may be the wrong "
                    "choice.",
                ],
            },
            {
                "start": "history_dict = history.history",
                "title": "Saving the training history",
                "explain": [
                    "model.fit() returns a History object; history.history is a plain "
                    "dictionary such as {'accuracy': [...], 'val_accuracy': [...], 'loss': "
                    "[...], 'val_loss': [...]}, with one number per epoch.",
                    "The dictionary is written to outputs/reports/<model>_history.json with "
                    "indent=2 so a human can read it.",
                    "Saving it matters: redrawing a graph later costs milliseconds, "
                    "retraining to recover the numbers would cost hours.",
                    "The function returns the history, the model path and the duration.",
                ],
            },
            {
                "start": "def load_data():",
                "title": "A convenience wrapper",
                "explain": [
                    "Calls data_loader.create_data_generators() and "
                    "data_loader.get_class_names() together, and returns all four results.",
                    "It exists so that train_all_models.py has a single short line to get "
                    "everything it needs, instead of repeating two calls.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "src/evaluate.py",
        "role": "Scores a trained model",
        "purpose": (
            "This file gives a trained model its final exam. It loads the saved .h5 file "
            "back from disk, predicts on the test images - pictures the model has never seen "
            "and that were never used for any decision - and produces the four metrics, a "
            "per-species report and a confusion matrix. Loading from disk rather than reusing "
            "the model in memory is deliberate: it proves the saved file actually works, "
            "which is exactly what the Streamlit app will later rely on."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Defines the four metrics in plain English. Precision and recall are the "
                    "two most commonly confused, so they are stated as questions: 'when it "
                    "says shrimp, how often is it right?' versus 'of all the shrimp, how many "
                    "did it find?'",
                ],
            },
            {
                "start": "import os",
                "title": "Imports",
                "explain": [
                    "matplotlib.use(\"Agg\") must be called BEFORE pyplot is imported. 'Agg' "
                    "is a backend that draws into files instead of opening a window. Without "
                    "it, running on a server with no screen crashes, and on a laptop a window "
                    "would pop up and block the script until closed.",
                    "seaborn draws the confusion matrix heatmap - it is matplotlib with "
                    "nicer defaults.",
                    "The six functions imported from sklearn.metrics do all the scoring. "
                    "Using the standard library rather than hand-written formulas means the "
                    "numbers are trustworthy and the code is short.",
                    "load_model reads a .h5 file back into a working Keras model.",
                ],
            },
            {
                "start": "def evaluate_model(model_path, test_generator, class_names, model_name):",
                "title": "The function signature",
                "explain": [
                    "model_path is the .h5 file to test; test_generator supplies the images; "
                    "class_names labels the rows and columns of the report; model_name is "
                    "used in titles and file names.",
                    "It returns a dictionary of scores, which train_all_models.py collects "
                    "into the comparison table.",
                ],
            },
            {
                "start": "model = load_model(model_path)",
                "title": "Predicting on the test set",
                "explain": [
                    "load_model(model_path) rebuilds the whole model - architecture, weights "
                    "and compilation settings - from the single .h5 file.",
                    "test_generator.reset() rewinds the conveyor belt to the first image. "
                    "Without it, a generator that has already been partly consumed would "
                    "start somewhere in the middle and every label would be misaligned.",
                    "model.predict(test_generator) returns an array with one row per image "
                    "and one column per species, each row holding softmax probabilities.",
                    "np.argmax(predicted_probabilities, axis=1) takes the position of the "
                    "largest probability in each row. axis=1 means 'along each row'. The "
                    "result is the predicted class number for every test image.",
                    "y_true = test_generator.classes is the list of correct answers, in "
                    "folder order. This line is only correct because shuffle=False was set "
                    "for the test generator in data_loader.py - the single most important "
                    "detail in the whole evaluation.",
                ],
            },
            {
                "start": "accuracy = accuracy_score(y_true, y_predicted)",
                "title": "The four headline metrics",
                "explain": [
                    "accuracy_score counts how many predictions match the truth and divides "
                    "by the total.",
                    "precision_score, recall_score and f1_score all use "
                    "average=\"weighted\", which computes the metric for each species "
                    "separately and then averages them, weighting each species by how many "
                    "images it has. This is the right choice when some species have far more "
                    "photographs than others.",
                    "zero_division=0 tells scikit-learn to report 0 instead of crashing if a "
                    "species was never predicted at all - which does happen with a weak "
                    "model, and should not stop the whole run.",
                    "The four numbers are printed with four decimal places using the "
                    "f-string format specifier {value:.4f}.",
                ],
            },
            {
                "start": "report_text = classification_report(",
                "title": "The per-species report",
                "explain": [
                    "classification_report produces a text table with precision, recall, "
                    "F1-score and support (the number of images) for every species "
                    "individually.",
                    "target_names=class_names replaces the numbers 0, 1, 2 with real species "
                    "names, which is what makes the table readable.",
                    "The table is written to outputs/reports/<model>_classification_report.txt "
                    "with a title line and a row of equals signs.",
                    "This per-species view is where the real insight lives: an overall "
                    "accuracy of 95% can still hide one species the model gets wrong almost "
                    "every time.",
                    "save_confusion_matrix(...) is then called to draw the picture version.",
                ],
            },
            {
                "start": "return {",
                "title": "Returning the scores",
                "explain": [
                    "The five values are returned as a dictionary rather than a bare tuple, "
                    "so the calling code reads scores[\"f1_score\"] instead of having to "
                    "remember that F1 was the fourth item.",
                    "A list of these dictionaries is all pandas needs to build the comparison "
                    "table, which is why this shape was chosen.",
                ],
            },
            {
                "start": "def save_confusion_matrix(y_true, y_predicted, class_names, model_name):",
                "title": "The confusion matrix - how to read it",
                "explain": [
                    "The docstring gives the reading rule: each row is the true species, each "
                    "column is what the model guessed, the diagonal is correct answers and "
                    "everything off the diagonal is a mistake.",
                    "A bright square off the diagonal tells you precisely which two species "
                    "the model confuses - far more useful than a single accuracy number.",
                ],
            },
            {
                "start": "matrix = confusion_matrix(y_true, y_predicted)",
                "title": "Drawing and saving the heatmap",
                "explain": [
                    "confusion_matrix() builds the grid of counts.",
                    "plt.figure(figsize=(10, 8)) sets the canvas size in inches, big enough "
                    "that eleven species names still fit.",
                    "sns.heatmap draws it, colouring each square by its value.",
                    "annot=True writes the number inside each square; fmt=\"d\" formats those "
                    "numbers as integers rather than 12.00.",
                    "cmap=\"Blues\" means darker blue equals more images - and because the "
                    "diagonal should be darkest, a good model is visible at a glance.",
                    "xticklabels and yticklabels put the species names on the axes.",
                    "plt.xticks(rotation=45, ha=\"right\") tilts the long species names so "
                    "they do not overlap; ha=\"right\" aligns them neatly under their column.",
                    "plt.tight_layout() recalculates the margins so nothing is cut off - "
                    "without it, rotated labels are usually clipped.",
                    "plt.savefig(save_path, dpi=120) writes the PNG at a resolution sharp "
                    "enough for a report or a slide.",
                    "plt.close() frees the figure. In a loop over six models, forgetting this "
                    "leaks memory and eventually triggers a matplotlib warning.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "src/visualize.py",
        "role": "Every graph in the project",
        "purpose": (
            "All plotting lives in this one file, so the look of the charts can be changed "
            "in a single place and no plotting code is ever repeated. It draws three kinds "
            "of graph: the accuracy and loss curves for one model, the bar chart comparing "
            "all six, and the distribution of images across species."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Names the two main graph types and states the rule that all "
                    "graph-drawing code belongs here.",
                ],
            },
            {
                "start": "import os",
                "title": "Imports",
                "explain": [
                    "matplotlib.use(\"Agg\") again comes before pyplot, for the same reason "
                    "as in evaluate.py: save to a file, never open a window.",
                    "pandas is used to turn the list of score dictionaries into a table that "
                    "can be plotted directly.",
                ],
            },
            {
                "start": "def plot_training_history(history_dict, model_name):",
                "title": "Training curves - what they tell you",
                "explain": [
                    "The docstring gives the diagnostic rule that makes these graphs worth "
                    "drawing: if the training line keeps improving while the validation line "
                    "stalls or worsens, the model is overfitting.",
                    "This is the single most useful picture to have on screen during a live "
                    "project evaluation.",
                ],
            },
            {
                "start": "figure, (left_graph, right_graph) = plt.subplots(1, 2, figsize=(13, 5))",
                "title": "Two graphs side by side",
                "explain": [
                    "plt.subplots(1, 2) creates one row of two graphs and returns the figure "
                    "plus the two axes, which are unpacked into clearly named variables.",
                    "left_graph.plot(history_dict[\"accuracy\"]) draws training accuracy "
                    "against epoch number; the second plot call adds validation accuracy to "
                    "the same axes so the two can be compared directly.",
                    "marker=\"o\" puts a dot on each epoch, which matters when a run stops "
                    "after only three or four epochs and the line would otherwise be too "
                    "short to read.",
                    "set_title, set_xlabel, set_ylabel and legend label the graph. An "
                    "unlabelled graph loses marks in any evaluation.",
                    "grid(True, alpha=0.3) adds faint grid lines; alpha is transparency, so "
                    "0.3 keeps them in the background.",
                    "The right-hand graph repeats all of this for loss instead of accuracy. "
                    "Loss should fall while accuracy rises - if loss starts rising again, "
                    "that is overfitting in its clearest form.",
                ],
            },
            {
                "start": "plt.tight_layout()",
                "title": "Saving the training-history figure",
                "explain": [
                    "tight_layout() fixes the spacing so the two graphs do not overlap.",
                    "The file is saved as outputs/plots/<model>_training_history.png at "
                    "dpi=120.",
                    "plt.close() releases the figure before the next model is plotted.",
                    "The path is printed so the log tells you exactly where the picture went.",
                ],
            },
            {
                "start": "def plot_model_comparison(results_list):",
                "title": "The comparison chart",
                "explain": [
                    "The argument is the list of score dictionaries returned by "
                    "evaluate_model(), one per model.",
                    "This chart is the visual answer to the 'Model Comparison' business use "
                    "case in the brief.",
                ],
            },
            {
                "start": "table = pd.DataFrame(results_list)",
                "title": "Building and drawing the bar chart",
                "explain": [
                    "pd.DataFrame(results_list) turns a list of dictionaries into a table "
                    "automatically, using the dictionary keys as column names.",
                    "sort_values(\"accuracy\", ascending=False) puts the best model on the "
                    "left, so the winner is obvious without reading any numbers.",
                    "set_index(\"model\")[[...]] makes the model name the row label and keeps "
                    "only the four score columns, dropping training_minutes and epochs_run "
                    "which are on a completely different scale and would flatten the chart.",
                    "chart_data.plot(kind=\"bar\") draws four bars per model - one per "
                    "metric.",
                    "plt.ylim(0, 1.05) fixes the y-axis from 0 to just above 1. Without this, "
                    "matplotlib auto-scales and a set of models between 0.90 and 0.95 looks "
                    "dramatically different when the real gap is tiny. Fixing the axis is an "
                    "honesty measure.",
                    "xticks(rotation=30, ha=\"right\") tilts the model names so they fit.",
                    "The PNG is saved to outputs/plots/model_comparison.png, the figure is "
                    "closed, and the sorted table is returned so the caller can print it.",
                ],
            },
            {
                "start": "def plot_class_distribution(generator, class_names, title, file_name):",
                "title": "The class distribution chart",
                "explain": [
                    "generator.classes is a long list such as [0,0,0,1,1,2,2,2,...], one "
                    "entry per image.",
                    "pd.Series(...).value_counts() counts how many times each class number "
                    "appears; .sort_index() puts them back in class order so they line up "
                    "with class_names.",
                    "plt.bar(class_names, counts.values) draws one bar per species.",
                    "This chart answers a question every evaluator asks: is the dataset "
                    "balanced? If one species has ten times more images than another, that "
                    "explains a weak recall score and justifies quoting the weighted F1 "
                    "rather than plain accuracy.",
                    "The title and file name are passed in as arguments, so the same function "
                    "can also chart the test set later without any new code.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "prepare_dataset.py",
        "role": "Step 1 - arrange the downloaded images",
        "purpose": (
            "Run this once, before training. Downloaded datasets arrive in inconsistent "
            "shapes: sometimes already split into train/test, sometimes as a plain set of "
            "species folders, and almost always wrapped in one or two extra folders created "
            "by the zip. This script works out which case it is looking at and produces the "
            "exact data/train, data/val, data/test layout the rest of the project expects."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Shows the command to run, including the --source argument, and lists the "
                    "three cases the script handles.",
                ],
            },
            {
                "start": "import argparse",
                "title": "Imports and constants",
                "explain": [
                    "argparse reads options typed after the command, such as --source.",
                    "random is used to shuffle before splitting; shutil copies files and "
                    "whole folder trees.",
                    "IMAGE_EXTENSIONS lists the file types counted as images. Anything else - "
                    "a README, a .csv, a hidden system file - is ignored, which stops junk "
                    "files being treated as photographs.",
                    "TRAIN_SHARE = 0.70 and VAL_SHARE = 0.15 define the split; the remaining "
                    "15% becomes the test set. 70/15/15 is a standard choice for a dataset of "
                    "this size.",
                ],
            },
            {
                "start": "def list_images(folder):",
                "title": "Two tiny listing helpers",
                "explain": [
                    "list_images() walks one folder and keeps the file names ending in an "
                    "image extension. file_name.lower() means .JPG and .jpg both match.",
                    "list_subfolders() keeps only entries that are folders, using "
                    "os.path.isdir(), and returns them sorted so the class order is the same "
                    "on every machine and every run.",
                    "Both are two or three lines long and are used repeatedly below. Writing "
                    "them once is what keeps the rest of the file readable.",
                ],
            },
            {
                "start": "def find_dataset_root(start_folder):",
                "title": "Stepping down through wrapper folders",
                "explain": [
                    "Zip files commonly unpack as extracted/Dataset/Dataset/train/..., with "
                    "one or two pointless wrapper folders. This function finds the folder "
                    "that actually holds the data.",
                    "The while True loop repeats until it decides to return.",
                    "If the current folder holds exactly one subfolder and no images at all, "
                    "it must be a wrapper, so the code steps into that single subfolder and "
                    "checks again.",
                    "As soon as the folder holds several subfolders (the species) or some "
                    "images, it is the real root and is returned.",
                    "This one function removes the most common cause of 'Found 0 images "
                    "belonging to 0 classes', which otherwise stops beginners for hours.",
                ],
            },
            {
                "start": "def copy_split_folders(source_root):",
                "title": "Case A - the dataset is already split",
                "explain": [
                    "name_map translates the many names datasets use - train, training, val, "
                    "valid, validation, test, testing - into the three folders this project "
                    "wants.",
                    "The loop goes through each subfolder of the source and looks its "
                    "lower-cased name up in the map.",
                    "name_map.get(...) returns None for an unrecognised folder, and the "
                    "'continue' statement skips it rather than crashing.",
                    "If the target folder already exists it is deleted with shutil.rmtree "
                    "first, so running the script twice gives a clean result instead of "
                    "mixing old and new files.",
                    "shutil.copytree copies the whole folder tree, species subfolders and "
                    "all, in one call.",
                ],
            },
            {
                "start": "def split_class_folders(source_root):",
                "title": "Case B - splitting it ourselves",
                "explain": [
                    "Used when the dataset is just species folders with no train/test "
                    "division.",
                    "random.seed(config.RANDOM_SEED) makes the shuffle repeatable, so the "
                    "same images land in the test set every time you run the script. Without "
                    "this your accuracy would change slightly on every rerun for no real "
                    "reason.",
                    "For each species, list_images() collects the file names and "
                    "random.shuffle() mixes them. Shuffling before splitting matters because "
                    "files are often named in capture order, and an unshuffled split could "
                    "put one whole photo session into the test set.",
                    "A species folder with no images prints a skip message instead of "
                    "crashing on a division by zero.",
                    "train_cut = int(total * 0.70) and val_cut = int(total * 0.85) are the "
                    "two positions where the shuffled list is cut.",
                    "The slices image_names[:train_cut], image_names[train_cut:val_cut] and "
                    "image_names[val_cut:] produce the three groups with no overlap and no "
                    "image left out - a guarantee of Python slicing itself.",
                    "The groups dictionary maps each target folder to its list of file names, "
                    "so one loop copies all three.",
                    "os.makedirs(target_folder, exist_ok=True) creates data/train/<species>, "
                    "and shutil.copyfile copies each image. Copying rather than moving leaves "
                    "the original download untouched, so a mistake is never destructive.",
                    "One summary line per species is printed as it goes.",
                ],
            },
            {
                "start": "def print_summary():",
                "title": "Printing the final counts",
                "explain": [
                    "Walks train, val and test in turn and counts the images in each species "
                    "folder.",
                    "A missing split is reported as MISSING rather than crashing.",
                    "f\"{species:<35} {count:>6}\" is f-string alignment: <35 pads the name to "
                    "35 characters on the left, >6 right-aligns the number in 6 characters. "
                    "The result is a neat column layout.",
                    "This printout is the first thing to check before training. If a species "
                    "shows 0 images, stop and fix it now rather than after an hour of "
                    "training.",
                ],
            },
            {
                "start": "def main():",
                "title": "Tying it together",
                "explain": [
                    "argparse.ArgumentParser builds the command-line reader; "
                    "required=True means the script refuses to run without --source.",
                    "If the given folder does not exist, SystemExit prints a clear message and "
                    "stops - far friendlier than a traceback.",
                    "os.makedirs(config.DATA_DIR, exist_ok=True) makes sure data/ exists.",
                    "find_dataset_root() steps past any wrapper folders and the real path is "
                    "printed, so you can confirm it found the right place.",
                    "inside holds the lower-cased names of the subfolders; "
                    "already_split checks whether 'train' or 'training' is among them.",
                    "Depending on that answer, either copy_split_folders() or "
                    "split_class_folders() runs.",
                    "The next block handles a common half-way case: a dataset with train and "
                    "test but no validation folder. Rather than stopping, it copies test into "
                    "val so training can proceed. This is a documented compromise, not ideal "
                    "practice - with a validation set identical to the test set, the "
                    "EarlyStopping decision is made using the same images you later report "
                    "scores on.",
                    "print_summary() shows the result and the final line tells you the next "
                    "command to run.",
                    "if __name__ == \"__main__\": main() means the code runs when you execute "
                    "the file directly, but not if another file imports it.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "train_all_models.py",
        "role": "Step 2 - the main script",
        "purpose": (
            "This is the script that runs the project. It loads the data once, loops over "
            "the six model names in config.MODEL_NAMES, and for each one trains it, draws "
            "its graphs, evaluates it and records its scores. At the end it compares "
            "everything, announces the winner and copies that model to best_model.h5 for the "
            "web app to use."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Lists the six steps the script performs and shows both ways to run it: "
                    "all six models, or a single named model for quick testing.",
                ],
            },
            {
                "start": "import argparse",
                "title": "Imports",
                "explain": [
                    "shutil is used once, at the very end, to copy the winning model to "
                    "best_model.h5.",
                    "json saves the class-name list that the Streamlit app reads.",
                    "The four 'from src import ...' lines bring in the project's own modules. "
                    "Notice how short this script can be precisely because the real work "
                    "lives in src/.",
                ],
            },
            {
                "start": "def main():",
                "title": "The entry point",
                "explain": [
                    "All of the script's work is inside main() rather than at the top level "
                    "of the file. That keeps the file importable and is standard Python "
                    "practice.",
                ],
            },
            {
                "start": 'parser = argparse.ArgumentParser(description="Train fish classification models")',
                "title": "Reading the command line",
                "explain": [
                    "--model defaults to \"all\". Passing --model MobileNet trains just that "
                    "one, which is how you check everything works before committing to a long "
                    "run.",
                    "--epochs defaults to None, meaning 'use the value in config.py'. "
                    "type=int makes argparse convert the text to a number.",
                    "If --epochs was given, config.EPOCHS is overwritten. Because every other "
                    "module reads config.EPOCHS at the moment it is used, that one assignment "
                    "changes the behaviour of the whole program.",
                    "The if/else turns the --model value into a list: either all six names or "
                    "a list containing one name. From this point on the code is identical for "
                    "both cases, which is why there is no duplicated branch below.",
                    "config.create_output_folders() makes sure models/ and outputs/ exist "
                    "before anything tries to write into them.",
                ],
            },
            {
                "start": 'print("\\nLoading the fish images ...")',
                "title": "Loading the data once",
                "explain": [
                    "train.load_data() returns the three generators plus the class names. "
                    "This happens ONCE, outside the model loop, so all six models see exactly "
                    "the same images - which is the only way a comparison between them is "
                    "fair.",
                    "The loop with enumerate(class_names) prints each species next to its "
                    "number, so you can see the mapping the model will use.",
                    "The three counts of train, validation and test images are printed. These "
                    "numbers belong in the report.",
                    "The class names are saved to models/class_names.json with "
                    "json.dump(..., indent=2). The Streamlit app reads this file, which is "
                    "what guarantees the app and the model agree on which number means which "
                    "species.",
                    "plot_class_distribution() draws the balance chart before any training "
                    "starts.",
                ],
            },
            {
                "start": "for model_name in models_to_train:",
                "title": "The main loop - six models, one block of code",
                "explain": [
                    "all_results = [] is the empty list that will collect one score "
                    "dictionary per model.",
                    "The loop body is written once and runs for every model. Adding a seventh "
                    "model needs no change here at all.",
                    "train.train_one_model(...) trains it and returns the history, the saved "
                    "path and the duration.",
                    "visualize.plot_training_history(...) draws that model's accuracy and loss "
                    "curves.",
                    "evaluate.evaluate_model(...) loads the saved file back and scores it on "
                    "the test set.",
                    "The training time and the number of epochs actually run are added to the "
                    "scores dictionary. epochs_run comes from len(history_dict[\"accuracy\"]) "
                    "- one entry per completed epoch - which is how you see that EarlyStopping "
                    "cut a model short at, say, 6 of 10 epochs.",
                    "scores is appended to all_results.",
                    "save_results_table(all_results) is called INSIDE the loop, on purpose. "
                    "If the run crashes or you stop it during model five, the CSV already "
                    "holds the results of models one to four. On a multi-hour CPU run this is "
                    "the difference between losing an afternoon and losing nothing.",
                ],
            },
            {
                "start": "if len(all_results) > 1:",
                "title": "Comparing and choosing the winner",
                "explain": [
                    "The comparison chart is only drawn when there is more than one model - "
                    "a bar chart of a single model would be meaningless. With one model a "
                    "plain table is built instead.",
                    "comparison_table.to_string(index=False) prints the table without pandas' "
                    "row numbers, which is cleaner for a screenshot.",
                    "max(all_results, key=lambda row: row[\"accuracy\"]) finds the dictionary "
                    "with the highest accuracy. The lambda is a short anonymous function that "
                    "tells max() which value to compare.",
                    "shutil.copyfile copies that model to models/best_model.h5. The app always "
                    "loads this fixed name, so when a different model wins next time the app "
                    "needs no change whatsoever.",
                    "The winner's name is written to models/best_model_name.txt, so the app "
                    "can display which architecture is answering.",
                ],
            },
            {
                "start": "def save_results_table(all_results):",
                "title": "Writing the comparison CSV",
                "explain": [
                    "pd.DataFrame(all_results) turns the list of dictionaries into a table.",
                    "to_csv(csv_path, index=False) writes outputs/reports/model_comparison.csv "
                    "without the row-number column, so it opens cleanly in Excel.",
                    "This CSV is the 'Comparison Report' listed in the project deliverables.",
                    "The final if __name__ == \"__main__\" guard calls main() when the file is "
                    "run directly.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "make_report.py",
        "role": "Step 2b - the comparison report",
        "purpose": (
            "Turns the raw comparison CSV into the written report the brief asks for: a "
            "readable table plus a handful of insight sentences. Every sentence is "
            "generated from the numbers rather than typed by hand, so the report can never "
            "contradict the results. It also writes the same block into README.md, between "
            "two HTML comment markers, so the repository front page is always up to date."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "States when to run the script - after training - and names the two "
                    "files it writes.",
                ],
            },
            {
                "start": "import json",
                "title": "Imports, paths and markers",
                "explain": [
                    "pandas reads the CSV and formats the Markdown table.",
                    "CSV_PATH, REPORT_PATH and README_PATH are built from config.py, so "
                    "nothing is hard-coded.",
                    "START_MARKER and END_MARKER are the two HTML comments sitting in "
                    "README.md. HTML comments are invisible when GitHub renders the page, "
                    "which makes them perfect anchors for generated content.",
                ],
            },
            {
                "start": "def load_results():",
                "title": "Reading the results",
                "explain": [
                    "If the CSV is missing, SystemExit prints a clear instruction to run "
                    "train_all_models.py first, instead of a confusing pandas error.",
                    "sort_values(\"accuracy\", ascending=False) puts the best model first.",
                    "reset_index(drop=True) renumbers the rows from 0 after the sort, so "
                    "that iloc[0] reliably means 'the best model'. drop=True throws the old "
                    "index away instead of keeping it as a column.",
                ],
            },
            {
                "start": "def make_markdown_table(table):",
                "title": "Formatting the table",
                "explain": [
                    "table.copy() works on a copy, so the original DataFrame is left "
                    "untouched for the insight calculations.",
                    "The loop rounds the four score columns to four decimal places. The "
                    "'if column in pretty.columns' check means the function still works on a "
                    "CSV from a partial run.",
                    "rename() gives the columns human headings - 'F1-score' instead of "
                    "'f1_score'.",
                    "to_markdown(index=False) produces a GitHub-ready Markdown table. This "
                    "needs the small 'tabulate' package, which is listed in "
                    "requirements.txt.",
                ],
            },
            {
                "start": "def write_insights(table):",
                "title": "Generating the insights",
                "explain": [
                    "table.iloc[0] is the first row - the best model - and table.iloc[-1] is "
                    "the last, the weakest. This works because the table was sorted on load.",
                    "The first two sentences state the best and worst models with their "
                    "actual scores.",
                    "gap measures the spread between them, reported both as a fraction and "
                    "as percentage points.",
                    "table[table[\"model\"] == \"CNN_Scratch\"] is boolean filtering: it "
                    "keeps only the rows where the condition is true. This separates the "
                    "from-scratch CNN from the five transfer-learning models.",
                    "transfer_rows[\"accuracy\"].mean() averages the five pre-trained models "
                    "so the report can say whether transfer learning actually helped on THIS "
                    "dataset, rather than assuming it did.",
                    "The if/else covers both outcomes honestly, including the awkward case "
                    "where the from-scratch CNN wins.",
                    "sort_values(\"training_minutes\").iloc[0] finds the fastest model, and "
                    "the following check adds a sentence about the accuracy-versus-time "
                    "trade-off only when the fastest and the most accurate are different "
                    "models.",
                    "The last block lists any model whose epochs_run is below config.EPOCHS, "
                    "which is exactly the set of models EarlyStopping cut short.",
                    "The sentences are joined with newlines and returned as one Markdown "
                    "bullet list.",
                ],
            },
            {
                "start": "def update_readme(results_block):",
                "title": "Updating the README in place",
                "explain": [
                    "If the README or either marker is missing, the function prints a note "
                    "and returns. Generating a report should never destroy a file it does "
                    "not understand.",
                    "text.split(START_MARKER)[0] keeps everything before the opening marker; "
                    "text.split(END_MARKER)[1] keeps everything after the closing one.",
                    "The new text is the two kept pieces with the fresh results block "
                    "between them, so running the script repeatedly replaces the old results "
                    "rather than piling up copies.",
                    "encoding=\"utf-8\" is specified on both the read and the write. On "
                    "Windows the default encoding is not UTF-8, and omitting this is a "
                    "frequent cause of corrupted characters in a README.",
                ],
            },
            {
                "start": "def main():",
                "title": "Putting the report together",
                "explain": [
                    "The table and the insights are joined into one results_block, used "
                    "twice: once in the standalone report, once in the README.",
                    "The report file gets a title, a sentence explaining that all models saw "
                    "identical data, the results block, and a list of where the supporting "
                    "plots and per-species reports live.",
                    "Finally the table is printed to the terminal too, so you can read the "
                    "result without opening a file.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------
    {
        "path": "app.py",
        "role": "Step 3 - the Streamlit web app",
        "purpose": (
            "The deployment half of the project. Streamlit turns a plain Python script into "
            "a web page: there is no HTML, CSS or JavaScript anywhere. The script runs from "
            "top to bottom every time the user interacts with the page, which is why the "
            "expensive model load is cached. The app loads the winning model, accepts an "
            "uploaded photograph, and reports the predicted species with a confidence score "
            "for every class."
        ),
        "blocks": [
            {
                "start": '"""',
                "title": "The file header",
                "explain": [
                    "Gives the launch command - streamlit run app.py, never python app.py - "
                    "and lists what the user sees. Running it with plain python prints a "
                    "warning and produces no web page, which is a very common first mistake.",
                ],
            },
            {
                "start": "import json",
                "title": "Imports and file paths",
                "explain": [
                    "PIL (Pillow) opens the uploaded image; numpy converts it to numbers; "
                    "pandas builds the confidence table.",
                    "load_model reads the saved .h5 file.",
                    "Importing src.config means the app uses exactly the same image size and "
                    "folder paths as training did. If the two ever disagreed, every "
                    "prediction would be wrong in a way that is extremely hard to debug.",
                    "MODEL_PATH, CLASS_NAMES_PATH and BEST_NAME_PATH are the three files "
                    "train_all_models.py produced. This is the entire interface between "
                    "training and deployment: three files on disk.",
                ],
            },
            {
                "start": "st.set_page_config(",
                "title": "Page settings",
                "explain": [
                    "set_page_config must be the first Streamlit command executed in the "
                    "script - calling anything else first raises an error.",
                    "page_title sets the browser tab text, page_icon sets the small tab icon, "
                    "and layout=\"centered\" keeps the content in a readable column rather "
                    "than stretching across a wide monitor.",
                ],
            },
            {
                "start": "@st.cache_resource",
                "title": "Loading the model, once",
                "explain": [
                    "@st.cache_resource is a decorator: it wraps the function so Streamlit "
                    "runs it the first time and then reuses the result. Without it the model "
                    "would be reloaded from disk on every click, adding several seconds to "
                    "every interaction.",
                    "cache_resource is the correct decorator for objects that are not copied, "
                    "such as a model or a database connection; cache_data is for values.",
                    "The function first checks os.path.exists(MODEL_PATH). If training has "
                    "never been run it returns three Nones instead of crashing, and the page "
                    "below turns that into a helpful message.",
                    "load_model(MODEL_PATH) restores the trained network.",
                    "json.load reads class_names.json - the same list, in the same order, "
                    "that the model was trained on.",
                    "best_name is read from the text file if it exists, defaulting to "
                    "\"Unknown\". It is shown in the sidebar so the viewer knows which "
                    "architecture won.",
                ],
            },
            {
                "start": "def prepare_image(uploaded_image):",
                "title": "Preparing the uploaded photo",
                "explain": [
                    "This function is the most important one in the file: the uploaded image "
                    "must be processed in EXACTLY the way the training images were, or the "
                    "predictions will be meaningless.",
                    "convert(\"RGB\") forces three channels. A PNG often has a fourth "
                    "transparency channel and a scanned photo may be greyscale with only one; "
                    "either would make the model reject the input.",
                    "resize(config.IMAGE_SIZE) scales the photo to 224x224 - the same size "
                    "target_size used during training, read from the same constant.",
                    "np.array(image) converts the picture into a numbers array of shape "
                    "(224, 224, 3).",
                    "image_array / 255.0 reproduces ImageDataGenerator(rescale=1./255). "
                    "Forgetting this single line is the classic deployment bug: the app runs, "
                    "returns confident answers, and they are wrong.",
                    "np.expand_dims(image_array, axis=0) adds a batch dimension, turning "
                    "(224, 224, 3) into (1, 224, 224, 3). Keras models always expect a batch, "
                    "even a batch of one.",
                    "Note what is NOT done here: no rotation, zoom or flip. Augmentation is "
                    "for training only.",
                ],
            },
            {
                "start": 'st.title("\N{FISH} Fish Species Classifier")',
                "title": "The page header and the no-model guard",
                "explain": [
                    "st.title and st.write put the heading and the instruction line on the "
                    "page. In Streamlit, writing to the page is just calling a function.",
                    "load_trained_model() is called and its three results unpacked.",
                    "If model is None the app shows a red st.error box explaining that "
                    "train_all_models.py must be run first.",
                    "st.stop() halts the script immediately, so none of the upload code below "
                    "runs. Handling the missing-model case properly is what separates a demo "
                    "that survives a live evaluation from one that shows a traceback.",
                ],
            },
            {
                "start": "with st.sidebar:",
                "title": "The sidebar and the upload box",
                "explain": [
                    "'with st.sidebar:' puts everything indented beneath it into the "
                    "collapsible panel on the left, instead of the main column.",
                    "The sidebar reports which architecture is in use, how many species it "
                    "knows and the input size, then lists every species. This tells the user "
                    "what the model can and cannot recognise - useful, because a model trained "
                    "on 11 species will still confidently name one of those 11 when shown a "
                    "dog.",
                    "st.file_uploader draws the drag-and-drop box. The type=[...] list "
                    "makes the browser reject other file types before they are ever "
                    "uploaded. Note it matches on the file EXTENSION, not the real "
                    "format, so a .jfif file - which is an ordinary JPEG that Windows "
                    "and Chrome sometimes save under that name - was refused until jfif "
                    "was added to the list.",
                    "It returns None until the user actually picks a file, which is what the "
                    "next block tests.",
                ],
            },
            {
                "start": "if uploaded_file is not None:",
                "title": "Making the prediction",
                "explain": [
                    "Everything inside this block only runs once a file has been chosen.",
                    "Image.open(uploaded_file) opens the upload as a picture. Streamlit hands "
                    "over a file-like object, so Pillow can read it directly without saving "
                    "anything to disk.",
                    "st.image(...) shows the user their own photo back, with "
                    "use_container_width=True so it fits the column neatly.",
                    "'with st.spinner(\"Thinking ...\"):' displays an animated message while "
                    "the indented code runs, then removes it. On a CPU a prediction can take "
                    "a second or two, and without a spinner the page looks frozen.",
                    "prepare_image(image) does the resize-and-rescale described above.",
                    "model.predict(image_batch)[0] runs the network. The result is an array "
                    "containing one row, so [0] takes that row: a list of probabilities, one "
                    "per species.",
                ],
            },
            {
                "start": 'st.success(f"### Prediction: {predicted_species}")',
                "title": "Showing the answer",
                "explain": [
                    "np.argmax(probabilities) gives the position of the highest probability; "
                    "int(...) converts it from a numpy integer to a plain Python one so it "
                    "can index the list.",
                    "class_names[best_position] turns that position into the species name - "
                    "the exact reverse of the mapping made in data_loader.get_class_names().",
                    "float(probabilities[best_position]) * 100 turns the probability into a "
                    "percentage.",
                    "st.success draws a green box; the ### inside the f-string is markdown, "
                    "which Streamlit renders as a large heading.",
                    "st.metric shows the confidence as a large, clean number - this is the "
                    "'provide model confidence scores' requirement from the brief.",
                ],
            },
            {
                "start": "scores_table = pd.DataFrame(",
                "title": "Confidence for every species",
                "explain": [
                    "A DataFrame is built with two columns: the species names and their "
                    "probabilities multiplied by 100 and rounded to two decimal places.",
                    "sort_values(\"Confidence (%)\", ascending=False) puts the most likely "
                    "species at the top, so the runner-up is immediately visible. A photo "
                    "where the top two are 51% and 47% is a far less trustworthy answer than "
                    "one at 99%, and showing the whole distribution makes that honest.",
                    "st.bar_chart(scores_table.set_index(\"Species\")) draws an interactive "
                    "bar chart - one line of code, because Streamlit reads the DataFrame's "
                    "index as the labels.",
                    "st.dataframe(..., hide_index=True) prints the exact numbers underneath "
                    "the chart.",
                    "The final else branch shows a blue information box when no file has been "
                    "uploaded yet, so the page is never blank and the user always knows what "
                    "to do next.",
                ],
            },
        ],
    },
]


# ======================================================================
# THE CHAPTERS THAT COME AFTER THE CODE
# ======================================================================

CLOSING_SECTIONS = [
    (
        "Checking the project against the brief",
        [
            "Every requirement from the project document, and where in the code it is met.",

            ("Data preprocessing and augmentation",),
            [
                "'Rescale images to [0,1] range' - rescale=1.0/255 in both generators, "
                "src/data_loader.py.",
                "'Apply data augmentation techniques like rotation, zoom and flipping' - "
                "rotation_range, zoom_range, width_shift_range, height_shift_range, "
                "shear_range and horizontal_flip in train_datagen, src/data_loader.py.",
                "'Loaded using TensorFlow's ImageDataGenerator' - used exactly as specified.",
            ],

            ("Model training",),
            [
                "'Train a CNN model from scratch' - build_cnn_from_scratch() in "
                "src/models.py: four Conv2D + MaxPooling blocks, Flatten, Dense, Dropout, "
                "softmax.",
                "'Experiment with five pre-trained models' - VGG16, ResNet50, MobileNet, "
                "InceptionV3 and EfficientNetB0, all listed in config.MODEL_NAMES and built "
                "by build_pretrained_model().",
                "'Fine-tune the pre-trained models on the fish dataset' - ImageNet weights "
                "loaded, original top removed, base frozen, a new classifier head trained at "
                "a reduced learning rate of 0.0001.",
                "'Save the trained model (max accuracy model) in .h5 or .pkl format' - every "
                "model is saved as models/<name>.h5 by ModelCheckpoint, and the "
                "highest-accuracy one is copied to models/best_model.h5 at the end of "
                "train_all_models.py.",
            ],

            ("Model evaluation",),
            [
                "'Compare accuracy, precision, recall, F1-score and confusion matrix across "
                "all models' - evaluate_model() computes all four metrics plus a "
                "per-species classification report, and save_confusion_matrix() draws the "
                "matrix for every model.",
                "'Visualize training history (accuracy and loss) for each model' - "
                "plot_training_history() writes "
                "outputs/plots/<model>_training_history.png for each of the six.",
            ],

            ("Deployment",),
            [
                "'Allow users to upload fish images' - st.file_uploader in app.py.",
                "'Predict and display the fish category' - st.success with the predicted "
                "species name.",
                "'Provide model confidence scores' - st.metric for the top class plus a bar "
                "chart and table of the confidence for every species.",
            ],

            ("Documentation and deliverables",),
            [
                "'Trained models in .h5 or .pkl format' - models/*.h5.",
                "'Streamlit application' - app.py.",
                "'Python scripts for training, evaluation and deployment' - "
                "train_all_models.py, src/train.py, src/evaluate.py, app.py.",
                "'Comparison report: metrics and insights from all models' - "
                "outputs/reports/model_comparison.csv, the per-model classification reports "
                "and outputs/plots/model_comparison.png.",
                "'GitHub repository with a detailed README' - README.md documents the "
                "problem, the structure, the full workflow and every command.",
                "'Follow coding standards, consistent naming, modular code' - snake_case "
                "throughout, a docstring on every module and function, settings centralised "
                "in config.py and all reusable logic in src/.",
                "Two deliverables are yours to complete outside the code: push the "
                "repository to GitHub and keep it public, and record a demo video of the "
                "working app and post it on LinkedIn.",
            ],
        ],
    ),
    (
        "Questions you are likely to be asked",
        [
            "Short answers to the questions that come up most often about a project of this "
            "shape.",

            ("About the data",),
            [
                "Why rescale to 0-1? Neural networks train more steadily on small inputs. "
                "Large raw values of 0-255 produce large gradients and unstable learning.",
                "Why augment only the training set? Validation and test scores must describe "
                "performance on real photographs. Augmenting them would measure the model on "
                "pictures that do not exist.",
                "Why no vertical flip? A mirrored fish is realistic; an upside-down fish is "
                "not. Augmentation should only produce images that could genuinely occur.",
                "Why does shuffle=False matter for the test set? Because evaluate.py pairs "
                "the predictions with test_generator.classes, which is in folder order. "
                "Shuffling would misalign them and the accuracy would be meaningless.",
            ],

            ("About the models",),
            [
                "What is transfer learning? Reusing a model trained on a large general "
                "dataset (ImageNet) and retraining only a small new output layer for your "
                "own task.",
                "Why freeze the base? Speed, and protection. Frozen layers are not updated, "
                "so each epoch is much faster, and the randomly-initialised head cannot send "
                "large early gradients that would damage the pre-trained weights.",
                "Why a smaller learning rate for the pre-trained models? Because they start "
                "from a good place. 0.0001 nudges them; 0.001 would overwrite what they "
                "know.",
                "Why GlobalAveragePooling2D instead of Flatten? It produces far fewer numbers "
                "(for example 1280 instead of tens of thousands), which means far fewer "
                "weights in the next layer and much less overfitting.",
                "Why does EfficientNetB0 need the Rescaling(255.0) layer? It performs its own "
                "normalisation internally and expects 0-255 input, but the generator has "
                "already divided by 255. Without the correction its accuracy collapses to "
                "near random.",
                "Which model would you expect to win? Usually MobileNet or EfficientNetB0 - "
                "strong accuracy with far fewer parameters than VGG16, so they also train "
                "fastest. The from-scratch CNN is normally the weakest, because it has only "
                "this dataset to learn from.",
            ],

            ("About training and evaluation",),
            [
                "What is an epoch, a batch and a learning rate? One full pass over the "
                "training data; the number of images seen before one weight update; and the "
                "size of that update.",
                "How do you know the model is overfitting? Training accuracy keeps climbing "
                "while validation accuracy flattens or falls - visible immediately on the "
                "training-history graph.",
                "What stops it here? Data augmentation, dropout, and EarlyStopping with "
                "restore_best_weights.",
                "Why report F1 rather than accuracy? Because the dataset is not balanced. "
                "With one species far larger than the others, accuracy can look high while "
                "the small species are being missed completely.",
                "What does the confusion matrix add? It names the specific pairs of species "
                "the model mixes up, which points to the fix - usually more images or better "
                "augmentation for those two classes.",
            ],

            ("About the code and deployment",),
            [
                "Why is there a config.py? So that a setting exists in exactly one place. It "
                "is the practical form of the 'maintainable' and 'modular' marks in the "
                "evaluation metrics.",
                "How does the app know which model to load? train_all_models.py copies the "
                "winner to models/best_model.h5 and writes models/class_names.json. The app "
                "reads those two fixed names, so a change of winning architecture needs no "
                "change to the app.",
                "Why @st.cache_resource? A Streamlit script reruns top to bottom on every "
                "interaction. Without caching, the model would reload from disk on every "
                "click.",
                "What is the most likely deployment bug? Preprocessing the uploaded image "
                "differently from the training images - most often forgetting to divide by "
                "255. The app would still answer confidently, and would still be wrong.",
            ],
        ],
    ),
    (
        "Glossary",
        [
            [
                "Augmentation - randomly rotating, zooming, shifting or flipping training "
                "images so the model sees a new version each epoch.",
                "Batch - the group of images processed before one weight update. 32 here.",
                "Callback - an object Keras runs automatically during training, such as "
                "EarlyStopping or ModelCheckpoint.",
                "CNN - Convolutional Neural Network; a network that finds patterns by sliding "
                "small filters across an image.",
                "Confusion matrix - a grid of true species against predicted species. The "
                "diagonal is correct, everything else is a mistake.",
                "Dense layer - a fully connected layer where every input reaches every "
                "neuron.",
                "Dropout - randomly switching off a fraction of neurons during training, to "
                "prevent memorising.",
                "Epoch - one complete pass through the training set.",
                "F1-score - the balance of precision and recall as a single number.",
                "Fine-tuning - training a pre-trained model further on your own data.",
                "Generator - an object that yields batches of images from disk instead of "
                "loading everything into memory.",
                "GlobalAveragePooling - averaging each feature map down to one number, used "
                "instead of Flatten to keep the model small.",
                "ImageNet - a dataset of 1.2 million labelled photographs across 1000 "
                "categories, used to pre-train the five borrowed models.",
                "Learning rate - how large each weight adjustment is.",
                "Loss - the number the model tries to minimise. Falling loss means learning.",
                "One-hot encoding - representing class 2 of 5 as [0,0,1,0,0].",
                "Overfitting - memorising the training data instead of learning the general "
                "pattern.",
                "Pooling - shrinking the image between convolution layers.",
                "ReLU - an activation that replaces negative values with zero, letting the "
                "network learn non-linear relationships.",
                "Softmax - converts the final layer's numbers into probabilities that sum "
                "to 1.0.",
                "Transfer learning - reusing a model trained on one task as the starting "
                "point for another.",
                "Weights - the numbers inside the model that training adjusts; what a .h5 "
                "file stores.",
            ],
        ],
    ),
]
