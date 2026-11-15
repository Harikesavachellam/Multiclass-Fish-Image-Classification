"""
evaluate.py
-----------
After a model is trained, this file gives it a final exam on the TEST
images (pictures it has never seen) and writes down the marks.

The marks we calculate:
  accuracy  - out of all the test images, how many did it get right?
  precision - when it says "shrimp", how often is it actually shrimp?
  recall    - out of all the real shrimp pictures, how many did it find?
  f1-score  - one number that balances precision and recall
  confusion matrix - a grid showing exactly which species got mixed up
"""

import os

import matplotlib
matplotlib.use("Agg")       # draw graphs to files, do not open a window
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from tensorflow.keras.models import load_model

from src import config


def evaluate_model(model_path, test_generator, class_names, model_name):
    """
    Load a saved model, test it, and return a dictionary of its scores.

    Args:
        model_path:     path to the saved .h5 file
        test_generator: the conveyor belt of test images
        class_names:    list of species names, in model order
        model_name:     e.g. "MobileNet" (used for file names and titles)

    Returns:
        a dictionary of scores
    """

    print(f"\nEvaluating {model_name} ...")

    # Load the trained model back from disk
    model = load_model(model_path)

    # Always rewind the generator before predicting, so it starts at image 1
    test_generator.reset()

    # predict() returns probabilities, one row per image.
    # Example row: [0.01, 0.02, 0.95, 0.02] -> 95% sure it is class 2
    predicted_probabilities = model.predict(test_generator, verbose=1)

    # np.argmax picks the POSITION of the biggest number in each row,
    # which is the class the model chose.
    y_predicted = np.argmax(predicted_probabilities, axis=1)

    # The true answers. This works only because we set shuffle=False
    # for the test generator in data_loader.py.
    y_true = test_generator.classes

    # ------------------------------------------------------------------
    # THE FOUR MAIN SCORES
    # ------------------------------------------------------------------
    # average="weighted" means: work out the score for each species, then
    # take the average, giving more weight to species with more images.
    accuracy = accuracy_score(y_true, y_predicted)
    precision = precision_score(y_true, y_predicted, average="weighted", zero_division=0)
    recall = recall_score(y_true, y_predicted, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_predicted, average="weighted", zero_division=0)

    print(f"  Accuracy : {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall   : {recall:.4f}")
    print(f"  F1-score : {f1:.4f}")

    # ------------------------------------------------------------------
    # THE PER-SPECIES REPORT (a text table)
    # ------------------------------------------------------------------
    report_text = classification_report(
        y_true, y_predicted, target_names=class_names, zero_division=0
    )

    report_path = os.path.join(config.REPORTS_DIR, f"{model_name}_classification_report.txt")
    with open(report_path, "w") as f:
        f.write(f"Classification report for {model_name}\n")
        f.write("=" * 60 + "\n")
        f.write(report_text)

    # ------------------------------------------------------------------
    # THE CONFUSION MATRIX (a picture)
    # ------------------------------------------------------------------
    save_confusion_matrix(y_true, y_predicted, class_names, model_name)

    # Put everything in one dictionary and hand it back
    return {
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    }


def save_confusion_matrix(y_true, y_predicted, class_names, model_name):
    """
    Draw the confusion matrix and save it as a PNG.

    How to read it: each ROW is the true species, each COLUMN is what the
    model guessed. The numbers down the diagonal are the correct answers.
    Anything off the diagonal is a mistake.
    """
    matrix = confusion_matrix(y_true, y_predicted)

    # Make the picture bigger when there are more species
    plt.figure(figsize=(10, 8))

    sns.heatmap(
        matrix,
        annot=True,          # write the number inside each square
        fmt="d",             # show them as whole numbers
        cmap="Blues",        # dark blue = many images
        xticklabels=class_names,
        yticklabels=class_names,
    )

    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted species")
    plt.ylabel("True species")
    plt.xticks(rotation=45, ha="right")   # tilt long names so they fit
    plt.yticks(rotation=0)
    plt.tight_layout()                    # stop the labels being cut off

    save_path = os.path.join(config.PLOTS_DIR, f"{model_name}_confusion_matrix.png")
    plt.savefig(save_path, dpi=120)
    plt.close()                           # free the memory

    print(f"  Confusion matrix saved to: {save_path}")
