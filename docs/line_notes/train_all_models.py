"""Line-by-line notes for train_all_models.py."""

PURPOSE = (
    "The main script - the one you actually run. It loads the images once, loops "
    "over the six models training and testing each, saves the results after every "
    "model, draws the comparison chart and copies the winner to best_model.h5 for "
    "the app. It also understands command-line options, which is what makes it "
    "possible to retrain a single model or resume a run that was stopped partway."
)

NOTES = {
    21: "argparse, Python's standard library for reading command-line options.",
    22: "json, used to save the species names for the app.",
    23: "os, for building file paths.",
    24: "shutil, used once at the end to copy the winning model file.",
    26: "pandas, for the results table and the CSV.",
    28: "Our settings.",
    29: "Our evaluation code.",
    30: "Our training code.",
    31: "Our graph-drawing code.",

    34: "The main function. Everything happens inside it, which keeps the "
        "module-level namespace clean.",

    38: "Creates the command-line parser. The description appears if you run the "
        "script with --help.",

    39: "Starts defining the --model option.",
    40: "Its name on the command line.",
    41: "Its default: train every model in config.MODEL_NAMES.",
    42: "The help text, first line.",
    43: "The help text, second line, showing the comma-separated form.",
    44: "Closes the option.",

    45: "Starts defining --epochs.",
    46: "Its name.",
    47: "type=int converts what the user types into a number; without this it would "
        "arrive as text and comparisons would misbehave.",
    48: "Default None, which is how the code below tells 'the user said nothing' "
        "apart from 'the user genuinely asked for zero'.",
    49: "The help text.",
    50: "Closes the option.",

    51: "Starts defining --patience.",
    52: "Its name.",
    53: "Also a number.",
    54: "Also defaults to None.",
    55: "The help text.",
    56: "Closes the option.",

    57: "Starts defining --retrain.",
    58: "Its name.",
    59: "action='store_true' makes this a flag: present means True, absent means "
        "False. It takes no value.",
    60: "The help text, explaining what it overrides.",
    61: "Continues that text.",
    62: "Finishes it, describing the resume behaviour.",
    63: "Closes the option.",

    64: "Reads whatever the user actually typed and returns it as an object whose "
        "attributes are the option names.",

    69: "If the user supplied --epochs...",
    70: "...overwrite the value in config. Because every other module reads "
        "config.EPOCHS at the moment it is used rather than copying it at import "
        "time, changing it here changes the behaviour of the whole program.",

    72: "The same for --patience...",
    73: "...overwriting the EarlyStopping patience.",

    76: "If the user did not name specific models...",
    77: "...train the full list of six from config.",
    78: "Otherwise...",
    81: "...split what they typed on commas and strip stray spaces, so both "
        "'MobileNet' and 'MobileNet, ResNet50' work.",

    84: "Creates models/ and outputs/ if they do not exist, so a freshly cloned "
        "copy of the project runs without manual setup.",

    89: "Announces that loading has started - it takes a few seconds.",
    90: "Loads all three generators and the species names in one call. This happens "
        "ONCE and the generators are reused for all six models, which is far "
        "cheaper than re-scanning the folders six times.",

    92: "Prints how many species were found.",
    93: "Loops over them with their position number...",
    94: "...printing each. This is worth keeping, because the position is exactly "
        "what the model's output numbers mean.",

    96: "Prints how many training images there are.",
    97: "Prints how many validation images.",
    98: "Prints how many test images.",

    102: "Builds the path for the species names file.",
    103: "Opens it for writing.",
    104: "Writes the list as JSON. The Streamlit app reads this file, which is how "
         "it knows that output number 8 means 'shrimp'.",

    107: "Draws the chart of images per species...",
    108: "...passing the training generator, the names, a title and a filename.",
    109: "Closes the call.",

    117: "Reads any results from an earlier run. This is the line that makes a long "
         "training job resumable.",

    119: "If anything was found...",
    120: "...collect the names of the models already finished...",
    121: "...and print them, so it is obvious why some models are about to be "
         "skipped.",

    123: "The main loop - everything below runs once per model.",

    126: "any() checks whether this model already has a row in the results. It "
         "returns True as soon as it finds one.",
    127: "If it is already done AND the user did not ask for a retrain...",
    128: "...say so clearly...",
    129: "...including how to force it...",
    130: "...and move straight on to the next model. This is what let the project "
         "switch to faster settings without throwing away the 35 minutes already "
         "spent on the from-scratch CNN.",

    133: "Trains this model. This single call does everything in train.py: builds "
         "the model, fits it, and saves the .h5 file.",
    134: "The arguments: which model, and the two generators.",
    135: "Closes the call. It returns the history, the saved path and the minutes "
         "taken.",

    138: "Draws this model's accuracy and loss curves.",

    141: "Tests the model on the test set and gets back the four scores. Note it "
         "passes model_path, not the model, so evaluate.py loads it from disk.",
    142: "Adds the training time to the scores, rounded to one decimal.",
    143: "Adds how many epochs actually ran. This can be fewer than requested when "
         "EarlyStopping triggers, and recording it is what makes the comparison "
         "honest.",

    145: "Adds this model's complete scores to the list.",

    149: "Writes the CSV again, inside the loop rather than after it. If training "
         "crashes on model five, the results for models one to four are already "
         "safely on disk.",

    154: "If there is more than one model to compare...",
    155: "...draw the comparison bar chart, which also returns the sorted table.",
    156: "Otherwise...",
    157: "...just build a table, since a bar chart of one model compares nothing.",

    159: "Prints a separator.",
    160: "Prints the heading.",
    161: "Prints another separator.",
    162: "Prints the whole table. index=False hides pandas' row numbers, which mean "
         "nothing here.",

    165: "max() with key=... finds the dictionary with the highest accuracy. The "
         "lambda tells it which value to compare on.",
    166: "Announces the winner and its accuracy.",

    170: "Builds the path to the winner's own .h5 file.",
    171: "Builds the path to the fixed name best_model.h5.",
    172: "Copies the winner to that fixed name. This is why the Streamlit app never "
         "needs to know which architecture won.",
    173: "Prints where it went.",

    176: "Opens a small text file...",
    177: "...and writes the winner's name into it, purely so the app can display it.",

    180: "A tiny function returning the CSV path.",
    182: "Returns that path. Having it in one function rather than typed in three "
         "places means the filename can never fall out of step between the saving "
         "and loading code.",

    185: "Writes the results collected so far to the CSV.",
    187: "Turns the list of dictionaries into a table.",
    188: "Writes it out, without pandas' row numbers.",

    191: "Reads the results of models trained in an earlier run.",

    199: "Gets the CSV path from the single function above.",

    201: "If the file does not exist yet...",
    202: "...return an empty list, so a first run behaves exactly like a resumed one "
         "with nothing done.",

    204: "Otherwise read the CSV into a table.",

    207: "to_dict('records') turns each row back into a dictionary - the same shape "
         "evaluate_model() produces. That is the point: the rest of the script "
         "cannot tell a result loaded from disk apart from one just calculated.",

    212: "This guard means main() runs when you execute the file directly, but not "
         "when another file imports it. Without it, importing anything from this "
         "script would start a multi-hour training run.",
    213: "Calls main().",
}
