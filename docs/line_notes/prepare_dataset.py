"""Line-by-line notes for prepare_dataset.py."""

PURPOSE = (
    "Run once, before training, to get the downloaded images into the folder shape "
    "Keras expects. It copes with three situations: a dataset already split into "
    "train/val/test, a dataset that is only species folders and needs splitting "
    "70/15/15, and a zip that unpacked with extra wrapper folders around the real "
    "data. For this project's dataset the first case applied, but the splitting "
    "code is what makes the project work on a differently packaged copy."
)

NOTES = {
    19: "argparse, to read the --source folder from the command line.",
    20: "os, for walking folders and building paths.",
    21: "random, used to shuffle before splitting.",
    22: "shutil, for copying whole folder trees.",
    24: "Our settings, which say where data/ lives.",

    27: "The file extensions treated as images. Keeping this as one tuple means "
        "'what counts as an image' is defined in exactly one place.",

    30: "70% of each species goes to training.",
    31: "15% goes to validation. The remaining 15% becomes the test set, worked out "
        "by subtraction rather than written down, so the three shares can never "
        "add up to anything but 100%.",

    35: "Lists the image files sitting directly inside one folder.",
    37: "Starts with an empty list.",
    38: "Looks at every entry in the folder.",
    39: ".lower() first means .JPG and .jpg are both accepted. endswith() accepts a "
        "tuple and returns True if any of them match.",
    40: "Keeps the name if it is an image.",
    41: "Returns the collected names.",

    44: "Lists the folders inside one folder, ignoring files.",
    46: "Starts with an empty list.",
    47: "Looks at every entry.",
    48: "os.path.isdir() is the test for 'this is a folder, not a file'.",
    49: "Keeps it if so.",
    50: "Returns them sorted, so the order is predictable rather than whatever the "
        "operating system happens to give.",

    53: "Handles the wrapper-folder problem. A zip often unpacks to "
        "extracted/Dataset/train/... with one or more useless folders wrapped "
        "around the real content.",

    60: "Starts at the folder the user gave.",

    63: "Loops until the function returns.",
    64: "Lists the folders at this level.",
    65: "Lists the images at this level.",

    67: "The test for a wrapper: exactly one folder inside, and no loose images. "
        "That combination means the real data must be one level further down.",
    68: "Step into it and loop again.",
    69: "Otherwise...",
    70: "...this is the real root, so return it.",

    73: "Handles the case where the dataset is already divided into train, val and "
        "test.",

    78: "Tells the user which path was taken.",

    81: "A dictionary mapping the names a dataset MIGHT use to the folder we want.",
    82: "'train' maps to our training folder.",
    83: "'training' maps to the same place.",
    84: "'val'...",
    85: "'valid'...",
    86: "'validation' - three spellings, one destination.",
    87: "'test'...",
    88: "'testing' likewise.",
    89: "Closes the dictionary. This is what lets the script accept datasets packaged "
        "by different people with different naming habits.",

    91: "Looks at each folder in the source.",
    92: "Looks its lower-cased name up in the map. .get() returns None instead of "
        "raising an error when the name is unknown.",

    94: "If the name was not recognised...",
    95: "...skip it quietly. A stray 'notes' or '__MACOSX' folder should not stop "
        "the program.",

    97: "Builds the full path to copy from.",

    100: "If something is already at the destination...",
    101: "...delete it first. copytree refuses to write into an existing folder, and "
         "this also stops a second run from mixing old and new files together.",

    103: "Reports what is being copied.",
    104: "Copies the entire folder tree, subfolders and all.",

    107: "Handles the other case: just species folders, which need splitting.",

    112: "Tells the user which path was taken.",

    114: "Gets the list of species folders.",

    117: "Seeds the random generator from config. This is what makes the split "
         "REPEATABLE: run the script twice and the same images land in the same "
         "sets. Without it, a second run would reshuffle and could move a training "
         "image into the test set, quietly invalidating any comparison with earlier "
         "results.",

    119: "Handles one species at a time.",
    120: "Builds the path to that species' folder.",
    121: "Lists its images.",

    123: "If the folder turned out to be empty...",
    124: "...say so...",
    125: "...and move on rather than creating empty folders.",

    127: "Shuffles the filenames. Without this, files are processed in alphabetical "
         "order, and if the photos happen to be grouped (all of one fish first), "
         "the three splits would end up systematically different from each other.",

    130: "How many images this species has.",
    131: "The position to cut at for training - 70% of the way through. int() rounds "
         "down to a whole number, since you cannot have a fraction of a file.",
    132: "The position to cut at for validation - 85% of the way through.",

    135: "A dictionary mapping each destination folder to its slice of the list.",
    136: "[:train_cut] means 'from the start up to the cut' - the first 70%.",
    137: "[train_cut:val_cut] means 'between the two cuts' - the next 15%.",
    138: "[val_cut:] means 'from the cut to the end' - the final 15%. Because this "
         "takes everything left, no image can ever be lost or duplicated.",
    139: "Closes the dictionary.",

    141: "Loops over the three destinations and their file lists together.",
    142: "Builds the species folder inside that destination.",
    143: "Creates it, including parents, without complaining if it exists.",

    145: "For each file in this group...",
    146: "...copy it...",
    147: "...from its place in the source...",
    148: "...to its place in the destination.",
    149: "Closes the copy. Note it COPIES rather than moves, so the original "
         "download is left untouched and the script can safely be run again.",

    151: "Prints a one-line summary for this species...",
    152: "...showing the three counts, each worked out from the cut positions.",

    155: "Prints the final tally, which is how you confirm the dataset is where it "
         "should be before spending hours training.",

    157: "Prints a blank line and a separator.",
    158: "Prints the heading.",
    159: "Prints another separator.",

    161: "Loops over the three splits...",
    162: "...training...",
    163: "...validation...",
    164: "...and test.",
    165: "Closes the list.",

    166: "If a split folder is missing...",
    167: "...say so plainly rather than crashing...",
    168: "...and carry on to the next.",

    170: "A running total for this split.",
    171: "Prints the split's name as a heading.",
    172: "Loops over its species folders.",
    173: "Counts the images in each.",
    174: "Adds to the running total.",
    175: "Prints the species name padded to 35 characters and the count right "
         "aligned in 6, so the output lines up into readable columns.",
    176: "Prints the total for this split.",

    179: "The main function, which ties the whole script together.",
    180: "Creates the argument parser.",
    181: "Starts defining --source.",
    182: "Its name.",
    183: "required=True means the script refuses to run without it, which is right "
         "because there is no sensible default for 'where did you unzip it'.",
    184: "The help text.",
    185: "Closes the option.",
    186: "Reads what the user typed.",

    188: "Checks the folder actually exists...",
    189: "...and exits with a clear message if not. SystemExit stops the program "
         "without a confusing stack trace.",

    192: "Creates data/ if needed.",

    195: "Steps down through any wrapper folders to find the real root.",
    196: "Prints where it settled, so the user can see it guessed correctly.",

    199: "Lists what is inside, lower-cased so 'Train' and 'train' both match.",

    201: "Decides which case we are in: if there is a train folder, the dataset is "
         "already split.",

    203: "If it is already split...",
    204: "...copy the folders across.",
    205: "Otherwise...",
    206: "...split the species folders 70/15/15.",

    209: "Some datasets ship train and test but no validation set.",
    210: "Say what is being done...",
    211: "...and copy the test folder to serve as validation. Worth knowing this is "
         "a compromise: validation and test would then contain the same images, so "
         "the validation score would no longer be independent. It did not apply to "
         "this project's dataset, which arrived with all three.",

    213: "Prints the final summary.",
    214: "Tells the user what to run next.",

    217: "Only run main() when the file is executed directly.",
    218: "Calls it.",
}
