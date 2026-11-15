"""Line-by-line notes for validate_data.py."""

PURPOSE = (
    "Checks the dataset is accurate and complete BEFORE hours are spent training on "
    "it - the brief's 'data validation' guideline. The most valuable check here is "
    "the leakage test: if a test image was also used for training, the model has "
    "already seen the answer and the reported accuracy is meaningless. This script "
    "never changes a file; it only looks and reports."
)

NOTES = {
    29: "collections, which provides the two convenient counting containers used "
        "below.",
    30: "hashlib, for fingerprinting file contents.",
    31: "os, for walking the folders.",
    32: "sys, used to exit with a failure code if something is wrong.",
    34: "Pillow's Image class, used to test whether each file really decodes.",
    36: "Our settings, which say where the three folders are.",

    39: "Produces a short fingerprint of a file's contents.",

    48: "Opens the file in binary mode ('rb'), because we want the raw bytes rather "
        "than text.",
    49: "Reads the whole file, runs md5 over it, and returns the result as text. Two "
        "files with the same fingerprint hold identical bytes, so they are the same "
        "picture. Comparing fingerprints rather than filenames is what catches a "
        "duplicate that was renamed.",

    52: "Check one: do the three folders exist at all?",
    54: "Announces the check.",

    56: "Collects any folders that are missing.",
    57: "Looks at all three.",
    58: "If one is not a folder...",
    59: "...record it.",

    61: "If anything was missing...",
    62: "...print a heading...",
    63: "...list each missing folder...",
    64: "...one per line...",
    65: "...tell the user exactly how to fix it...",
    66: "...and report failure.",

    68: "Otherwise confirm all three are present.",
    69: "Report success.",

    72: "Check two: does every split hold the same species?",
    74: "Announces the check. The leading \\n puts a blank line before it.",

    76: "A dictionary to hold each split's species.",
    77: "Loops over the three splits by name and folder.",
    78: "The validation entry.",
    79: "The test entry.",
    81: "Stores the species as a set. Sets can be compared and subtracted directly, "
        "which is what the next few lines rely on.",

    83: "An empty set to collect every species seen anywhere.",
    84: "Looks at each split's set...",
    85: "...and joins it in. The | operator is set union - everything in either set.",

    87: "Counts problems found.",
    88: "Looks at each split again, now that the full list is known.",
    89: "Set subtraction: everything in the full list that this split does NOT have.",
    90: "If anything is missing...",
    91: "...count it as a problem...",
    92: "...and say which split and which species. This matters because a species "
        "missing from the test folder can never be scored, and one missing from "
        "train can never be learned.",

    94: "If nothing was missing...",
    95: "...confirm it, naming the number of species found.",

    97: "Returns True only when there were no problems.",

    100: "Checks three and four together - opening every image, spotting duplicates "
         "and counting the classes.",

    107: "Announces the check.",

    110: "A dictionary that maps a fingerprint to the list of places that exact "
         "image was found. defaultdict(list) means a missing key automatically "
         "starts as an empty list, so there is no need to check before appending.",

    112: "Collects any files that failed to open.",
    113: "A nested counter: split, then species, then how many images. "
         "defaultdict(Counter) creates the inner counter automatically.",

    115: "Walks the three splits.",
    116: "The validation entry.",
    117: "The test entry.",

    119: "Loops over the species folders, sorted so output is predictable.",
    120: "Builds the path to that species folder.",

    122: "Loops over every file in it.",
    123: "Builds the full path to the file.",
    124: "Counts it. All three checks share this single pass over the files, because "
         "reading 10,514 images three separate times would be three times as slow.",

    126: "try/except so that one damaged file is reported rather than crashing the "
         "whole run.",
    127: "Fingerprints the file and records where it was found, as "
         "'split/species/filename'.",

    131: ".verify() asks Pillow to decode the file and complain if it is damaged. It "
         "is faster than fully loading the image because it does not build the "
         "pixel data.",

    133: "If anything above raised an error...",
    134: "...record the file and the reason, and carry on with the next one.",

    137: "If any files failed...",
    138: "...say how many...",
    139: "...and list the first ten only, because a systematically broken download "
         "could produce thousands and flood the screen.",
    140: "Prints each path with its error.",
    141: "Otherwise...",
    142: "...confirm every file opened.",

    145: "Collects images found in more than one split - the leakage cases.",
    146: "Counts images duplicated within a single split, which is harmless.",

    148: "Looks at every fingerprint's list of locations.",
    149: "If the image appeared only once...",
    150: "...there is nothing to report, so move on.",

    154: "Takes the part before the first slash of each location - the split name - "
         "and collects them into a set. If the same image is in train and test, "
         "this set holds two entries.",

    156: "More than one split involved means leakage...",
    157: "...so record it.",
    158: "Otherwise...",
    159: "...it is just a duplicate inside one split, which only means that picture "
         "counts twice. Not ideal, but it does not invalidate anything.",

    161: "If leakage was found...",
    162: "...say so in the strongest terms...",
    163: "...and state the consequence plainly: the scores cannot be trusted.",
    164: "Lists the first five cases...",
    165: "...so the problem can be traced.",
    166: "Otherwise...",
    167: "...confirm there is none. For this project this line is what justifies "
         "quoting 98.15% as a real number.",

    169: "If there were harmless within-split duplicates...",
    170: "...mention how many...",
    171: "...and explain why they are not the same problem, so the note is not "
         "mistaken for a warning.",

    174: "Starts the per-species count report.",
    175: "Gets the species list from the training counts, sorted.",
    176: "Prints the column headings. The <40 and >7 are format specifiers - pad "
         "left-aligned to 40 characters, right-aligned to 7 - which is what makes "
         "the output line up into columns.",

    178: "Tracks the smallest class found so far. Both start as None because no "
         "class has been seen yet.",
    179: "Loops over the species.",
    180: "How many training images this species has.",
    181: "Prints the species and its training count...",
    182: "...followed by its validation and test counts.",

    184: "If this is the first species, or smaller than the smallest so far...",
    185: "...remember it.",

    187: "Totals every count across all three splits.",
    188: "Prints the TOTAL row...",
    189: "...with the three per-split totals.",
    190: "Prints the grand total.",

    193: "Works out the average number of training images per species.",
    194: "If the smallest class has less than a third of the average, it is unusual "
         "enough to warn about explicitly.",
    195: "Names the species and its count...",
    196: "...compares it to the average...",
    197: "...predicts the consequence - its recall will be the weakest number...",
    198: "...and says which metric to quote instead. For this dataset it flags "
         "'animal fish bass' at 30 images against an average of 566, and its recall "
         "did indeed come out at 0.15.",

    200: "Returns True only if nothing was broken and nothing leaked. Duplicates "
         "inside a split are deliberately not treated as failure.",

    203: "Ties the checks together.",
    204: "Prints a separator.",
    205: "Prints the heading.",
    206: "Prints another separator.",
    207: "States which folder is being checked, so there is no doubt about what was "
         "validated.",

    209: "If the folders are missing there is nothing to check...",
    210: "...so exit with code 1. A non-zero exit code is the standard way of "
         "signalling failure, which lets this script be used in an automated "
         "pipeline.",

    212: "Runs the species check.",
    213: "Runs the image, duplicate and count checks.",

    215: "Prints a separator before the verdict.",
    216: "If both checks passed...",
    217: "...say the dataset is safe to train on.",
    218: "Otherwise...",
    219: "...say problems were found...",
    220: "...and exit with a failure code.",
    221: "Prints the closing separator.",

    224: "Only run main() when executed directly.",
    225: "Calls it.",
}
