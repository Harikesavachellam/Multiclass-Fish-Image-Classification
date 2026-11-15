# Requirements check

Every requirement from the project brief, where it is implemented, and how it
was verified. Re-verified on **15 November 2026**, after all six models had
finished training on the real dataset.

Status key:
**DONE** = implemented and verified by actually running it ·
**GAP** = a real shortfall against the wording of the brief ·
**YOURS** = not a coding task, you have to do it

---

## Problem statement

| Requirement | Where | Status |
|---|---|---|
| Classify fish images into multiple categories | whole project | **DONE** — 11 species, 98.15% test accuracy |
| Train a CNN from scratch | `src/models.py` → `build_cnn_from_scratch()` | **DONE** — trained 10 epochs, 92.21% |
| Transfer learning with pre-trained models | `src/models.py` → `build_pretrained_model()` | **DONE** — all 5 trained and scored |
| Save models for later use | `src/train.py` → `ModelCheckpoint` | **DONE** — all 7 `.h5` files verified to load back |
| Deploy a Streamlit app predicting from uploaded images | `app.py` | **DONE** — launched, loads MobileNet, uploader renders |

## Approach — data preprocessing and augmentation

| Requirement | Where | Status |
|---|---|---|
| Rescale images to [0, 1] | `src/data_loader.py`, `rescale=1.0/255` on all three generators | **DONE** |
| Rotation | `rotation_range=20` | **DONE** |
| Zoom | `zoom_range=0.2` | **DONE** |
| Flipping | `horizontal_flip=True` | **DONE** |
| (extra) width/height shift, shear | `width_shift_range`, `height_shift_range`, `shear_range` | **DONE** |
| Loaded using `ImageDataGenerator` | `src/data_loader.py` | **DONE** — verified on TensorFlow 2.21 / Keras 3.15 |

Augmentation is applied to the training set only. Validation and test images are
rescaled but never distorted, so the reported scores describe real photographs.
`shuffle=False` is set on the test generator — verified — which is what keeps
each prediction lined up with its true label in `evaluate.py`.

## Approach — model training

| Requirement | Where | Status |
|---|---|---|
| Train a CNN model from scratch | `build_cnn_from_scratch()` — 4 Conv2D+MaxPooling blocks, Flatten, Dense(256), Dropout(0.5), softmax | **DONE** |
| Five pre-trained models | `config.MODEL_NAMES` + `models.PRETRAINED_MODELS` | **DONE** |
| → VGG16 | `tensorflow.keras.applications.VGG16` | **DONE** — 0.6931 |
| → ResNet50 | `tensorflow.keras.applications.ResNet50` | **DONE** — 0.1648, see note below |
| → MobileNet | `tensorflow.keras.applications.MobileNet` | **DONE** — 0.9815, the winner |
| → InceptionV3 | `tensorflow.keras.applications.InceptionV3` | **DONE** — 0.9650 |
| → EfficientNetB0 | `+ Rescaling(255.0)` fix | **DONE** — 0.9553 |
| **"Fine-tune the pre-trained models on the fish dataset"** | `src/models.py:149`, `base_model.trainable = False` | **GAP** — see below |
| Save the max-accuracy model in .h5 | `train_all_models.py` copies the winner to `models/best_model.h5` | **DONE** — verified identical to `MobileNet.h5` |

### GAP: frozen base, so this is feature extraction rather than fine-tuning

The brief says *"Fine-tune the pre-trained models on the fish dataset."*

What the code actually does is freeze the entire pre-trained base
(`base_model.trainable = False`) and train only a new classification head on
top. In the strict vocabulary of transfer learning that is **feature
extraction**, not **fine-tuning**. Fine-tuning means unfreezing some of the
pre-trained layers and continuing to train them at a very low learning rate.

Two honest ways to read this:

* The loose reading — "fine-tune" is used casually to mean "adapt a pre-trained
  model to your data", which is exactly what happens here, and the results
  (98.15%) show it worked.
* The strict reading — an evaluator who knows the distinction may ask why no
  layers were unfrozen. **Be ready for that question.**

This gap is also the most likely cause of the ResNet50 result below, so fixing
it would probably fix two things at once.

### Note: ResNet50 scored 0.1648

The random baseline for 11 classes is 0.0909, so ResNet50 barely cleared
chance. This is the known behaviour of a frozen ResNet50: its
BatchNormalization layers keep using the mean and variance they learned from
ImageNet, which do not match this dataset, so the features reaching the new
head are badly scaled. Unfreezing the base — the fix for the gap above — is
the standard remedy.

It is kept in the results rather than hidden. A model that failed, with a
diagnosis, is a better thing to discuss in a live evaluation than a table where
everything quietly worked.

## Approach — model evaluation

| Requirement | Where | Status |
|---|---|---|
| Accuracy | `evaluate.py` → `accuracy_score` | **DONE** — independently recomputed as 0.9815 |
| Precision | `precision_score(average="weighted")` | **DONE** |
| Recall | `recall_score(average="weighted")` | **DONE** |
| F1-score | `f1_score(average="weighted")` | **DONE** — independently recomputed as 0.9803 |
| Confusion matrix | `save_confusion_matrix()` | **DONE** — 6 PNGs in `outputs/plots/` |
| Compared across all models | `model_comparison.csv` + `model_comparison.png` | **DONE** — all 6 models |
| Visualize training history (accuracy and loss) | `visualize.plot_training_history()` | **DONE** — 6 PNGs |

The metrics were re-derived from `best_model.h5` using a separate script that
does not import `evaluate.py`, and matched the published numbers to four
decimal places. So the comparison table is not quoting itself.

## Approach — deployment

| Requirement | Where | Status |
|---|---|---|
| Allow users to upload fish images | `st.file_uploader` in `app.py` | **DONE** — uploader rendered in a real browser |
| Predict and display the fish category | `st.success` with the predicted species | **DONE** — 10 of 11 species correctly identified through the app's exact preprocessing path |
| Provide model confidence scores | `st.metric` + bar chart + per-species table | **DONE** |

## Documentation and deliverables

| Deliverable | Where | Status |
|---|---|---|
| Trained models in .h5 or .pkl | `models/*.h5` | **DONE** — 7 files, all verified loadable |
| Streamlit application | `app.py` | **DONE** |
| Python scripts for training, evaluation, deployment | `train_all_models.py`, `src/train.py`, `src/evaluate.py`, `app.py` | **DONE** |
| Comparison report — metrics and insights | `outputs/reports/comparison_report.md` | **DONE** — includes the unequal-epoch disclosure |
| Comprehensive documentation of approach, code and evaluation | `README.md` + the 61-page line-by-line PDF in `docs/` | **DONE** |
| GitHub repository, well documented | `README.md` written, `.gitignore` ready; repo not created | **YOURS** |

## Project guidelines

| Guideline | How it is met | Status |
|---|---|---|
| Consistent naming conventions | `snake_case` functions and variables throughout, PEP 8 | **DONE** |
| Modular code | all reusable logic in `src/`, each module one job, no duplication | **DONE** |
| **Data validation — data accurate and complete** | `validate_data.py` | **DONE** — added 15 Nov 2026 after this check found it missing |
| Maintainable | every setting in `src/config.py`; adding a model is one line in `PRETRAINED_MODELS` | **DONE** |
| Portable (same on every OS) | no hardcoded absolute paths anywhere; all paths built with `os.path.join` from `__file__` | **DONE** — verified by grep |
| PEP 8 | docstring on every module and function, 4-space indent | **DONE** |

### What `validate_data.py` reported

```
11 species present in all three splits
10,514 images, 0 unreadable
0 images appear in more than one split  <- no data leakage
10 duplicate images inside a single split (harmless)
WARNING: 'animal fish bass' has 30 training images vs an average of 566
```

**The leakage check is the important one.** It confirms no test image was also
used for training, which is what makes the 98.15% a real number rather than a
memorised one.

## Mandatory items that are yours, not the code's

| Item | Status |
|---|---|
| Maintain the code on GitHub | **YOURS** |
| Keep the repo public | **YOURS** |
| Proper README with workflow and execution | code side **DONE** — `README.md` is written and complete; pushing it is **YOURS** |
| Demo video of the working model, posted on LinkedIn | **YOURS** — record the Streamlit app, not the notebook |

---

## Summary

Every requirement in the brief is implemented and verified, with **one genuine
gap**: the pre-trained bases are frozen, so the project does feature extraction
rather than strict fine-tuning. Everything else — including the parts most
likely to be silently wrong, like data leakage and whether the published
metrics actually reproduce — was tested and passed.
