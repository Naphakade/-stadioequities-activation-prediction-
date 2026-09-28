# Feature Engineering

## File

**Notebook:** [`feature-extraction/feature_engineering.ipynb`](feature-extraction/feature_engineering.ipynb)

This notebook creates and transforms features from the cleaned data, splits the data by time into training and test sets, and defines the encoding and scaling used by both models.

## How to use

1. Run [`preprocessing/preprocessing.ipynb`](Preprocessing.MD) first, so that `data/cleaned_data.csv` exists.
2. Open `feature-extraction/feature_engineering.ipynb` in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

**Input:** `data/cleaned_data.csv`

**Outputs:**
- `data/train.csv`: training set, earlier campaigns (32,940 rows)
- `data/test.csv`: test set, later campaigns (8,236 rows)
- `models/preprocessor.pkl`: the unfitted encoding and scaling transformer, loaded by both model notebooks

This notebook must be run before [Model 1](Model1.MD) and [Model 2](Model2.MD).

## Feature engineering steps

### 1. New feature: `previously_contacted`
`pdays` records days since the customer was last contacted, but uses `999` to mean "never contacted" (96.3% of rows). Left as a number, the model would treat 999 as a real, very long gap. It is replaced with a binary flag, `previously_contacted` (1 = contacted in an earlier campaign, 0 = not), and `pdays` is dropped. 1,515 customers (3.7%) had been contacted before.

### 2. Target encoding
The target `y` is converted from `yes`/`no` to `1`/`0`.

### 3. Time-ordered train/test split
The rows are in date order, so the first 80% (earlier campaigns) form the training set and the last 20% (later campaigns) form the test set, without shuffling. This reflects the real situation for STADIOEquities, where a model trained on past registrants predicts future ones (Moro, Cortez and Rita, 2014).

| Set | Rows | Conversion rate |
|---|---|---|
| Train (earlier) | 32,940 | 6.4% |
| Test (later) | 8,236 | 30.8% |

A range check shows the economic indicators in the test period fall largely outside the training range (for example, `euribor3m` is 1.30 to 5.05 in training but 0.63 to 1.30 in testing), and September appears only in the test period. This makes the test harder than a random split, and explains part of the model results.

### 4. One-hot encoding (categorical features)
The 10 categorical features (`job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `day_of_week`, `poutcome`) are one-hot encoded, so each category becomes its own 0/1 column. This avoids implying a false order between categories. `handle_unknown="ignore"` prevents errors when the test data contains a category not seen in training.

### 5. Standard scaling (numerical features)
The 9 numerical features (`age`, `campaign`, `previous`, `emp.var.rate`, `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed`, `previously_contacted`) are standardised to a mean of 0 and a standard deviation of 1. This stops features with large units, such as `nr.employed` (around 5,000), from dominating logistic regression.

After encoding and scaling, the 19 input features become 61 model columns.

### Preventing data leakage
The encoder and scaler are saved **unfitted**. Each model notebook places them in a scikit-learn `Pipeline` with the model, so they learn their settings from the training data only, including within each cross-validation fold.

## References

Moro, S., Cortez, P. and Rita, P. (2014) 'A data-driven approach to predict the success of bank telemarketing', *Decision Support Systems*, 62, pp. 22-31. doi: 10.1016/j.dss.2014.03.001.
