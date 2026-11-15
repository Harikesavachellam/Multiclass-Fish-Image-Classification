"""Line-by-line notes for app.py."""

PURPOSE = (
    "The Streamlit web application - the part of the project anyone can actually "
    "use, and the part to record for the demo video. It loads the winning model "
    "once, takes an uploaded photo, puts it through exactly the same preprocessing "
    "the model was trained on, and shows the predicted species with a confidence "
    "figure for every class. Streamlit re-runs this entire file top to bottom every "
    "time the user interacts with the page, which explains several of the choices "
    "below."
)

NOTES = {
    17: "json, used to read the species names back from the file training saved.",
    18: "os, used to build file paths and to check whether the model exists.",

    20: "numpy, for turning the image into numbers and for argmax.",
    21: "pandas, used to build the little table of per-species confidence.",
    22: "streamlit itself, conventionally imported as st.",
    23: "Pillow's Image class, which opens the uploaded file as a picture.",
    24: "load_model, to read the trained .h5 file.",

    26: "Our settings, so the image size used here is guaranteed to match the one "
        "used in training.",

    31: "Configures the browser page. Streamlit requires this to be the FIRST "
        "Streamlit command in the file - calling anything else before it raises an "
        "error.",
    32: "The text shown in the browser tab.",
    33: "The little icon in the tab.",
    34: "'centered' keeps the content in a readable column instead of stretching it "
        "across a wide monitor.",
    35: "Closes the call.",

    38: "The path to the winning model. train_all_models.py copies the best "
        "performer to this fixed name, so the app never needs to know which "
        "architecture won.",
    39: "The path to the species names saved during training.",
    40: "The path to a small text file holding the winning model's name, shown in "
        "the sidebar.",

    49: "This decorator is what keeps the app fast. It tells Streamlit to run the "
        "function below ONCE and keep the result in memory. Without it, the whole "
        "file re-runs on every click, and a 16 MB model would be read from disk "
        "each time - several seconds of waiting per interaction.",

    50: "Defines the loading function.",

    54: "Checks whether a trained model actually exists before trying to load it.",
    55: "If not, returns three Nones rather than crashing. The page below turns "
        "that into a helpful message instead of a stack trace - which matters if "
        "an examiner runs the app on a fresh clone.",

    57: "Loads the trained model from the .h5 file.",

    59: "Opens the species names file.",
    60: "Reads the list of names. Loading this from disk rather than retyping it is "
        "important: the order must match the order the model was trained with, or "
        "every prediction would carry the wrong label.",

    63: "A sensible default in case the name file is missing.",
    64: "If the file does exist...",
    65: "...open it...",
    66: "...and read the name, stripping the trailing newline.",

    68: "Returns the model, the names and the winning architecture's name.",

    71: "Converts an uploaded picture into exactly the form the model expects. This "
        "function must mirror the training preprocessing precisely - any difference "
        "here produces confident nonsense rather than an error.",

    80: "Forces the image to RGB. A PNG may carry a fourth transparency channel, and "
        "a photo may be greyscale with only one; the model only accepts three.",

    83: "Resizes to 224x224, taking the size from config so it cannot drift away "
        "from what data_loader used.",

    86: "Converts the picture into a numpy array of numbers, shaped "
        "(224, 224, 3).",

    89: "Divides by 255, which is exactly what ImageDataGenerator(rescale=1./255) "
        "did during training. Forgetting this single line is the classic cause of "
        "an app that works perfectly in testing and predicts nonsense in a demo.",

    94: "Adds a fourth dimension at the front, turning (224, 224, 3) into "
        "(1, 224, 224, 3). Keras models always expect a BATCH of images, so a "
        "single picture has to be presented as a batch of one.",

    96: "Returns the prepared batch.",

    103: "Draws the page's main heading. From here down, the code runs top to "
         "bottom every time the page refreshes.",
    104: "Writes the introductory sentence.",
    105: "The first part of that text.",
    106: "The second part. Python joins these two adjacent strings automatically.",
    107: "Closes the call.",

    109: "Calls the cached loader. On the first run this reads the model from disk; "
         "on every later run it returns the copy already in memory instantly.",

    112: "If no model was found...",
    113: "...show a red error box...",
    114: "...saying plainly that nothing is trained yet...",
    115: "...and telling the user exactly which command fixes it...",
    116: "...naming the file the app is looking for.",
    117: "Closes the error message.",
    118: "st.stop() halts the script here, so the rest of the page never runs. "
         "Without this, the next lines would try to use a model that is None and "
         "crash with a confusing error.",

    121: "Opens the sidebar. Everything indented under this 'with' block is drawn "
         "in the panel on the left.",
    122: "A heading for the sidebar.",
    123: "Shows which architecture won - MobileNet, in this project.",
    124: "Shows how many species the model can recognise, counted from the list "
         "rather than typed as 11.",
    125: "States the input size, which helps anyone judging what kind of photo to "
         "upload.",
    126: "Draws a horizontal line.",
    127: "A heading for the species list.",
    128: "Loops over every species name...",
    129: "...and prints it as a bullet, so the user knows what the model can and "
         "cannot identify.",

    132: "Creates the upload box, which is the brief's 'allow users to upload fish "
         "images' requirement.",
    133: "The label shown on the box, and the file types accepted. Restricting the "
         "types stops someone uploading a PDF and getting an obscure error. Be aware "
         "Streamlit matches on the file EXTENSION here, not on what the file really "
         "is: a .jfif file is an ordinary JPEG that Windows and Chrome sometimes save "
         "under that name, and it was rejected until jfif was added to this list. "
         "Pillow opens all six of these happily, and prepare_image() converts "
         "whatever arrives to RGB.",
    134: "Closes the call.",

    136: "This is None until the user actually uploads something, so everything "
         "indented below only happens once a file arrives.",

    139: "Opens the uploaded file as a picture.",

    142: "Shows the uploaded photo back to the user, so they can see the app got the "
         "right file.",

    145: "st.spinner shows a 'Thinking ...' message while the indented code runs. "
         "Prediction takes a moment on a CPU, and without this the page would "
         "simply appear frozen.",
    146: "Converts the picture into the model's expected input.",

    149: "Runs the model. predict() returns one row per image; [0] takes the single "
         "row, which holds eleven probabilities adding up to 1.0.",

    152: "argmax finds the position of the largest probability - the model's "
         "choice. int() converts numpy's integer type into a plain Python one.",
    153: "Looks that position up in the species list to get a readable name. This is "
         "where the saved class order matters.",
    154: "Converts the winning probability into a percentage.",

    159: "Shows the predicted species in a green success box. The ### makes it a "
         "large heading, so it is readable from across a room in a demo video.",
    160: "Shows the confidence as a metric, to two decimal places. This is the "
         "brief's 'provide model confidence scores' requirement.",

    165: "A subheading for the full breakdown.",

    168: "Builds a small table so the user can see the confidence for every species, "
         "not just the winner. This is what shows whether the model was certain or "
         "torn between two similar fish.",
    169: "Opens the dictionary of columns.",
    170: "The first column: the species names.",
    171: "The second column: each probability as a percentage, rounded to two "
         "decimal places.",
    172: "Closes the dictionary.",
    173: "Closes the DataFrame.",

    176: "Sorts so the most likely species is at the top.",

    179: "Draws the bar chart. set_index('Species') tells Streamlit to use the "
         "species names as the labels along the bottom.",

    182: "Shows the same numbers as a table underneath. hide_index=True removes the "
         "meaningless row numbers; use_container_width makes it fill the page.",

    184: "If no file has been uploaded yet...",
    185: "...show a friendly blue prompt rather than an empty page.",
}
