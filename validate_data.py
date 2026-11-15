"""
validate_data.py
----------------
Checks that the dataset is accurate and complete BEFORE you spend hours
training on it. The project brief asks for this under "Data validation".

Run it with:

    python validate_data.py

It answers four questions:

  1. Are all three folders (train / val / test) there, with the same species
     in each? If a species is missing from one split, the model can never be
     scored on it.
  2. Can every image file actually be opened? A corrupt JPEG will crash
     training halfway through, usually after an hour of waiting.
  3. Is the same image in two different splits? This is called DATA LEAKAGE
     and it is the most serious problem on this list. If a test image was
     also used for training, the model has already seen the answer and the
     test score is a lie.
  4. How many images does each species have? A species with very few images
     will score badly no matter how good the model is, and it is better to
     know that now than to be surprised by the results.

Nothing here changes any file. It only looks and reports.
"""

import collections
import hashlib
import os
import sys

from PIL import Image

from src import config


def file_fingerprint(path):
    """
    Return a short text 'fingerprint' of a file's contents.

    Two files with the same fingerprint contain exactly the same bytes, so
    they are the same picture. This is how we spot the same image sitting in
    two different folders. md5 is a standard way of producing such a
    fingerprint.
    """
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def check_folders_exist():
    """Question 1a: do train/, val/ and test/ exist at all?"""
    print("1. Checking the three folders exist ...")

    missing = []
    for folder in [config.TRAIN_DIR, config.VAL_DIR, config.TEST_DIR]:
        if not os.path.isdir(folder):
            missing.append(folder)

    if missing:
        print("   PROBLEM - these folders are missing:")
        for folder in missing:
            print(f"      {folder}")
        print("   Run prepare_dataset.py first, or unzip the dataset here.")
        return False

    print("   OK - train, val and test are all present.")
    return True


def check_same_species_everywhere():
    """Question 1b: does every split contain the same list of species?"""
    print("\n2. Checking all three splits have the same species ...")

    species_per_split = {}
    for name, folder in [("train", config.TRAIN_DIR),
                         ("val", config.VAL_DIR),
                         ("test", config.TEST_DIR)]:
        # set(...) makes an unordered collection we can compare easily
        species_per_split[name] = set(os.listdir(folder))

    everything = set()
    for names in species_per_split.values():
        everything = everything | names        # | means "join the two sets"

    problems = 0
    for split_name, names in species_per_split.items():
        missing = everything - names           # - means "what is in A but not B"
        if missing:
            problems += 1
            print(f"   PROBLEM - {split_name} is missing: {sorted(missing)}")

    if problems == 0:
        print(f"   OK - all three splits contain the same {len(everything)} species.")

    return problems == 0


def check_images_and_duplicates():
    """
    Questions 2, 3 and 4 in one pass over the files.

    We only want to read every image once, because there are over ten
    thousand of them, so all three checks happen inside the same loop.
    """
    print("\n3. Opening every image and looking for duplicates ...")

    # fingerprint -> list of places that exact image was found
    seen = collections.defaultdict(list)

    broken = []
    counts = collections.defaultdict(collections.Counter)

    for split_name, folder in [("train", config.TRAIN_DIR),
                               ("val", config.VAL_DIR),
                               ("test", config.TEST_DIR)]:

        for species in sorted(os.listdir(folder)):
            species_folder = os.path.join(folder, species)

            for file_name in os.listdir(species_folder):
                path = os.path.join(species_folder, file_name)
                counts[split_name][species] += 1

                try:
                    seen[file_fingerprint(path)].append(f"{split_name}/{species}/{file_name}")

                    # .verify() asks Pillow to decode the file and complain
                    # if it is damaged. It is faster than fully loading it.
                    Image.open(path).verify()

                except Exception as error:
                    broken.append((path, error))

    # ---- report: broken files ----
    if broken:
        print(f"   PROBLEM - {len(broken)} file(s) could not be opened:")
        for path, error in broken[:10]:
            print(f"      {path}  ({error})")
    else:
        print("   OK - every image file opened successfully.")

    # ---- report: leakage ----
    leaked = []
    duplicated_inside = 0

    for places in seen.values():
        if len(places) < 2:
            continue                       # appears once: nothing to say

        # places looks like ["train/trout/a.jpg", "test/trout/b.jpg"]
        # The bit before the first "/" is the split it was found in.
        splits_involved = {place.split("/")[0] for place in places}

        if len(splits_involved) > 1:
            leaked.append(places)
        else:
            duplicated_inside += 1

    if leaked:
        print(f"\n   SERIOUS PROBLEM - {len(leaked)} image(s) appear in more than")
        print("   one split. The test scores cannot be trusted while this is true.")
        for places in leaked[:5]:
            print(f"      {places}")
    else:
        print("   OK - no image appears in more than one split (no data leakage).")

    if duplicated_inside:
        print(f"   NOTE - {duplicated_inside} image(s) appear twice inside a single")
        print("   split. That is not leakage, it just means those pictures count twice.")

    # ---- report: counts ----
    print("\n4. Images per species:")
    all_species = sorted(counts["train"].keys())
    print(f"   {'species':<40} {'train':>7} {'val':>7} {'test':>7}")

    smallest_name, smallest_count = None, None
    for species in all_species:
        train_n = counts["train"][species]
        print(f"   {species:<40} {train_n:>7} "
              f"{counts['val'][species]:>7} {counts['test'][species]:>7}")

        if smallest_count is None or train_n < smallest_count:
            smallest_name, smallest_count = species, train_n

    total = sum(sum(c.values()) for c in counts.values())
    print(f"   {'TOTAL':<40} {sum(counts['train'].values()):>7} "
          f"{sum(counts['val'].values()):>7} {sum(counts['test'].values()):>7}")
    print(f"\n   {total} images in total.")

    # A class with very few images is worth warning about explicitly.
    average = sum(counts["train"].values()) / len(all_species)
    if smallest_count < average / 3:
        print(f"\n   WARNING - '{smallest_name}' has only {smallest_count} training")
        print(f"   images, far below the average of {average:.0f}. Expect its recall")
        print("   to be the weakest number in your results. Quote the weighted")
        print("   F1-score rather than plain accuracy because of this.")

    return len(broken) == 0 and len(leaked) == 0


def main():
    print("=" * 70)
    print("DATA VALIDATION")
    print("=" * 70)
    print(f"Looking in: {config.DATA_DIR}\n")

    if not check_folders_exist():
        sys.exit(1)

    ok_species = check_same_species_everywhere()
    ok_images = check_images_and_duplicates()

    print("\n" + "=" * 70)
    if ok_species and ok_images:
        print("RESULT: the dataset is complete and usable. Safe to train.")
    else:
        print("RESULT: problems found above. Fix them before training.")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    main()
