"""Line-by-line notes for src/visualize.py."""

PURPOSE = (
    "Every graph in the project is drawn here and nowhere else. Three kinds: the "
    "training curves for one model, the bar chart comparing all six, and the chart "
    "of how many images each species has. Keeping all the plotting in one file "
    "means the graphs share a consistent look, and the files that do the real work "
    "are not cluttered with styling."
)

NOTES = {
    11: "os, for building the paths the PNG files are saved to.",

    13: "Imports matplotlib.",
    14: "Selects the 'Agg' backend, which writes images to files rather than opening "
        "windows. As in evaluate.py, this line must come BEFORE pyplot is imported, "
        "or it has no effect.",
    15: "Now pyplot is safe to import.",
    16: "pandas, used to turn the list of results into a table that can plot itself.",

    18: "Our settings, for the plots folder path.",

    21: "Draws the two training curves for one model. It takes the history "
        "dictionary rather than the model, so graphs can be redrawn later from the "
        "saved JSON without retraining anything.",

    32: "Creates one figure holding two graphs side by side - 1 row, 2 columns. The "
        "two returned axes are named left_graph and right_graph so the code below "
        "reads plainly.",

    35: "Plots training accuracy against epoch number. marker='o' puts a dot on each "
        "epoch, which matters here because with only 4 epochs a plain line is hard "
        "to read.",
    36: "Plots validation accuracy on the same axes, so the two can be compared "
        "directly. The gap between these two lines is the thing to look at: if "
        "training accuracy climbs while validation accuracy stalls or falls, the "
        "model is overfitting.",
    37: "Titles the graph with the model's name.",
    38: "Labels the horizontal axis as the epoch number.",
    39: "Labels the vertical axis as accuracy.",
    40: "Draws the legend, so the two lines can be told apart.",
    41: "Adds faint grid lines. alpha=0.3 makes them 30% opaque so they guide the "
        "eye without competing with the data.",

    44: "Plots training loss on the right-hand graph. Loss is the number the model "
        "is actually trying to reduce; accuracy is what humans find easier to read.",
    45: "Plots validation loss alongside it. Validation loss turning upward while "
        "training loss still falls is the clearest early warning of overfitting.",
    46: "Titles the loss graph.",
    47: "Labels the horizontal axis.",
    48: "Labels the vertical axis.",
    49: "Adds the legend.",
    50: "Adds the same faint grid.",

    52: "Rearranges everything so no label is clipped at the edges.",

    54: "Builds the output path, named after the model.",
    55: "Saves the figure at 120 dots per inch.",
    56: "Closes the figure to free the memory. Over six models this prevents "
        "matplotlib warning that too many figures are open.",

    58: "Prints where the graph was saved.",

    61: "Draws the bar chart that compares every model. It takes the list of score "
        "dictionaries collected by train_all_models.py.",

    70: "Turns that list of dictionaries into a pandas DataFrame - a table with one "
        "row per model and one column per score.",

    73: "Sorts by accuracy, highest first, so the winning model appears on the left "
        "and the chart tells its story immediately.",

    76: "Sets the model name as the row label, then keeps only the four score "
        "columns. This drops training_minutes and epochs_run, which belong in the "
        "table but would look absurd on a chart whose axis runs from 0 to 1.",

    78: "Asks pandas to draw the whole table as a grouped bar chart. One group per "
        "model, four bars per group.",

    80: "Adds the chart title.",
    81: "Labels the horizontal axis.",
    82: "Labels the vertical axis, stating the 0-to-1 range.",
    83: "Fixes the vertical axis from 0 to 1.05. This is an honesty measure: left to "
        "itself, matplotlib would zoom in on the range the data occupies, making a "
        "difference between 0.96 and 0.98 look enormous. Pinning the axis to the "
        "full possible range shows the real size of each gap.",
    84: "Tilts the model names 30 degrees so longer names do not overlap.",
    85: "Puts the legend bottom-right, where the bars are shortest and it blocks "
        "least.",
    86: "Adds horizontal grid lines only, which help in reading bar heights.",
    87: "Tidies the layout.",

    89: "Builds the output path. This file has a fixed name because the README and "
        "the Colab notebook both refer to it.",
    90: "Saves the chart.",
    91: "Closes the figure.",

    93: "Prints where it went.",
    94: "Returns the sorted table, which train_all_models.py prints as the final "
        "comparison and uses to pick the winner.",

    97: "Draws how many images each species has. This is what makes the imbalance "
        "in this dataset visible at a glance.",

    103: "generator.classes is a long list of class numbers, one per image, like "
         "[0,0,0,1,1,2,...]. value_counts() tallies how many times each number "
         "appears, and sort_index() puts them back in class order so they line up "
         "with the species names.",

    105: "Creates a wide, short figure suited to eleven labelled bars.",
    106: "Draws the bars, species names along the bottom, counts as the heights.",
    107: "Sets the title, which is passed in so the function can be reused for "
         "train, val or test.",
    108: "Labels the horizontal axis.",
    109: "Labels the vertical axis.",
    110: "Tilts the long species names 45 degrees.",
    111: "Tidies the layout.",

    113: "Builds the output path. The file name is passed in, again so the function "
         "can be reused.",
    114: "Saves it.",
    115: "Closes the figure.",

    117: "Prints where it went.",
}
