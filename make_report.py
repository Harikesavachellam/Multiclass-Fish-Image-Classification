"""
make_report.py
--------------
Writes the comparison report: the table of every model's scores plus a few
sentences of insight, in plain Markdown.

Run it AFTER train_all_models.py has finished:

    python make_report.py

It writes:
  outputs/reports/comparison_report.md
and it also drops the same table into the Results section of README.md,
between the RESULTS_START and RESULTS_END markers.
"""

import json
import os

import pandas as pd

from src import config

CSV_PATH = os.path.join(config.REPORTS_DIR, "model_comparison.csv")
REPORT_PATH = os.path.join(config.REPORTS_DIR, "comparison_report.md")
README_PATH = os.path.join(config.PROJECT_DIR, "README.md")

# The two markers in README.md that we replace between
START_MARKER = "<!-- RESULTS_START -->"
END_MARKER = "<!-- RESULTS_END -->"


def load_results():
    """Read the comparison CSV that train_all_models.py wrote."""
    if not os.path.exists(CSV_PATH):
        raise SystemExit(
            f"\n{CSV_PATH} does not exist.\n"
            "Run 'python train_all_models.py' first."
        )

    table = pd.read_csv(CSV_PATH)
    # Best model first
    return table.sort_values("accuracy", ascending=False).reset_index(drop=True)


def make_markdown_table(table):
    """Turn the results table into a Markdown table, rounded to 4 decimals."""
    pretty = table.copy()

    # Round the four score columns so the table is readable
    for column in ["accuracy", "precision", "recall", "f1_score"]:
        if column in pretty.columns:
            pretty[column] = pretty[column].round(4)

    # Give the columns nicer headings
    pretty = pretty.rename(
        columns={
            "model": "Model",
            "accuracy": "Accuracy",
            "precision": "Precision",
            "recall": "Recall",
            "f1_score": "F1-score",
            "training_minutes": "Training (min)",
            "epochs_run": "Epochs",
        }
    )

    return pretty.to_markdown(index=False)


def write_insights(table):
    """
    Build a few sentences of insight from the numbers.

    Nothing here is hand-written about a particular model - every sentence
    is generated from the table, so the report is always true.
    """
    lines = []

    best = table.iloc[0]        # first row = highest accuracy
    worst = table.iloc[-1]      # last row = lowest accuracy

    lines.append(
        f"- **Best model: {best['model']}** with an accuracy of "
        f"{best['accuracy']:.4f} and an F1-score of {best['f1_score']:.4f}. "
        f"This is the model saved as `models/best_model.h5` and used by the "
        f"Streamlit app."
    )

    lines.append(
        f"- **Weakest model: {worst['model']}** with an accuracy of "
        f"{worst['accuracy']:.4f}."
    )

    gap = best["accuracy"] - worst["accuracy"]
    lines.append(
        f"- The gap between the best and the weakest model is "
        f"{gap:.4f} ({gap * 100:.1f} percentage points)."
    )

    # Compare the from-scratch CNN against the transfer-learning models
    scratch_rows = table[table["model"] == "CNN_Scratch"]
    transfer_rows = table[table["model"] != "CNN_Scratch"]

    if len(scratch_rows) > 0 and len(transfer_rows) > 0:
        scratch_accuracy = scratch_rows.iloc[0]["accuracy"]
        transfer_average = transfer_rows["accuracy"].mean()
        difference = transfer_average - scratch_accuracy

        if difference > 0:
            lines.append(
                f"- Transfer learning clearly helped: the five pre-trained models "
                f"averaged {transfer_average:.4f} accuracy against "
                f"{scratch_accuracy:.4f} for the CNN trained from scratch, a "
                f"difference of {difference:.4f}."
            )
        else:
            lines.append(
                f"- The from-scratch CNN ({scratch_accuracy:.4f}) matched or beat the "
                f"average of the pre-trained models ({transfer_average:.4f}). With a "
                f"small or very distinctive dataset this can happen, but it is worth "
                f"training for more epochs before trusting it."
            )

    # Was the fastest model also the most accurate?
    if "training_minutes" in table.columns:
        fastest = table.sort_values("training_minutes").iloc[0]
        lines.append(
            f"- Fastest to train: **{fastest['model']}** at "
            f"{fastest['training_minutes']} minutes."
        )

        if fastest["model"] != best["model"]:
            lines.append(
                f"- {best['model']} is the most accurate but took "
                f"{best['training_minutes']} minutes, against "
                f"{fastest['training_minutes']} for {fastest['model']}. If "
                f"prediction speed or retraining cost mattered more than the last "
                f"fraction of accuracy, {fastest['model']} would be the practical "
                f"choice."
            )

    # Did early stopping cut anything short?
    if "epochs_run" in table.columns:
        stopped_early = table[table["epochs_run"] < config.EPOCHS]
        if len(stopped_early) > 0:
            names = ", ".join(stopped_early["model"].tolist())
            lines.append(
                f"- EarlyStopping ended training before the full {config.EPOCHS} "
                f"epochs for: {names}. Those models had stopped improving on the "
                f"validation set."
            )

    return "\n".join(lines)


def update_readme(results_block):
    """Paste the results block into README.md between the two markers."""
    if not os.path.exists(README_PATH):
        print("README.md not found - skipping that part.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    if START_MARKER not in text or END_MARKER not in text:
        print("Markers not found in README.md - skipping that part.")
        return

    # Keep everything before the start marker and after the end marker
    before = text.split(START_MARKER)[0]
    after = text.split(END_MARKER)[1]

    new_text = before + START_MARKER + "\n\n" + results_block + "\n\n" + END_MARKER + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_text)

    print(f"README.md updated: {README_PATH}")


def main():
    table = load_results()

    markdown_table = make_markdown_table(table)
    insights = write_insights(table)

    # The block that goes into both files
    results_block = markdown_table + "\n\n### Insights\n\n" + insights

    # 1. the standalone report
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Model Comparison Report\n\n")
        f.write("All six models were trained on the same images, with the same ")
        f.write("augmentation, and scored on the same unseen test set.\n\n")
        f.write(results_block)
        f.write("\n\n### Where the supporting files are\n\n")
        f.write("- Training curves: `outputs/plots/<model>_training_history.png`\n")
        f.write("- Confusion matrices: `outputs/plots/<model>_confusion_matrix.png`\n")
        f.write("- Per-species scores: `outputs/reports/<model>_classification_report.txt`\n")
        f.write("- Comparison chart: `outputs/plots/model_comparison.png`\n")

    print(f"Report written: {REPORT_PATH}")

    # 2. the same block inside the README
    update_readme(results_block)

    print("\n" + markdown_table)


if __name__ == "__main__":
    main()
