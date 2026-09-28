# Model 2 Performance: Decision Tree

## File

**Notebook:** [`evaluation/model2_performance.ipynb`](evaluation/model2_performance.ipynb)
**Helper functions:** [`utils/evaluation_utils.py`](utils/evaluation_utils.py)

This notebook evaluates the saved Model 2 (see [Model2.MD](Model2.MD)) on the unseen, later test period.

## How to use

1. Install the packages: `pip install -r requirements.txt`
2. Run the notebooks in order: [preprocessing](Preprocessing.MD), [feature engineering](FeatureEngineering.MD) and [Model 2](Model2.MD). These create `data/train.csv`, `data/test.csv` and `models/model2_decision_tree.pkl`.
3. Open `evaluation/model2_performance.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Outputs:**
- `evaluation/model2_decision_tree_performance.csv`: metrics with confidence intervals
- `evaluation/model2_decision_tree_cv_scores.csv`: cross-validation AUC per fold
- `evaluation/figures/model2_confusion_matrix.png` and `evaluation/figures/model2_curves.png`

## Evaluation setup

The setup is identical to Model 1, so the results are directly comparable:

- **Test set:** the last 20% of rows in date order (8,236 customers, 30.8% converted), not used in training or tuning.
- **Threshold:** predicted probability of 0.5 or above = "yes", unless stated otherwise.
- **Statistical method:** 95% confidence intervals from 1,000 bootstrap resamples of the test set, and 5-fold stratified cross-validation on the training period.

## Results

### Metrics with 95% confidence intervals (test period)

| Metric | Value | 95% CI |
|---|---|---|
| Accuracy | 0.420 | 0.410 to 0.431 |
| Balanced accuracy | 0.496 | 0.486 to 0.506 |
| Precision | 0.306 | 0.293 to 0.318 |
| Recall (sensitivity) | 0.693 | 0.676 to 0.711 |
| Specificity | 0.299 | 0.287 to 0.310 |
| F1-Score | 0.424 | 0.411 to 0.438 |
| ROC AUC | 0.552 | 0.539 to 0.567 |
| PR AUC (average precision) | 0.389 | 0.372 to 0.406 |
| Brier score (lower is better) | 0.266 | 0.261 to 0.269 |

### Comparison with baselines

| | Accuracy | Recall | ROC AUC | PR AUC |
|---|---|---|---|---|
| Always predict "no" | 0.692 | 0.000 | 0.500 | 0.308 |
| Random ranking | n/a | n/a | 0.500 | 0.308 |
| **Model 2** | 0.420 | 0.693 | 0.552 | 0.389 |

### Confusion matrix (test period)

| | Predicted "no" | Predicted "yes" |
|---|---|---|
| **Actual "no"** | 1,701 | 3,996 |
| **Actual "yes"** | 779 | 1,760 |

### Cross-validation stability (training period)

Fold AUCs: 0.665, 0.659, 0.670, 0.663, 0.666. **Mean ± SD: 0.665 ± 0.004.**

### Cumulative gains and lift

| Top share contacted | Converters captured | Lift |
|---|---|---|
| 10% | 19.3% | 1.93 |
| 20% | 31.4% | 1.57 |
| 30% | 42.1% | 1.40 |
| 50% | 57.3% | 1.15 |

### Threshold analysis

| Threshold | Share predicted "yes" | Precision | Recall | F1-Score | Accuracy |
|---|---|---|---|---|---|
| 0.3 | 84.9% | 0.294 | 0.810 | 0.432 | 0.342 |
| 0.4 | 73.1% | 0.306 | 0.724 | 0.430 | 0.408 |
| **0.5** | 69.9% | 0.306 | 0.693 | 0.424 | 0.420 |
| 0.6 | 13.6% | 0.599 | 0.263 | 0.366 | 0.719 |
| 0.7 | 13.3% | 0.605 | 0.261 | 0.365 | 0.720 |

### Robustness check

| Split | ROC AUC |
|---|---|
| Time-ordered (main result) | 0.552 |
| Random stratified | 0.799 |

## Interpretation

1. **Ranking ability is only slightly better than chance.** ROC AUC is 0.552 (95% CI 0.539 to 0.567). The interval excludes 0.5, so the model has some genuine skill, but very little. Balanced accuracy of 0.496 (CI includes 0.5) shows its yes/no predictions are no better than chance once class imbalance is accounted for.
2. **It misses far more converters than Model 1.** Recall is 0.693, so 779 of 2,539 converters were missed. Precision (0.306) is at the level of the 30.8% base rate, meaning a "yes" prediction is barely more informative than picking customers at random.
3. **Probabilities are better calibrated than Model 1's.** The Brier score of 0.266 is lower (better) than Model 1's 0.315. The tree's probabilities come from the share of "yes" customers in each leaf, which keeps them closer to observed rates. However, good calibration is of limited use when the model cannot rank customers well.
4. **Thresholds behave in steps.** Because a tree only produces a small number of distinct probabilities (one per leaf), moving the threshold from 0.5 to 0.6 changes the share predicted "yes" abruptly from 69.9% to 13.6%. This makes the model hard to fine-tune for a business target.
5. **Very stable in training, but collapses under time shift.** Cross-validation AUC is highly consistent (0.665 ± 0.004), and on a random split the tree reaches 0.799. The drop to 0.552 on the time-ordered split is caused by the economic indicators in the test period falling outside the training range: a decision tree cannot extrapolate beyond the values it has seen, so it assigns most new customers to the same few leaves.

See [Comparison.MD](Comparison.MD) for the statistical comparison with Model 1.
