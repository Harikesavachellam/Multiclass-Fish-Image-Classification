"""Line-by-line notes for src/evaluate.py."""

PURPOSE = (
    "Once a model is trained, this file gives it a final exam on the TEST images - "
    "pictures it has never seen in any form - and writes down the marks. It "
    "deliberately loads the model back from the .h5 file rather than using the one "
    "still in memory, which proves the saved file actually works. It produces the "
    "four headline metrics the brief asks for, a per-species breakdown, and the "
    "confusion matrix."
)

NOTES = {
    15: "os, for building output file paths.",

    17: "Imports matplotlib, the plotting library.",
    18: "Switches matplotlib to the 'Agg' backend, which draws into files instead of "
        "opening windows. This MUST come before pyplot is imported on the next "
        "line. Without it, a script run on a server with no screen crashes, and on "
        "a laptop it would pop up windows that block training until you close them.",
    19: "Now pyplot can be imported safely.",

    20: "numpy, used for argmax - finding the position of the largest number.",
    21: "seaborn, which draws the confusion-matrix heatmap much more attractively "
        "than matplotlib alone.",

    22: "Opens a bracketed import of the scikit-learn metrics.",
    23: "accuracy_score - the plain percentage correct.",
    24: "classification_report - the per-species text table.",
    25: "confusion_matrix - the grid of true versus predicted.",
    26: "f1_score - the balance of precision and recall.",
    27: "precision_score - of the images called X, how many really were X.",
    28: "recall_score - of the images that really were X, how many were found.",
    29: "Closes the import.",

    30: "load_model, to read a saved .h5 file back into a usable model.",
    32: "Our settings, for the output folder paths.",

    35: "The main evaluation function. It takes the PATH to the model rather than "
        "the model object itself, which is what forces the round trip through disk.",

    49: "Announces which model is being tested.",

    52: "Loads the model back from the .h5 file. This is a deliberate design "
        "choice: if the saved file were somehow broken, this line would fail here "
        "during training rather than later in the Streamlit app in front of an "
        "examiner.",

    55: "Rewinds the generator to the first image. Without this, if anything had "
        "already pulled batches from it, predictions would start partway through "
        "the dataset and silently misalign with the labels.",

    59: "Runs every test image through the model. The result is one row per image, "
        "each row holding eleven probabilities that add up to 1.0.",

    63: "argmax finds the POSITION of the largest probability in each row - which is "
        "the species the model chose. axis=1 means 'along each row'.",

    67: "The true answers, as a plain list of class numbers in folder order. This "
        "line is only correct because the test generator was created with "
        "shuffle=False. If it had shuffled, these labels would describe different "
        "images from the predictions above, and every number below would be wrong "
        "without anything appearing to break.",

    74: "Accuracy: the fraction of all test images classified correctly.",

    75: "Precision, weighted. average='weighted' computes the score for each species "
        "separately then averages them, giving more say to species with more test "
        "images. zero_division=0 says that if a species was never predicted at all, "
        "score it 0 rather than crashing - which matters here, because the bass "
        "class is predicted very rarely.",

    76: "Recall, weighted, with the same handling.",
    77: "F1-score, weighted - the harmonic mean of precision and recall, and the "
        "fairest single number to quote on an unbalanced dataset like this one.",

    79: "Prints accuracy to four decimal places.",
    80: "Prints precision.",
    81: "Prints recall.",
    82: "Prints the F1-score.",

    87: "Builds the per-species table.",
    88: "target_names=class_names puts the real species names in the table instead "
        "of the numbers 0 to 10, which makes it readable in the report.",
    89: "Closes the call.",

    91: "Builds the path for this model's report file.",
    92: "Opens it for writing.",
    93: "Writes a heading naming the model.",
    94: "Writes a line of equals signs under the heading.",
    95: "Writes the table itself.",

    100: "Calls the function below to draw and save the confusion matrix picture.",

    103: "Returns the scores as a dictionary.",
    104: "The model's name, so rows can be told apart in the comparison table.",
    105: "Its accuracy.",
    106: "Its precision.",
    107: "Its recall.",
    108: "Its F1-score.",
    109: "Closes the dictionary. train_all_models.py collects one of these per "
         "model and turns the collection into the comparison CSV.",

    112: "Draws the confusion matrix. Kept as its own function because it is a "
         "separate job - calculating scores and drawing pictures should not be "
         "tangled together.",

    120: "Builds the grid of counts. Row = true species, column = predicted species.",

    123: "Creates a figure 10 by 8 inches, large enough for eleven long species "
         "names.",

    125: "Draws the heatmap.",
    126: "The grid of numbers to draw.",
    127: "annot=True writes the actual count inside each square, so the picture is "
         "readable as a table too.",
    128: "fmt='d' formats those numbers as whole integers rather than decimals.",
    129: "The 'Blues' colour scheme - darker means more images.",
    130: "Species names along the bottom.",
    131: "Species names down the side.",
    132: "Closes the heatmap call.",

    134: "Adds a title naming the model.",
    135: "Labels the horizontal axis as what the model predicted.",
    136: "Labels the vertical axis as the truth.",
    137: "Tilts the bottom labels 45 degrees so the long species names do not "
         "overlap each other.",
    138: "Keeps the side labels horizontal, where there is room for them.",
    139: "tight_layout resizes everything so no label is cut off at the edge.",

    141: "Builds the output path for the PNG.",
    142: "Saves the picture at 120 dots per inch - sharp enough to read in a report.",
    143: "Closes the figure. Skipping this would leave each figure in memory, and "
         "after six models matplotlib would start warning about memory use.",

    145: "Prints where the picture went.",
}
