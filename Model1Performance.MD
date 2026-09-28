# Model 1 Performance: Logistic Regression

## File

**Notebook:** [`evaluation/model1_performance.ipynb`](evaluation/model1_performance.ipynb)
**Helper functions:** [`utils/evaluation_utils.py`](utils/evaluation_utils.py)

This notebook evaluates the saved Model 1 (see [Model1.MD](Model1.MD)) on the unseen, later test period.

## How to use

1. Install the packages: `pip install -r requirements.txt`
2. Run the notebooks in order: [preprocessing](Preprocessing.MD), [feature engineering](FeatureEngineering.MD) and [Model 1](Model1.MD). These create `data/train.csv`, `data/test.csv` and `models/model1_logistic_regression.pkl`.
3. Open `evaluation/model1_performance.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Outputs:**
- `evaluation/model1_logistic_regression_performance.csv`: metrics with confidence intervals
- `evaluation/model1_logistic_regression_cv_scores.csv`: cross-validation AUC per fold
- `evaluation/figures/model1_confusion_matrix.png` and `evaluation/figures/model1_curves.png`

## Evaluation setup

- **Test set:** the last 20% of rows in date order (8,236 customers, of whom 2,539 or 30.8% converted). The model never saw this period during training or tuning.
- **Threshold:** predicted probability of 0.5 or above = "yes", unless stated otherwise.
- **Statistical method:** 95% confidence intervals from 1,000 bootstrap resamples of the test set (percentile method), and 5-fold stratified cross-validation on the training period.

## Results

### Metrics with 95% confidence intervals (test period)

| Metric | Value | 95% CI |
|---|---|---|
| Accuracy | 0.450 | 0.439 to 0.460 |
| Balanced accuracy | 0.584 | 0.576 to 0.591 |
| Precision | 0.352 | 0.340 to 0.363 |
| Recall (sensitivity) | 0.932 | 0.922 to 0.941 |
| Specificity | 0.236 | 0.224 to 0.246 |
| F1-Score | 0.511 | 0.498 to 0.523 |
| ROC AUC | 0.741 | 0.728 to 0.752 |
| PR AUC (average precision) | 0.539 | 0.518 to 0.560 |
| Brier score (lower is better) | 0.315 | 0.310 to 0.320 |

### Comparison with baselines

| | Accuracy | Recall | ROC AUC | PR AUC |
|---|---|---|---|---|
| Always predict "no" | 0.692 | 0.000 | 0.500 | 0.308 |
| Random ranking | n/a | n/a | 0.500 | 0.308 |
| **Model 1** | 0.450 | 0.932 | 0.741 | 0.539 |

### Confusion matrix (test period)

| | Predicted "no" | Predicted "yes" |
|---|---|---|
| **Actual "no"** | 1,343 | 4,354 |
| **Actual "yes"** | 172 | 2,367 |

### Cross-validation stability (training period)

Fold AUCs: 0.670, 0.671, 0.669, 0.692, 0.655. **Mean ± SD: 0.671 ± 0.013.**

### Cumulative gains and lift

| Top share contacted | Converters captured | Lift |
|---|---|---|
| 10% | 21.5% | 2.15 |
| 20% | 38.5% | 1.93 |
| 30% | 54.0% | 1.80 |
| 50% | 74.8% | 1.50 |

### Threshold analysis

| Threshold | Share predicted "yes" | Precision | Recall | F1-Score | Accuracy |
|---|---|---|---|---|---|
| 0.3 | 99.6% | 0.309 | 0.999 | 0.472 | 0.312 |
| 0.4 | 92.6% | 0.326 | 0.980 | 0.489 | 0.370 |
| **0.5** | 81.6% | 0.352 | 0.932 | 0.511 | 0.450 |
| 0.6 | 58.6% | 0.435 | 0.826 | 0.570 | 0.615 |
| 0.7 | 43.1% | 0.485 | 0.678 | 0.566 | 0.679 |

### Robustness check

| Split | ROC AUC |
|---|---|
| Time-ordered (main result) | 0.741 |
| Random stratified | 0.800 |

## Interpretation

1. **Ranking ability is good and statistically reliable.** ROC AUC of 0.741 (95% CI 0.728 to 0.752) is well above the 0.5 of random ranking, and PR AUC of 0.539 is well above the 0.308 baseline. The narrow confidence intervals show these results are not due to chance.
2. **The model catches almost all converters but flags too many customers.** Recall is 0.932, so only 172 of 2,539 converters were missed. However, specificity is only 0.236, because the model labels 81.6% of customers as "yes". This is why accuracy (0.450) falls below the "always no" baseline (0.692), and why accuracy is not a suitable headline metric here.
3. **Probabilities are too high (poor calibration).** The calibration curve lies below the diagonal: customers given a probability of about 0.6 actually converted only about 25% of the time. This is expected from class weighting, which deliberately boosts the "yes" class, and from the change in conditions between periods. It explains the relatively high Brier score of 0.315.
4. **The default threshold is not optimal.** Raising the threshold to 0.6 increases F1 from 0.511 to 0.570 and accuracy from 0.450 to 0.615, while still finding 82.6% of converters. In practice the threshold should be chosen on a validation period, not on the test set.
5. **Business value:** contacting the top 20% of ranked customers reaches 38.5% of converters, almost twice the 20% expected from random targeting (lift 1.93).
6. **Stable in training, but affected by time shift.** Cross-validation AUC varies little (SD 0.013). AUC falls from 0.800 on a random split to 0.741 on the time-ordered split, a modest drop given that economic conditions in the test period lie outside the training range.

See [Comparison.MD](Comparison.MD) for the statistical comparison with Model 2.
