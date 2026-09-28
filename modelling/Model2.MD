# Model 2: Decision Tree

## File

**Notebook:** [`modelling/model2_decision_tree.ipynb`](modelling/model2_decision_tree.ipynb)

This notebook trains, tunes, evaluates and saves a decision tree model, demonstrates inference on new records, and compares the results with Model 1.

## How to use

1. Run the [preprocessing](Preprocessing.MD) and [feature engineering](FeatureEngineering.MD) notebooks first.
2. For the comparison table at the end, also run [Model 1](Model1.MD) first.
3. Open `modelling/model2_decision_tree.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Inputs:** `data/train.csv`, `data/test.csv`, `models/preprocessor.pkl`

**Outputs:**
- `models/model2_decision_tree.pkl`: the trained pipeline (preprocessing and model)
- `evaluation/model2_decision_tree_results.csv`: test-period metrics
- `evaluation/model_comparison.csv`: side-by-side comparison with Model 1
- `modelling/figures/`: evaluation and feature importance charts

**Inference:** the notebook's inference section loads the saved model and predicts for new customers:

`model = joblib.load("../models/model2_decision_tree.pkl")`, then `model.predict_proba(new_data)[:, 1]` gives the probability of conversion. `new_data` must have the same columns as `data/train.csv`, without `y`.

## Technique

A decision tree classifies customers by learning a sequence of yes/no rules on the features. It was chosen as a contrast to logistic regression: it can capture non-linear relationships and interactions between features, its rules are easy to follow, and it was also compared by Moro, Cortez and Rita (2014).

## Hyperparameters

| Hyperparameter | Values searched | Selected |
|---|---|---|
| `max_depth` (maximum number of levels) | 3, 4, 5, 6, 8 | **8** |
| `min_samples_leaf` (minimum customers per final group) | 20, 50, 100 | **100** |
| `class_weight` | fixed | `balanced` |
| `criterion` | default | `gini` |
| `random_state` | fixed | 42 |

- **Class imbalance:** `class_weight="balanced"` gives the minority "yes" class more weight (Singh et al., 2024).
- **Tuning:** grid search with 5-fold stratified cross-validation within the training period only, using ROC AUC. Best cross-validation AUC: **0.665**.

## Results (test period)

| Algorithm | Accuracy | Precision | Recall | F1-Score | AUC |
|---|---|---|---|---|---|
| Model 1: Logistic Regression | 0.450 | 0.352 | 0.932 | 0.511 | 0.741 |
| **Model 2: Decision Tree** | 0.420 | 0.306 | 0.693 | 0.424 | 0.552 |

- The decision tree performs worse than logistic regression on every metric in the test period, with an AUC close to random guessing (0.5).
- **Robustness check:** on a random stratified split, the tree's AUC is 0.799, almost identical to logistic regression. Its poor time-split result is therefore caused by the change over time: the economic indicators in the test period fall outside the training range, and decision trees cannot extrapolate beyond values seen in training.
- **Main predictors:** consumer confidence (`cons.conf.idx`), `euribor3m` and `cons.price.idx` dominate, which are features describing economic conditions rather than the customer.

## Model selection

Logistic regression (Model 1) is selected as the final model. It performs better on the unseen later period, is more robust when conditions change, and is easier to interpret. For STADIOEquities, both models' reliance on timing and economic features suggests that customer-level behavioural data, such as the session and timing fields in the SS1 data request, would be needed for reliable activation prediction (Abbas, Hussain and Rimal, 2025).

## References

Abbas, S.K., Hussain, M. and Rimal, Y.N. (2025) 'Machine learning-based analysis of technology acceptance in FinTech: a behavioral study using digital wallet data', *SN Computer Science*, 6, article 674. doi: 10.1007/s42979-025-04214-8.

Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', *Decision Support Systems*, 62, pp. 22-31. doi: 10.1016/j.dss.2014.03.001.

Singh, P.P., Anik, F.I., Senapati, R., Sinha, A., Sakib, N. and Hossain, E. (2024) 'Investigating customer churn in banking: a machine learning approach and visualization app for data science and management', *Data Science and Management*, 7(1), pp. 7-16. doi: 10.1016/j.dsm.2023.09.002.
