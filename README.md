CAP182 Capstone Project. This project predicts whether a newly registered customer of STADIOEquities, a fictional South African fintech, will make a first deposit within 30 days of registering, using only information available at a day-3 decision point.

Because STADIOEquities data is not yet available, the modelling approach is tested on the public UCI Bank Marketing dataset, whose binary target (whether a customer converts to a financial product) serves as a proxy. The decision-point principle is applied by excluding call duration, which is only known after the outcome. The proxy has no registration timeline, so the day-3 and 30-day structure is not tested directly; the Part D report explains how the model would be adapted to the day-3 behavioural data requested in SS1.

## Part A: Literature review

See the [`literature-review`](literature-review) folder.

## Part B: Modelling

| Step | Description | Code |
|---|---|---|
| 1 | [Preprocessing](Preprocessing.MD) | `preprocessing/preprocessing.ipynb` |
| 2 | [Feature Engineering](FeatureEngineering.MD) | `feature-extraction/feature_engineering.ipynb` |
| 3 | [Model 1: Logistic Regression](Model1.MD) | `modelling/model1_logistic_regression.ipynb` |
| 4 | [Model 2: Decision Tree](Model2.MD) | `modelling/model2_decision_tree.ipynb` |

## Part C: Results

| Step | Description | Code |
|---|---|---|
| 5 | [Model 1 Performance](Model1Performance.MD) | `evaluation/model1_performance.ipynb` |
| 6 | [Model 2 Performance](Model2Performance.MD) | `evaluation/model2_performance.ipynb` |
| 7 | [Comparison of Model 1 and Model 2](Comparison.MD) | `evaluation/comparison.ipynb` |

Shared evaluation functions are in `utils/evaluation_utils.py`.

## Part D: Recommendations

The client report is in [`reports/Part_D_Recommendations_Report.pdf`](reports/Part_D_Recommendations_Report.pdf).

## Setup

1. Install the required packages: `pip install -r requirements.txt`
2. Place `bank-additional-full.csv` in the `data` folder. It can be downloaded from https://archive.ics.uci.edu/dataset/222/bank+marketing
3. Open each notebook in Jupyter and run **Kernel → Restart Kernel and Run All Cells**, in the order of the step numbers above.

## Dataset

Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [Dataset]. UCI Machine Learning Repository. doi: 10.24432/C5K306.

## Study Session 3 (SS3): Client Deposit Prediction

### Overview

Study Session 3 extends the existing CAP182 capstone project by applying the selected machine learning method to the STADIOEquities client dataset. The objective is to predict whether a newly registered client will make their first deposit within 30 days of registration, using information available by Day 3.

The earlier study sessions used the public UCI Bank Marketing dataset as a proxy because the STADIOEquities client dataset was not available at that stage. SS3 uses the supplied client data to evaluate the selected approach in the intended business context.

### Notebook

The SS3 Part B implementation is available in:

- `SS3_PartB.ipynb`

The notebook covers the following components:

1. **Dataset Loading:** Loads and combines the five client data tables.
2. **Dataset Preprocessing:** Handles duplicate records, missing values, feature preparation and chronological train, validation and test splits.
3. **Model Training:** Trains and tunes a logistic regression model using time-aware cross-validation and ROC-AUC scoring.
4. **Model Validation:** Evaluates the selected model on validation data and an unseen test dataset.
5. **Results Visualisation:** Presents classification metrics, a confusion matrix, a ROC curve and a precision-recall curve.

### Methodology

The selected logistic regression model uses a preprocessing pipeline that imputes missing values, scales numerical features and encodes categorical features. Hyperparameter tuning considers different regularisation strengths and class-weight settings.

The dataset is divided chronologically into training, validation and test subsets to reflect the order in which client registrations occur. Features that could reveal the target outcome, including the first-deposit date and Day 30 account status, are excluded to reduce data leakage.

### Test Results

The selected model achieved the following results on the unseen test dataset:

| Metric | Result |
|---|---:|
| Accuracy | 79.91% |
| Precision | 73.19% |
| Recall | 81.23% |
| F1-score | 77.00% |
| ROC-AUC | 0.8747 |
| Average precision (PR-AUC) | 0.8039 |

A simple KYC-based baseline achieved 79.17% accuracy. The logistic regression model performed slightly better in accuracy and precision, while the baseline achieved higher recall. This comparison demonstrates why model performance should be assessed using several metrics rather than accuracy alone.

### Limitations and Responsible Use

The model's predictions should support, rather than replace, business decisions. Missing information, changes in client behaviour and differences between historical and future client populations may affect performance. KYC-related missing values may also reflect the client's onboarding progress rather than random missing data.

The model should be monitored over time and assessed for fairness, reliability and suitability before being used in operational decisions. Predictions should not be treated as guarantees of future client behaviour.

### Study Session 3 Deliverables

- **Part A:** Peer-review report submitted to Canvas.
- **Part B:** `SS3_PartB.ipynb`, containing the implementation, evaluation and visualisations.
- **Part C:** Presentation video link to be added when available.
- **Part D:** GitHub Discussions to be enabled and monitored in accordance with the assignment requirements.

