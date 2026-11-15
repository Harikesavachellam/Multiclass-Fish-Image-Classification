"""
prepare_dataset.py
------------------
Run this ONCE, before training, to get the images into the folder shape
that Keras needs.

Run it like this:

    python prepare_dataset.py --source "C:/path/to/the/unzipped/dataset"

What it does:
  - looks inside the folder you gave it
  - if it already contains train / val / test, it just copies them to data/
  - if it only contains species folders, it splits them 70% train,
    15% validation, 15% test
  - prints how many images ended up in each folder
"""

import argparse
import os
import random
import shutil

from src import config

# The file types we accept as images
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")

# How to split the images when the dataset is not already split
TRAIN_SHARE = 0.70
VAL_SHARE = 0.15
# whatever is left (15%) becomes the test set


def list_images(folder):
    """Return the names of all image files directly inside one folder."""
    names = []
    for file_name in os.listdir(folder):
        if file_name.lower().endswith(IMAGE_EXTENSIONS):
            names.append(file_name)
    return names


def list_subfolders(folder):
    """Return the names of all folders directly inside one folder."""
    names = []
    for name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, name)):
            names.append(name)
    return sorted(names)


def find_dataset_root(start_folder):
    """
    Zip files often unpack with an extra wrapper folder, like:
        extracted/Dataset/train/...
    This walks down through single-folder wrappers until it finds the
    folder that actually holds the data.
    """
    current = start_folder

    # Keep going down while this folder holds exactly one folder and no images
    while True:
        subfolders = list_subfolders(current)
        images_here = list_images(current)

        if len(subfolders) == 1 and len(images_here) == 0:
            current = os.path.join(current, subfolders[0])
        else:
            return current


def copy_split_folders(source_root):
    """
    The dataset is already divided into train / val / test.
    Copy each one into our data/ folder.
    """
    print("The dataset is already split. Copying it into data/ ...")

    # the names the dataset might use -> the name we want
    name_map = {
        "train": config.TRAIN_DIR,
        "training": config.TRAIN_DIR,
        "val": config.VAL_DIR,
        "valid": config.VAL_DIR,
        "validation": config.VAL_DIR,
        "test": config.TEST_DIR,
        "testing": config.TEST_DIR,
    }

    for folder_name in list_subfolders(source_root):
        target = name_map.get(folder_name.lower())

        if target is None:
            continue    # a folder we do not recognise - skip it

        source = os.path.join(source_root, folder_name)

        # If we already copied something there before, remove it first
        if os.path.exists(target):
            shutil.rmtree(target)

        print(f"  copying {folder_name} -> {os.path.basename(target)}")
        shutil.copytree(source, target)


def split_class_folders(source_root):
    """
    The dataset is just species folders, with no train/val/test.
    Split every species 70 / 15 / 15.
    """
    print("The dataset is not split. Splitting it 70% / 15% / 15% ...")

    species_folders = list_subfolders(source_root)

    # Same shuffle every time, so the split is repeatable
    random.seed(config.RANDOM_SEED)

    for species in species_folders:
        species_folder = os.path.join(source_root, species)
        image_names = list_images(species_folder)

        if len(image_names) == 0:
            print(f"  skipping '{species}' - no images found")
            continue

        random.shuffle(image_names)

        # Work out where to cut the list
        total = len(image_names)
        train_cut = int(total * TRAIN_SHARE)
        val_cut = int(total * (TRAIN_SHARE + VAL_SHARE))

        # Python slicing: [start:stop]
        groups = {
            config.TRAIN_DIR: image_names[:train_cut],
            config.VAL_DIR: image_names[train_cut:val_cut],
            config.TEST_DIR: image_names[val_cut:],
        }

        for target_root, names in groups.items():
            target_folder = os.path.join(target_root, species)
            os.makedirs(target_folder, exist_ok=True)

            for file_name in names:
                shutil.copyfile(
                    os.path.join(species_folder, file_name),
                    os.path.join(target_folder, file_name),
                )

        print(f"  {species}: {train_cut} train, {val_cut - train_cut} val, "
              f"{total - val_cut} test")


def print_summary():
    """Print how many images are now in each split, for each species."""
    print("\n" + "=" * 60)
    print("FINAL DATASET")
    print("=" * 60)

    for split_name, split_folder in [
        ("train", config.TRAIN_DIR),
        ("val", config.VAL_DIR),
        ("test", config.TEST_DIR),
    ]:
        if not os.path.exists(split_folder):
            print(f"{split_name}: MISSING")
            continue

        total = 0
        print(f"\n{split_name}:")
        for species in list_subfolders(split_folder):
            count = len(list_images(os.path.join(split_folder, species)))
            total += count
            print(f"   {species:<35} {count:>6}")
        print(f"   {'TOTAL':<35} {total:>6}")


def main():
    parser = argparse.ArgumentParser(description="Prepare the fish dataset")
    parser.add_argument(
        "--source",
        required=True,
        help="Folder where you unzipped the downloaded dataset",
    )
    arguments = parser.parse_args()

    if not os.path.isdir(arguments.source):
        raise SystemExit(f"That folder does not exist: {arguments.source}")

    # Make sure data/ exists
    os.makedirs(config.DATA_DIR, exist_ok=True)

    # Step down through any wrapper folders
    source_root = find_dataset_root(arguments.source)
    print(f"Reading the dataset from: {source_root}")

    # What is inside? (lower-cased, so "Train" and "train" both match)
    inside = [name.lower() for name in list_subfolders(source_root)]

    already_split = "train" in inside or "training" in inside

    if already_split:
        copy_split_folders(source_root)
    else:
        split_class_folders(source_root)

    # If the dataset had train and test but no val, borrow from test
    if not os.path.exists(config.VAL_DIR) and os.path.exists(config.TEST_DIR):
        print("\nNo validation folder found - using a copy of the test folder.")
        shutil.copytree(config.TEST_DIR, config.VAL_DIR)

    print_summary()
    print("\nDone. You can now run:  python train_all_models.py")


if __name__ == "__main__":
    main()
