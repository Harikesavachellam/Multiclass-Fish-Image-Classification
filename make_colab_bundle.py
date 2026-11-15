"""
make_colab_bundle.py
--------------------
Makes a small zip of just the CODE, ready to upload to Google Colab.

Run it with:

    python make_colab_bundle.py

It writes `colab_bundle.zip` in this folder. Upload that file in Step 2,
Option B of Fish_Classification_Colab.ipynb.

Only use this if your project is not on GitHub yet. If it is, Option A in the
notebook (git clone) is easier and you never have to rebuild this zip.

The bundle deliberately leaves out:
  - data/    the images, which Colab downloads itself (261 MB)
  - models/  the .h5 files, which Colab is about to create
  - outputs/ the graphs and reports, same reason
so the zip stays tiny - a few tens of kilobytes.
"""

import os
import zipfile

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_PATH = os.path.join(PROJECT_DIR, "colab_bundle.zip")

# The files and folders Colab actually needs in order to train
THINGS_TO_INCLUDE = [
    "src",                   # the whole library folder
    "train_all_models.py",   # the main training script
    "prepare_dataset.py",    # in case the dataset ever arrives unsplit
    "make_report.py",        # writes the comparison report
    "requirements.txt",
    "README.md",
]

# File types that should never go in, even if they are inside src/
SKIP_EXTENSIONS = (".pyc", ".h5", ".keras", ".pkl", ".zip")


def should_include(path):
    """Decide whether one file belongs in the bundle."""
    if "__pycache__" in path:
        return False
    if path.lower().endswith(SKIP_EXTENSIONS):
        return False
    return True


def add_folder(zip_file, folder_name):
    """Add every file inside a folder, keeping the folder structure."""
    folder_path = os.path.join(PROJECT_DIR, folder_name)

    # os.walk visits the folder and every folder inside it
    for current_folder, _subfolders, file_names in os.walk(folder_path):
        for file_name in file_names:
            full_path = os.path.join(current_folder, file_name)

            if not should_include(full_path):
                continue

            # The path to store inside the zip, relative to the project folder
            name_in_zip = os.path.relpath(full_path, PROJECT_DIR)
            zip_file.write(full_path, name_in_zip)
            print(f"  added {name_in_zip}")


def main():
    print("Building colab_bundle.zip ...\n")

    # ZIP_DEFLATED means "compress it", not just "store it"
    with zipfile.ZipFile(BUNDLE_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for thing in THINGS_TO_INCLUDE:
            full_path = os.path.join(PROJECT_DIR, thing)

            if not os.path.exists(full_path):
                print(f"  SKIPPED (not found): {thing}")
                continue

            if os.path.isdir(full_path):
                add_folder(zip_file, thing)
            else:
                zip_file.write(full_path, thing)
                print(f"  added {thing}")

    size_kb = os.path.getsize(BUNDLE_PATH) / 1024
    print(f"\nDone: {BUNDLE_PATH}")
    print(f"Size: {size_kb:.0f} KB")
    print("\nUpload this file in Step 2, Option B of the Colab notebook.")


if __name__ == "__main__":
    main()
