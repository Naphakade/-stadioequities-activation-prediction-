# Preprocessing

## File

**Notebook:** [`preprocessing/preprocessing.ipynb`](preprocessing/preprocessing.ipynb)

This notebook loads the raw Bank Marketing dataset, checks its quality, explores it with charts, cleans it, and saves a cleaned version for the feature engineering step.

## How to use

1. Install the required packages from the main project folder:

2. Place the raw dataset at `data/bank-additional-full.csv`. It can be downloaded from the UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/222/bank+marketing
3. Open `preprocessing/preprocessing.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Input:** `data/bank-additional-full.csv` (41,188 rows, 21 columns, semicolon-separated)

**Outputs:**
- `data/cleaned_data.csv`: the cleaned dataset (41,176 rows, 20 columns), used by the feature engineering notebook
- `preprocessing/figures/`: exploratory charts

This notebook must be run before the feature engineering notebook.

## Preprocessing techniques

### 1. Data quality checks
- **Missing values:** the dataset contains no blank values.
- **Placeholder values:** missing information is recorded as placeholder codes instead of blanks. Six categorical columns contain the value `unknown` (for example, `default` has 8,597 and `education` has 1,731), and `pdays` uses `999` to mean "never previously contacted" (96.3% of rows).
- **Duplicates:** 12 rows are exact duplicates.
- **Near-constant column:** `default` contains only 3 "yes" values; almost all values are "no" or "unknown".

### 2. Exploratory data analysis
- **Class imbalance:** only 11.3% of customers converted ("yes"), so accuracy alone would be a misleading metric. This is handled during modelling with class weighting, following Singh et al. (2024).
- **Change over time:** the rows are in date order (May 2008 to November 2010). The conversion rate rises sharply in the later campaigns, which supports using a time-ordered train/test split (Moro, Cortez and Rita, 2014).
- **Predictors:** conversion varies strongly by previous campaign outcome (`poutcome`), contact type, job and month.
- **Multicollinearity:** the economic indicators `emp.var.rate`, `euribor3m` and `nr.employed` are very highly correlated with each other.

### 3. Cleaning decisions

| Change | Reason | Effect |
|---|---|---|
| Removed exact duplicate rows | Duplicates would give some customers extra weight | 41,188 → 41,176 rows |
| Dropped `duration` | Call length is only known after the call ends, so it would leak the outcome into the model (target leakage) | 21 → 20 columns |
| Kept `unknown` as its own category | Not answering a question may itself be informative, and removing these rows would lose data | No rows removed |

Duplicates are removed **before** dropping `duration`. Otherwise, different calls that happen to share all other details would wrongly be treated as duplicates.

The `pdays` placeholder and the target variable are transformed in the feature engineering step (see [FeatureEngineering.MD](FeatureEngineering.MD)).

## References

Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', *Decision Support Systems*, 62, pp. 22–31. doi: 10.1016/j.dss.2014.03.001.

Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [Dataset]. UCI Machine Learning Repository. doi: 10.24432/C5K306.

Singh, P.P., Anik, F.I., Senapati, R., Sinha, A., Sakib, N. and Hossain, E. (2024) 'Investigating customer churn in banking: a machine learning approach and visualization app for data science and management', *Data Science and Management*, 7(1), pp. 7–16. doi: 10.1016/j.dsm.2023.09.002.
