# Model 1: Logistic Regression

## File

**Notebook:** [`modelling/model1_logistic_regression.ipynb`](modelling/model1_logistic_regression.ipynb)

This notebook trains, tunes, evaluates and saves a logistic regression model, and demonstrates inference on new records.

## How to use

1. Run the [preprocessing](Preprocessing.MD) and [feature engineering](FeatureEngineering.MD) notebooks first.
2. Open `modelling/model1_logistic_regression.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Inputs:** `data/train.csv`, `data/test.csv`, `models/preprocessor.pkl`

**Outputs:**
- `models/model1_logistic_regression.pkl`: the trained pipeline (preprocessing and model)
- `evaluation/model1_logistic_regression_results.csv`: test-period metrics
- `modelling/figures/`: evaluation and coefficient charts

**Inference:** the final section of the notebook loads the saved model and predicts for new customers:

`model = joblib.load("../models/model1_logistic_regression.pkl")`, then `model.predict_proba(new_data)[:, 1]` gives the probability of conversion. `new_data` must have the same columns as `data/train.csv`, without `y`.

## Technique

Logistic regression is a linear classifier that estimates the probability of conversion from a weighted combination of the features. It was chosen because it was one of the techniques compared by Moro, Cortez and Rita (2014) on this dataset, and because its coefficients are easy to explain to STADIOEquities decision-makers.

## Hyperparameters

| Hyperparameter | Values searched | Selected |
|---|---|---|
| `C` (inverse regularisation strength) | 0.01, 0.1, 1, 10 | **0.1** |
| `class_weight` | fixed | `balanced` |
| `max_iter` | fixed | 2000 |
| `random_state` | fixed | 42 |

- **Class imbalance:** `class_weight="balanced"` gives the minority "yes" class more weight in training (Singh et al., 2024).
- **Tuning:** grid search with 5-fold stratified cross-validation within the training period only, using ROC AUC. Best cross-validation AUC: **0.671**.

## Results (test period)

| Accuracy | Precision | Recall | F1-Score | AUC |
|---|---|---|---|---|
| 0.450 | 0.352 | 0.932 | 0.511 | 0.741 |

- The model finds 93% of customers who converted, at the cost of flagging many who did not.
- Contacting the top 20% of customers ranked by the model reaches 38.5% of converters, compared with 20% at random.
- Accuracy is low because the model over-predicts "yes" in the later period, where economic conditions fall outside the training range. AUC, which measures ranking, is the fairer measure here.
- **Robustness check:** on a random stratified split, AUC is 0.800. The drop to 0.741 on the time-ordered split shows the effect of the change over time.
- **Main predictors:** month of contact and economic indicators (`euribor3m`, `emp.var.rate`, `nr.employed`), followed by job (retired and student customers convert more often).

## References

Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', *Decision Support Systems*, 62, pp. 22-31. doi: 10.1016/j.dss.2014.03.001.

Singh, P.P., Anik, F.I., Senapati, R., Sinha, A., Sakib, N. and Hossain, E. (2024) 'Investigating customer churn in banking: a machine learning approach and visualization app for data science and management', *Data Science and Management*, 7(1), pp. 7-16. doi: 10.1016/j.dsm.2023.09.002.
