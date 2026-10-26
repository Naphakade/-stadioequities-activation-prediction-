
# Preprocessing

## File

**Notebook:** [`preprocessing/preprocessing.ipynb`](preprocessing/preprocessing.ipynb)

This notebook prepares the UCI Bank Marketing dataset for exploratory analysis and feature engineering. It checks data quality, explores patterns in the dataset, applies the documented cleaning decisions, and saves the cleaned dataset for the next stage of the project.

## How to Use

1. Install the required packages from the project root directory:

   `pip install -r requirements.txt`

2. Download the raw Bank Marketing dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing).

3. Place the raw dataset at `data/bank-additional-full.csv`.

4. Open `preprocessing/preprocessing.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Input:** `data/bank-additional-full.csv` (41,188 rows, 21 columns, semicolon-separated).

**Outputs:**

- `data/cleaned_data.csv`: cleaned dataset containing 41,176 rows and 20 columns, used by the feature engineering notebook.
- `preprocessing/figures/`: exploratory data analysis charts.

Run this notebook before the [Feature Engineering](FeatureEngineering.MD) stage.

## Preprocessing Techniques

### 1. Data Quality Checks

- **Missing values:** The dataset contains no blank values.
- **Placeholder values:** Missing information is represented by placeholder categories rather than blank cells. Six categorical columns contain `unknown`. For example, `default` contains 8,597 `unknown` values, while `education` contains 1,731.
- **Previous contact information:** The `pdays` column uses `999` to represent customers who were not previously contacted. This applies to approximately 96.3% of the rows.
- **Duplicates:** The dataset contains 12 exact duplicate rows.
- **Near-constant column:** The `default` column contains only three `yes` values, while the remaining values are predominantly `no` or `unknown`.

### 2. Exploratory Data Analysis

- **Class imbalance:** Approximately 11.3% of customers have a positive conversion outcome. Accuracy alone may therefore provide a misleading view of model performance. Class weighting is addressed during modelling, following the approach discussed by Sifa et al. (2015).
- **Changes over time:** The records span May 2008 to November 2010 and are arranged chronologically. The observed increase in conversion rates during later campaigns supports considering time-ordered data splitting during modelling (Moro, Cortez and Rita, 2014).
- **Predictor relationships:** Conversion rates vary across previous campaign outcomes (`poutcome`), contact type, job category, and month.
- **Multicollinearity:** The economic indicators `emp.var.rate`, `euribor3m`, and `nr.employed` are highly correlated. This relationship is relevant when interpreting the predictors used in subsequent modelling.

### 3. Cleaning Decisions

| Change | Reason | Effect |
|---|---|---|
| Removed exact duplicate rows | Prevents repeated records from receiving additional weight in the analysis | 41,188 to 41,176 rows |
| Dropped `duration` | Call duration is only known after the call ends and could introduce target leakage when predicting an outcome before the call finishes | 21 to 20 columns |
| Retained `unknown` as a category | Preserves records and allows the model to learn whether unknown information is associated with the outcome | No rows removed for this decision |

Exact duplicates are removed before dropping `duration`. This ordering avoids incorrectly treating records as duplicates when they differ only in call duration.

The `pdays` placeholder and the target variable are handled during feature engineering. See [Feature Engineering](FeatureEngineering.MD) for the next stage.

## References

Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', *Decision Support Systems*, 62, pp. 22–31. doi: [10.1016/j.dss.2014.03.001](https://doi.org/10.1016/j.dss.2014.03.001).

Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [Dataset]. UCI Machine Learning Repository. doi: [10.24432/C5K306](https://doi.org/10.24432/C5K306).

Sifa, R., Hadiji, F., Runge, J., Drachen, A., Kersting, K. and Bauckhage, C. (2015) 'Predicting purchase decisions in mobile free-to-play games', *Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment*, 11(1), pp. 79–85. doi: [10.1609/aiide.v11i1.12788](https://doi.org/10.1609/aiide.v11i1.12788).

