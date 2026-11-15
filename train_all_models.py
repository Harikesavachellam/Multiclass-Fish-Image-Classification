"""
train_all_models.py
-------------------
THIS IS THE MAIN SCRIPT. Run it like this:

    python train_all_models.py

What it does, in order:
  1. loads the fish images
  2. trains all six models, one after another
  3. tests each model and writes down its scores
  4. draws all the graphs
  5. saves a comparison table
  6. copies the BEST model to models/best_model.h5

You can also train just one model, which is handy for testing:

    python train_all_models.py --model MobileNet
"""

import argparse
import json
import os
import shutil

import pandas as pd

from src import config
from src import evaluate
from src import train
from src import visualize


def main():
    # ------------------------------------------------------------------
    # STEP 0: read the command line
    # ------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Train fish classification models")
    parser.add_argument(
        "--model",
        default="all",
        help="Which model(s) to train: 'all' (default), one name, or several "
             "names separated by commas, e.g. MobileNet,ResNet50",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Override the number of epochs from config.py",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=None,
        help="Override the EarlyStopping patience from config.py",
    )
    parser.add_argument(
        "--retrain",
        action="store_true",
        help="Train a model again even if it is already in the results CSV. "
             "Without this flag, finished models are skipped so a stopped run "
             "can be resumed where it left off.",
    )
    arguments = parser.parse_args()

    # If the user asked for different settings, change them now. Every other
    # module reads these values when it uses them, so changing them here
    # changes the behaviour of the whole program.
    if arguments.epochs is not None:
        config.EPOCHS = arguments.epochs

    if arguments.patience is not None:
        config.EARLY_STOPPING_PATIENCE = arguments.patience

    # Decide which models to train
    if arguments.model == "all":
        models_to_train = config.MODEL_NAMES
    else:
        # .split(",") turns "MobileNet,ResNet50" into ["MobileNet", "ResNet50"]
        # .strip() removes any stray spaces the user typed
        models_to_train = [name.strip() for name in arguments.model.split(",")]

    # Make sure models/ and outputs/ exist
    config.create_output_folders()

    # ------------------------------------------------------------------
    # STEP 1: load the images
    # ------------------------------------------------------------------
    print("\nLoading the fish images ...")
    train_gen, val_gen, test_gen, class_names = train.load_data()

    print(f"\nFound {len(class_names)} species:")
    for position, name in enumerate(class_names):
        print(f"  {position}: {name}")

    print(f"\nTraining images  : {train_gen.samples}")
    print(f"Validation images: {val_gen.samples}")
    print(f"Test images      : {test_gen.samples}")

    # Save the class names. The Streamlit app reads this file so that it
    # knows which name belongs to which output number.
    class_names_path = os.path.join(config.MODELS_DIR, "class_names.json")
    with open(class_names_path, "w") as f:
        json.dump(class_names, f, indent=2)

    # A quick chart showing how many images each species has
    visualize.plot_class_distribution(
        train_gen, class_names, "Training images per species", "class_distribution.png"
    )

    # ------------------------------------------------------------------
    # STEP 2: train and evaluate every model
    # ------------------------------------------------------------------
    # Pick up any models that were already finished in an earlier run.
    # This is what makes a long training job resumable: if it is stopped
    # after model three, starting it again carries on from model four.
    all_results = load_previous_results()

    if len(all_results) > 0:
        finished = [row["model"] for row in all_results]
        print(f"\nAlready finished in an earlier run: {', '.join(finished)}")

    for model_name in models_to_train:

        # Skip a model we already have results for, unless --retrain was given
        already_done = any(row["model"] == model_name for row in all_results)
        if already_done and not arguments.retrain:
            print(f"\nSkipping {model_name} - already trained. "
                  f"Use --retrain to train it again.")
            continue

        # --- train ---
        history_dict, model_path, train_minutes = train.train_one_model(
            model_name, train_gen, val_gen
        )

        # --- draw its accuracy / loss graphs ---
        visualize.plot_training_history(history_dict, model_name)

        # --- test it and collect the scores ---
        scores = evaluate.evaluate_model(model_path, test_gen, class_names, model_name)
        scores["training_minutes"] = round(train_minutes, 1)
        scores["epochs_run"] = len(history_dict["accuracy"])

        all_results.append(scores)

        # Save the results so far. If training crashes on model 5, we still
        # have the results of models 1 to 4.
        save_results_table(all_results)

    # ------------------------------------------------------------------
    # STEP 3: compare the models and pick the winner
    # ------------------------------------------------------------------
    if len(all_results) > 1:
        comparison_table = visualize.plot_model_comparison(all_results)
    else:
        comparison_table = pd.DataFrame(all_results)

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)
    print(comparison_table.to_string(index=False))

    # max() with key=... finds the dictionary with the highest accuracy
    best = max(all_results, key=lambda row: row["accuracy"])
    print(f"\nBEST MODEL: {best['model']}  (accuracy {best['accuracy']:.4f})")

    # Copy the winner to a fixed name, so the Streamlit app always knows
    # which file to load.
    best_source = os.path.join(config.MODELS_DIR, f"{best['model']}.h5")
    best_target = os.path.join(config.MODELS_DIR, "best_model.h5")
    shutil.copyfile(best_source, best_target)
    print(f"Copied to: {best_target}")

    # Remember the winner's name for the app and the report
    with open(os.path.join(config.MODELS_DIR, "best_model_name.txt"), "w") as f:
        f.write(best["model"])


def results_csv_path():
    """The one place the comparison CSV path is written down."""
    return os.path.join(config.REPORTS_DIR, "model_comparison.csv")


def save_results_table(all_results):
    """Write the scores of every model so far to a CSV file."""
    table = pd.DataFrame(all_results)
    table.to_csv(results_csv_path(), index=False)


def load_previous_results():
    """
    Read the results of models trained in an earlier run, if there are any.

    Returns a list of dictionaries - the same shape evaluate_model() produces -
    so the rest of the script cannot tell the difference between a result
    loaded from disk and one just calculated.
    """
    csv_path = results_csv_path()

    if not os.path.exists(csv_path):
        return []        # nothing from before: start with an empty list

    table = pd.read_csv(csv_path)

    # to_dict("records") turns each row of the table into a dictionary
    return table.to_dict("records")


# This line means: only run main() when the file is executed directly
# (python train_all_models.py), not when it is imported by another file.
if __name__ == "__main__":
    main()
