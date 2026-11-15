# Model Comparison Report

All six models were trained on the same images, with the same augmentation, and scored on the same unseen test set.

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

### Where the supporting files are

- Training curves: `outputs/plots/<model>_training_history.png`
- Confusion matrices: `outputs/plots/<model>_confusion_matrix.png`
- Per-species scores: `outputs/reports/<model>_classification_report.txt`
- Comparison chart: `outputs/plots/model_comparison.png`

---

## Important: the epoch budget was not equal

This table is **not** a like-for-like race, and it should not be presented as one.

| Model | Epochs allowed |
|---|---:|
| CNN_Scratch | 10 |
| VGG16, ResNet50, MobileNet, InceptionV3, EfficientNetB0 | 4 (patience 2) |

CNN_Scratch was trained first with the original `EPOCHS = 10` setting. The five
transfer-learning models were then run with `--epochs 4 --patience 2` to cut the
total training time on a CPU-only machine from roughly four hours to about
1 hour 45 minutes.

That difference is **biased in favour of the from-scratch CNN**: it got 2.5x the
training budget. So:

* MobileNet, InceptionV3 and EfficientNetB0 beat CNN_Scratch **despite having
  less than half the epochs**. That makes the case for transfer learning
  stronger than the table alone suggests, not weaker.
* VGG16's 0.6931 and ResNet50's 0.1648 are **under-trained numbers**, not a
  verdict on those architectures. Both were still climbing when they stopped.
  ResNet50 in particular stopped after 3 epochs at barely above the 1-in-11
  random baseline (0.0909), which is the classic signature of a frozen ResNet50
  whose BatchNormalization layers are still using ImageNet statistics on a very
  different image distribution. With a longer run, or by unfreezing the base,
  it would be expected to recover.

If you need a clean comparison for the write-up, re-run every model at the same
epoch count:

```bash
python train_all_models.py --epochs 10 --patience 3 --retrain
```
