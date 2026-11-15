"""
visualize.py
------------
All the graph-drawing code lives here.

Two kinds of graph:
  1. Training history - how accuracy and loss changed over the epochs
  2. Model comparison - a bar chart putting all six models side by side
"""

import os

import matplotlib
matplotlib.use("Agg")       # save graphs as files instead of opening windows
import matplotlib.pyplot as plt
import pandas as pd

from src import config


def plot_training_history(history_dict, model_name):
    """
    Draw two graphs side by side for one model:
      LEFT  = accuracy going up over the epochs
      RIGHT = loss going down over the epochs

    If the blue (train) line keeps improving but the orange (validation)
    line gets worse, the model is OVERFITTING - memorising instead of learning.
    """

    # 1 row, 2 columns of graphs
    figure, (left_graph, right_graph) = plt.subplots(1, 2, figsize=(13, 5))

    # ---------------- accuracy ----------------
    left_graph.plot(history_dict["accuracy"], label="Training accuracy", marker="o")
    left_graph.plot(history_dict["val_accuracy"], label="Validation accuracy", marker="o")
    left_graph.set_title(f"{model_name} - Accuracy")
    left_graph.set_xlabel("Epoch")
    left_graph.set_ylabel("Accuracy")
    left_graph.legend()
    left_graph.grid(True, alpha=0.3)   # faint grid lines, easier to read

    # ---------------- loss ----------------
    right_graph.plot(history_dict["loss"], label="Training loss", marker="o")
    right_graph.plot(history_dict["val_loss"], label="Validation loss", marker="o")
    right_graph.set_title(f"{model_name} - Loss")
    right_graph.set_xlabel("Epoch")
    right_graph.set_ylabel("Loss")
    right_graph.legend()
    right_graph.grid(True, alpha=0.3)

    plt.tight_layout()

    save_path = os.path.join(config.PLOTS_DIR, f"{model_name}_training_history.png")
    plt.savefig(save_path, dpi=120)
    plt.close()

    print(f"  Training history graph saved to: {save_path}")


def plot_model_comparison(results_list):
    """
    Draw one bar chart comparing every model on all four metrics.

    Args:
        results_list: a list of the dictionaries returned by evaluate_model()
    """

    # Turn the list of dictionaries into a table (a pandas DataFrame)
    table = pd.DataFrame(results_list)

    # Sort so the best model is on the left
    table = table.sort_values("accuracy", ascending=False)

    # Use the model name as the row label, keep only the four score columns
    chart_data = table.set_index("model")[["accuracy", "precision", "recall", "f1_score"]]

    chart_data.plot(kind="bar", figsize=(12, 6))

    plt.title("Model comparison - all metrics")
    plt.xlabel("Model")
    plt.ylabel("Score (0 to 1)")
    plt.ylim(0, 1.05)                     # scores can never go above 1
    plt.xticks(rotation=30, ha="right")
    plt.legend(loc="lower right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    save_path = os.path.join(config.PLOTS_DIR, "model_comparison.png")
    plt.savefig(save_path, dpi=120)
    plt.close()

    print(f"Comparison chart saved to: {save_path}")
    return table


def plot_class_distribution(generator, class_names, title, file_name):
    """
    Draw a bar chart of how many images each species has.
    Useful to show whether the dataset is balanced or not.
    """
    # generator.classes is a long list like [0,0,0,1,1,2,2,2,...]
    counts = pd.Series(generator.classes).value_counts().sort_index()

    plt.figure(figsize=(11, 5))
    plt.bar(class_names, counts.values, color="steelblue")
    plt.title(title)
    plt.xlabel("Species")
    plt.ylabel("Number of images")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    save_path = os.path.join(config.PLOTS_DIR, file_name)
    plt.savefig(save_path, dpi=120)
    plt.close()

    print(f"Class distribution chart saved to: {save_path}")
