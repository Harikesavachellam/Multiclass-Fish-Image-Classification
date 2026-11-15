"""Line-by-line notes for src/train.py."""

PURPOSE = (
    "This file trains exactly ONE model and saves it. The loop that trains all six "
    "lives in train_all_models.py, which calls this function six times. Keeping "
    "'train one model' separate from 'train every model' is what lets you retrain a "
    "single model without touching the rest, and it keeps each piece small enough "
    "to understand on its own."
)

NOTES = {
    10: "json is used at the end to write the training history to a file.",
    11: "os is used to build the paths where the model and history are saved.",
    12: "time is used to measure how long training took, which goes into the "
        "comparison table.",

    14: "Imports the two callbacks. A callback is a small helper that Keras runs "
        "automatically at the end of every epoch.",

    16: "Our settings.",
    17: "Our image-loading module.",
    18: "Our model-building module. It is imported 'as model_builder' because the "
        "name 'models' would otherwise clash with Keras's own models module.",

    21: "The main function. It receives the model's name plus the two generators, "
        "so it never has to load the images itself - they are loaded once and "
        "reused for all six models.",

    36: "Prints a line of equals signs to separate this model's output in the log.",
    37: "Prints which model is starting, so a long log file stays readable.",
    38: "Closes the banner.",

    42: "Asks the generator how many species it found. Taking this from the data "
        "rather than hard-coding 11 means the project works unchanged on a "
        "different dataset.",
    43: "Prints that number as a sanity check.",

    46: "Calls the dispatcher in models.py, which returns a compiled model matching "
        "the name. This one line is where all six architectures come from.",

    49: "Prints the table of layers and parameter counts. Worth capturing for your "
        "demo video and your report - it is the clearest evidence of what the "
        "model actually is.",

    52: "Builds the path the .h5 file will be saved to, named after the model.",

    60: "Creates the EarlyStopping callback.",
    61: "Watches validation accuracy - how well the model does on images it is not "
        "learning from. Watching TRAINING accuracy instead would be a mistake, "
        "because that keeps rising even as the model starts memorising.",
    62: "How many epochs of no improvement to tolerate, taken from config so it can "
        "be overridden from the command line.",
    63: "The most valuable setting here. When training stops, rewind the weights to "
        "the best epoch rather than keeping the last, possibly worse, one.",
    64: "Print a message when it triggers, so the log shows why training stopped.",
    65: "Closes the callback.",

    69: "Creates the ModelCheckpoint callback.",
    70: "Where to write the file.",
    71: "Judge 'better' by validation accuracy, the same yardstick EarlyStopping uses.",
    72: "Only overwrite the file when the model actually improves. So the .h5 on "
        "disk is always the best version seen so far, not the most recent one.",
    73: "Print a line each time it saves.",
    74: "Closes the callback.",

    79: "Records the clock before training starts.",

    81: "model.fit() is the line that does the actual learning. Everything before "
        "this was preparation; everything after is reporting.",
    82: "Learn from the training generator, which hands over augmented batches.",
    83: "After each epoch, check performance on the validation generator.",
    84: "Repeat for at most this many epochs - EarlyStopping may cut it short.",
    85: "Hand both callbacks to Keras so they run automatically each epoch.",
    86: "Print a progress bar so you can see it working.",
    87: "Closes the fit call. For the from-scratch CNN this line took 35 minutes.",

    89: "Works out how long training took, in minutes.",

    91: "Reports the time taken.",
    92: "Reports where the model was saved.",

    96: "history.history is a plain dictionary of lists: one list of accuracies, one "
        "of validation accuracies, one of losses, with one entry per epoch.",

    100: "Builds the path for the history JSON file.",
    101: "Opens that file for writing. 'with' guarantees it is closed properly even "
         "if something goes wrong.",
    102: "Writes the history as JSON, indented so a human can read it. Saving this "
         "means the training graphs can be redrawn later without retraining "
         "anything - which took hours the first time.",

    104: "Returns three things: the history, where the model was saved, and how long "
         "it took. The caller uses all three.",

    107: "A small convenience function so other scripts can get everything they need "
         "with one call instead of importing data_loader themselves.",

    112: "Builds the three generators.",
    113: "Works out the ordered list of species names from the training generator.",
    114: "Returns all four together.",
}
