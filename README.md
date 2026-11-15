# 🐟 Multiclass Fish Image Classification

Classify fish images into their species using deep learning — a CNN built from
scratch plus five pre-trained models, compared side by side, with the winner
deployed in a Streamlit web app.

---

## 1. Problem statement

Given a photo of a fish, predict which species it is.

The project trains six different models on the same dataset, measures them with
the same metrics, picks the best one, and serves it through a web app where
anyone can upload a photo and get a prediction with confidence scores.

## 2. Business use cases

| # | Use case | How this project delivers it |
|---|---|---|
| 1 | **Enhanced accuracy** — find the best architecture | Six models trained and scored on identical data |
| 2 | **Deployment ready** — real-time predictions | Streamlit app (`app.py`) that takes an upload and answers instantly |
| 3 | **Model comparison** — pick the right approach | `outputs/reports/model_comparison.csv` + a comparison bar chart |

## 3. Skills used

Deep Learning · Python · TensorFlow/Keras · Streamlit · Data Preprocessing ·
Transfer Learning · Model Evaluation · Visualization · Model Deployment

---

## 4. Project structure

```
multiclass_fish_classification/
│
├── src/                         <- all the reusable code (modular programming)
│   ├── config.py                <- every setting in one place
│   ├── data_loader.py           <- reads images, augments them
│   ├── models.py                <- builds the CNN + the 5 pre-trained models
│   ├── train.py                 <- trains ONE model and saves it
│   ├── evaluate.py              <- accuracy, precision, recall, F1, confusion matrix
│   └── visualize.py             <- all the graphs
│
├── prepare_dataset.py           <- STEP 1: arrange the downloaded images
├── validate_data.py             <- STEP 1b: check the data is complete, no leakage
├── train_all_models.py          <- STEP 2: train + evaluate all six models
├── app.py                       <- STEP 3: the Streamlit web app
├── make_report.py               <- writes the comparison report + fills in this README
├── make_colab_bundle.py         <- zips just the code, for uploading to Colab
├── Fish_Classification_Colab.ipynb  <- train on a free Colab GPU (same code)
├── make_code_pdf.py             <- builds the line-by-line code explanation PDF
│
├── data/                        <- the images (not in git, you download them)
│   ├── train/<species>/*.png
│   ├── val/<species>/*.png
│   └── test/<species>/*.png
│
├── models/                      <- saved .h5 models (not in git)
│   ├── CNN_Scratch.h5 ... EfficientNetB0.h5
│   ├── best_model.h5            <- the winner, used by the app
│   └── class_names.json
│
├── outputs/
│   ├── plots/                   <- training curves, confusion matrices, comparison chart
│   └── reports/                 <- per-model classification reports + comparison CSV
│
├── docs/                        <- the generated code-explanation PDF
├── requirements.txt
└── README.md
```

---

## 5. Workflow (what happens, in order)

```
   Download dataset (Google Drive zip)
                │
                ▼
   prepare_dataset.py ──► data/train, data/val, data/test  (70% / 15% / 15%)
                │
                ▼
   data_loader.py ──► rescale to [0,1] + augment (rotate, zoom, flip, shift)
                │
                ▼
   models.py ──► CNN from scratch │ VGG16 │ ResNet50 │ MobileNet │ InceptionV3 │ EfficientNetB0
                │                   (pre-trained bases frozen, new head trained)
                ▼
   train.py ──► model.fit() with EarlyStopping + ModelCheckpoint ──► models/<name>.h5
                │
                ▼
   evaluate.py ──► accuracy · precision · recall · F1 · confusion matrix (on the TEST set)
                │
                ▼
   visualize.py ──► training curves + comparison bar chart
                │
                ▼
   best model copied to models/best_model.h5
                │
                ▼
   app.py (Streamlit) ──► upload a photo ──► species + confidence scores
```

---

## 6. How to run it

### Step 0 — install

```bash
pip install -r requirements.txt
```

### Step 1 — get the dataset

Download the dataset zip from the project's Google Drive link (261 MB) and
unzip it. It already contains a `data/` folder split into `train`, `val` and
`test`, so unzipping it straight into the project root puts everything exactly
where it belongs.

If your copy arrives **unsplit** — just species folders, no train/test — run
this instead and it will create a 70/15/15 split for you:

```bash
python prepare_dataset.py --source "C:/path/to/the/unzipped/folder"
```

#### What is in the dataset

11 species, 10,514 JPEG images:

| Species | Train | Val | Test |
|---|---:|---:|---:|
| animal fish | 1096 | 187 | 527 |
| animal fish bass | 30 | 10 | 13 |
| fish sea_food black_sea_sprat | 569 | 105 | 298 |
| fish sea_food gilt_head_bream | 566 | 94 | 305 |
| fish sea_food hourse_mackerel | 573 | 97 | 286 |
| fish sea_food red_mullet | 579 | 90 | 291 |
| fish sea_food red_sea_bream | 571 | 113 | 273 |
| fish sea_food sea_bass | 538 | 97 | 327 |
| fish sea_food shrimp | 576 | 100 | 292 |
| fish sea_food striped_red_mullet | 547 | 101 | 293 |
| fish sea_food trout | 580 | 98 | 292 |
| **Total** | **6225** | **1092** | **3197** |

Ten of the eleven classes are well balanced at roughly 550 training images
each. **`animal fish bass` is the exception with only 30** — about 5% of a
normal class. Expect its recall to be the weakest number in the results, and
quote the weighted F1-score rather than plain accuracy for this reason.

### Step 1b — validate the dataset

```bash
python validate_data.py
```

Checks all three splits hold the same species, that every image opens, and —
most importantly — that **no image appears in more than one split**. A test
image that was also trained on would make the accuracy meaningless. Also warns
about any species with too few images. Takes about a minute; worth it before
spending hours training.

### Step 2 — train and evaluate all six models

```bash
python train_all_models.py
```

Useful variations while you are testing:

```bash
python train_all_models.py --model MobileNet --epochs 2
```

This writes:
- `models/*.h5` — one file per model, plus `best_model.h5`
- `outputs/plots/*_training_history.png` — accuracy and loss curves
- `outputs/plots/*_confusion_matrix.png` — which species get confused
- `outputs/plots/model_comparison.png` — all six models, all four metrics
- `outputs/reports/model_comparison.csv` — the comparison table
- `outputs/reports/*_classification_report.txt` — per-species precision/recall/F1

### Step 2b — write the comparison report

```bash
python make_report.py
```

Writes `outputs/reports/comparison_report.md` and fills in the Results section
of this README automatically.

### Faster alternative — train on a free Colab GPU

Training all six models on a laptop CPU takes hours. `Fish_Classification_Colab.ipynb`
runs the **same code** on Colab's free T4 GPU in roughly 20 minutes.

1. Upload `Fish_Classification_Colab.ipynb` to [Google Colab](https://colab.research.google.com).
2. `Runtime` → `Change runtime type` → **T4 GPU**.
3. Run the cells top to bottom. It fetches the code, downloads the dataset,
   trains, reports, and hands you a `results.zip`.
4. Unzip `results.zip` into this folder so you get `models/best_model.h5`,
   `models/class_names.json` and the contents of `outputs/`.
5. Run `streamlit run app.py` locally — it works straight away.

The notebook gets the code either by cloning your GitHub repo (Option A) or by
uploading a small zip you build with:

```bash
python make_colab_bundle.py
```

Nothing is duplicated: the notebook calls `train_all_models.py` and imports the
same `src/` modules. There is only ever one copy of the logic.

### Step 3 — run the web app

```bash
streamlit run app.py
```

Then open the address it prints (usually http://localhost:8501), upload a fish
photo, and read the prediction and confidence scores.

---

## 7. Approach in detail

### Data preprocessing and augmentation
Every image is resized to **224×224** and rescaled from 0–255 to **0–1**.
Training images are additionally augmented each epoch: rotation ±20°, zoom 20%,
width/height shift 20%, shear 20%, horizontal flip. Validation and test images
are only rescaled — never augmented — so the scores reflect real pictures.

### Model training
- **CNN from scratch** — four Conv2D + MaxPooling blocks (32 → 64 → 128 → 128
  filters), Flatten, Dense(256), Dropout(0.5), softmax output. Adam, lr 0.001.
- **Five pre-trained models** — ImageNet weights, `include_top=False`, base
  **frozen**, then GlobalAveragePooling2D → Dense(256) → Dropout(0.3) → softmax.
  Adam with a small lr of 0.0001 so the pre-trained knowledge is not destroyed.
- `EarlyStopping(patience=3, restore_best_weights=True)` stops a model that has
  stopped improving; `ModelCheckpoint(save_best_only=True)` keeps the best
  version on disk.

> **Note on EfficientNetB0:** it has its own rescaling built in and expects
> pixels in 0–255. Since our generator already divides by 255, the model adds a
> `Rescaling(255.0)` layer first to undo that. Without this one line,
> EfficientNetB0 scores near random.

### Model evaluation
Every model is judged on the **test set it has never seen**, using weighted
accuracy, precision, recall and F1 plus a per-species classification report and
a confusion matrix.

### Deployment
The highest-accuracy model is copied to `models/best_model.h5` and loaded by the
Streamlit app, which shows the predicted species, the confidence percentage, and
a bar chart of confidence across all species.

---

## 8. Results

<!-- RESULTS_START -->

| Model          |   Accuracy |   Precision |   Recall |   F1-score |   Training (min) |   Epochs |
|:---------------|-----------:|------------:|---------:|-----------:|-----------------:|---------:|
| MobileNet      |     0.9815 |      0.9818 |   0.9815 |     0.9803 |             10.1 |        4 |
| InceptionV3    |     0.965  |      0.9616 |   0.965  |     0.9631 |             14.2 |        4 |
| EfficientNetB0 |     0.9553 |      0.9569 |   0.9553 |     0.954  |             15   |        4 |
| CNN_Scratch    |     0.9221 |      0.9246 |   0.9221 |     0.9177 |             34.9 |       10 |
| VGG16          |     0.6931 |      0.7497 |   0.6931 |     0.6733 |             45.6 |        4 |
| ResNet50       |     0.1648 |      0.0272 |   0.1648 |     0.0467 |             19   |        3 |

### Insights

- **Best model: MobileNet** with an accuracy of 0.9815 and an F1-score of 0.9803. This is the model saved as `models/best_model.h5` and used by the Streamlit app.
- **Weakest model: ResNet50** with an accuracy of 0.1648.
- The gap between the best and the weakest model is 0.8167 (81.7 percentage points).
- The from-scratch CNN (0.9221) matched or beat the average of the pre-trained models (0.7520). With a small or very distinctive dataset this can happen, but it is worth training for more epochs before trusting it.
- Fastest to train: **MobileNet** at 10.1 minutes.
- EarlyStopping ended training before the full 10 epochs for: MobileNet, InceptionV3, EfficientNetB0, VGG16, ResNet50. Those models had stopped improving on the validation set.

<!-- RESULTS_END -->

> **The epoch budget was not equal.** CNN_Scratch was trained for 10 epochs;
> the five transfer-learning models got 4 (patience 2) to keep the total CPU
> training time near 1h45m. That favours the from-scratch CNN, so MobileNet,
> InceptionV3 and EfficientNetB0 beating it on less than half the budget is a
> stronger result than the table suggests. VGG16 and ResNet50 are
> **under-trained**, not bad architectures - see
> `outputs/reports/comparison_report.md` for the full explanation.

---

## 9. Deliverables checklist

- [x] Trained models saved in `.h5` format (CNN + 5 pre-trained)
- [x] Streamlit application for real-time predictions
- [x] Python scripts for training, evaluation and deployment
- [x] Comparison report with metrics and insights
- [x] Documented, modular codebase in a public GitHub repository

---

## 10. Coding standards

The code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/):
`snake_case` names, 4-space indentation, a docstring on every module and
function, and no logic duplicated between files — anything reusable lives in
`src/`.
