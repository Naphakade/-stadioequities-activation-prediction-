# Comparison of Model 1 and Model 2

## File

**Notebook:** [`evaluation/comparison.ipynb`](evaluation/comparison.ipynb)
**Helper functions:** [`utils/evaluation_utils.py`](utils/evaluation_utils.py)

This notebook compares Model 1 ([Logistic Regression](Model1.MD)) and Model 2 ([Decision Tree](Model2.MD)) on exactly the same unseen test period, using statistical tests for the differences.

## How to use

1. Install the packages: `pip install -r requirements.txt`
2. Run the notebooks in order: [preprocessing](Preprocessing.MD), [feature engineering](FeatureEngineering.MD), [Model 1](Model1.MD) and [Model 2](Model2.MD). Both saved models must exist in `models/`.
3. Open `evaluation/comparison.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Outputs:**
- `evaluation/comparison_metrics.csv`: side-by-side metrics with confidence intervals
- `evaluation/comparison_differences.csv`: paired bootstrap differences and p-values
- `evaluation/comparison_robustness.csv`: time-ordered vs random split
- `evaluation/figures/comparison_curves.png`: overlaid ROC and gains curves

## Statistical methods

- **Paired bootstrap:** both models are scored on the same 1,000 resamples of the test set. The difference (Model 1 minus Model 2) is recorded each time, giving a 95% confidence interval and a two-sided p-value. If the interval excludes 0, the difference is significant at the 5% level.
- **McNemar's test (exact):** compares the yes/no predictions using only the customers on whom the models disagree.
- **Paired t-test on cross-validation folds:** compares the models' AUCs on identical 5-fold splits of the training period.

## Results

### Side-by-side metrics (test period, 95% CI in brackets)

| Metric | Model 1: Logistic Regression | Model 2: Decision Tree |
|---|---|---|
| Accuracy | 0.450 (0.439 to 0.460) | 0.420 (0.410 to 0.431) |
| Balanced accuracy | **0.584** (0.576 to 0.591) | 0.496 (0.486 to 0.506) |
| Precision | **0.352** (0.340 to 0.363) | 0.306 (0.293 to 0.318) |
| Recall | **0.932** (0.922 to 0.941) | 0.693 (0.676 to 0.711) |
| Specificity | 0.236 (0.224 to 0.246) | **0.299** (0.287 to 0.310) |
| F1-Score | **0.511** (0.498 to 0.523) | 0.424 (0.411 to 0.438) |
| ROC AUC | **0.741** (0.728 to 0.752) | 0.552 (0.539 to 0.567) |
| PR AUC | **0.539** (0.518 to 0.560) | 0.389 (0.372 to 0.406) |
| Brier score (lower is better) | 0.315 (0.310 to 0.320) | **0.266** (0.261 to 0.269) |

### Paired bootstrap differences (Model 1 minus Model 2)

| Metric | Difference | 95% CI | p-value |
|---|---|---|---|
| Accuracy | +0.030 | 0.019 to 0.040 | <0.001 |
| Balanced accuracy | +0.088 | 0.077 to 0.098 | <0.001 |
| Precision | +0.046 | 0.040 to 0.052 | <0.001 |
| Recall | +0.239 | 0.221 to 0.256 | <0.001 |
| Specificity | -0.063 | -0.075 to -0.050 | <0.001 |
| F1-Score | +0.087 | 0.077 to 0.096 | <0.001 |
| ROC AUC | +0.188 | 0.173 to 0.202 | <0.001 |
| PR AUC | +0.150 | 0.135 to 0.165 | <0.001 |
| Brier score | +0.049 | 0.044 to 0.055 | <0.001 |

For the Brier score, a positive difference means Model 1 has the larger error.

### McNemar's test

| | Count |
|---|---|
| Model 1 correct, Model 2 wrong | 1,108 |
| Model 1 wrong, Model 2 correct | 859 |
| Exact p-value | 2.16 × 10⁻⁸ |

### Cross-validation on the training period

| | Mean AUC ± SD |
|---|---|
| Model 1 | 0.671 ± 0.013 |
| Model 2 | 0.665 ± 0.004 |
| Paired t-test | t = 1.00, p = 0.373 |

### Cumulative gains (share of converters captured)

| Top share contacted | Model 1 | Model 2 |
|---|---|---|
| 10% | 21.5% | 19.3% |
| 20% | 38.5% | 31.4% |
| 30% | 54.0% | 42.1% |
| 50% | 74.8% | 57.3% |

### Robustness: time-ordered vs random split

| Model | ROC AUC, time-ordered | ROC AUC, random | Drop |
|---|---|---|---|
| Model 1 | 0.741 | 0.800 | 0.059 |
| Model 2 | 0.552 | 0.799 | 0.247 |

## Discussion

1. **Model 1 is significantly better on the test period.** It outperforms Model 2 on accuracy, balanced accuracy, precision, recall, F1, ROC AUC and PR AUC. Every confidence interval for these differences excludes 0 (p < 0.001), and McNemar's test confirms that Model 1 makes significantly fewer classification errors (p = 2.16 × 10⁻⁸). The largest gains are in ROC AUC (+0.188) and recall (+0.239).
2. **Model 2 wins on two measures, for different reasons.** Its higher specificity (+0.063) simply reflects that it predicts "yes" less often, which is why it also misses far more converters. Its lower Brier score reflects better-calibrated probabilities, because Model 1's class weighting inflates its probabilities. Calibration can be corrected after training, whereas weak ranking ability cannot, so this does not change the overall conclusion.
3. **The models are equivalent before the change in conditions.** On the training period, their cross-validation AUCs are not significantly different (p = 0.373), and on a random split both reach an AUC of about 0.80. The difference between them appears only when they predict a later period with different economic conditions.
4. **The reason is extrapolation.** Model 2 loses 0.247 AUC under the time-ordered split, compared with 0.059 for Model 1. Economic indicators in the test period fall outside the training range. Logistic regression extends its fitted trends to these new values, while a decision tree can only place new customers into leaves learned from past values, so its predictions barely change.
5. **Business impact:** when contacting the top 20% of ranked customers, Model 1 reaches 38.5% of converters versus 31.4% for Model 2, about 180 additional converters in this test period.

**Conclusion:** Model 1 (Logistic Regression) is the better model for STADIOEquities. It is significantly more accurate at identifying and ranking likely converters on unseen future data, and far more robust when conditions change. Its main weakness, inflated probabilities, can be addressed through recalibration and threshold tuning.
