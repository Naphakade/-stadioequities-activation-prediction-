# CAP182 Capstone Project: STADIOEquities Activation Prediction

## Project Overview

This project investigates how machine learning can help STADIOEquities, a fictional South African fintech, identify customers who are likely to become active after registration.

The main business objective is to predict whether a newly registered client will make their first deposit within 30 days of registration. For the Study Session 3 (SS3) implementation, predictions are made using information available by Day 3. This creates an opportunity to identify clients who may benefit from additional onboarding support before the 30-day outcome is known.

The project progresses from a literature review and proxy-dataset modelling exercise to the application of logistic regression to the supplied STADIOEquities client data.

## Project Structure

The repository contains the following main folders and files.

| Folder or file | Purpose |
|---|---|
| `data/` | Location for datasets required by the notebooks. |
| `literature-review/` | Part A literature review and supporting material. |
| `preprocessing/` | Data cleaning and preprocessing notebooks. |
| `feature-extraction/` | Feature engineering notebooks. |
| `modelling/` | Model training and development notebooks. |
| `models/` | Model-related project files. |
| `evaluation/` | Model performance evaluation and comparison notebooks. |
| `utils/` | Shared evaluation utilities. |
| `visualisation/` | Visualisation-related project files. |
| `reports/` | Project reports and recommendations. |
| `requirements.txt` | Python package requirements. |
| `SS3_PartB.ipynb` | SS3 implementation using the supplied STADIOEquities client data. |

## Part A: Literature Review

Part A reviews relevant research on machine learning in financial services, customer behaviour, and fintech-related prediction tasks. It establishes the research context for the modelling approach and considers how findings from existing studies may apply to customer activation prediction.

The literature review is available in the `literature-review/` folder.

## Parts B and C: Proxy-Dataset Modelling and Evaluation

The earlier modelling stages used the public UCI Bank Marketing dataset because the STADIOEquities client dataset was not available at that stage.

The dataset's binary outcome served as a proxy for a financial conversion outcome. However, this proxy task is not identical to predicting a first deposit within 30 days of registration using information available by Day 3. The proxy results therefore provide a methodological starting point rather than direct evidence of model performance on STADIOEquities clients.

### Part B: Modelling

| Step | Description | Notebook |
|---|---|---|
| 1 | Preprocessing | `preprocessing/preprocessing.ipynb` |
| 2 | Feature engineering | `feature-extraction/feature_engineering.ipynb` |
| 3 | Model 1: Logistic Regression | `modelling/model1_logistic_regression.ipynb` |
| 4 | Model 2: Decision Tree | `modelling/model2_decision_tree.ipynb` |

### Part C: Results and Evaluation

| Step | Description | Notebook |
|---|---|---|
| 5 | Model 1 performance | `evaluation/model1_performance.ipynb` |
| 6 | Model 2 performance | `evaluation/model2_performance.ipynb` |
| 7 | Model comparison | `evaluation/comparison.ipynb` |

Shared evaluation functions are located in `utils/evaluation_utils.py`.

## Part D: Recommendations

The Part D report presents recommendations based on the proxy-dataset modelling results. It discusses model selection, potential improvements, adaptation to the requested STADIOEquities data, and the relationship between the results and the literature reviewed in Part A.

See the Part D Recommendations Report in the repository.

## Study Session 3: Client Deposit Prediction

### Objective

SS3 extends the capstone by applying logistic regression to the supplied STADIOEquities client dataset. The objective is to predict whether a newly registered client will make a first deposit within 30 days, using information available by Day 3.

The implementation combines five client data tables and prepares the data for modelling. It uses chronological training, validation, and test subsets so that later registrations are evaluated separately from earlier registrations.

### Implementation

The SS3 Part B notebook is `SS3_PartB.ipynb`.

The notebook covers:

- Loading and combining the five client data tables.
- Checking duplicate records, missing values, and data consistency.
- Preparing numerical and categorical features.
- Excluding identifiers and fields that would reveal information unavailable at the Day-3 decision point.
- Splitting the data chronologically into training, validation, and unseen test subsets.
- Training and tuning a logistic regression pipeline using time-series cross-validation and ROC-AUC scoring.
- Selecting a classification threshold using validation data.
- Evaluating the final model on the unseen test subset.
- Comparing the model with a simple KYC-completion baseline.
- Reviewing performance metrics and visualisations, including the confusion matrix, ROC curve, precision-recall curve, and calibration plot.

### Methodology and Data Leakage Prevention

The logistic regression pipeline uses median imputation and standardisation for numerical features, together with categorical imputation and one-hot encoding for categorical features. Hyperparameter tuning considers different regularisation strengths and class-weight settings.

The model excludes `client_id`, the target variable, the first-deposit date, and Day-30 account status from its predictors. The registration date is used to establish the chronological splits rather than as a raw model predictor. These measures help prevent information from after the Day-3 decision point from leaking into model training.

The classification threshold is selected on the validation subset by maximising the F1-score. The selected threshold is then applied to the unseen test subset, which remains separate from model and threshold selection.

### SS3 Test Results

The selected model achieved the following results on the unseen test subset using the validation-selected threshold of **0.489**.

| Metric | Unseen test result |
|---|---:|
| Accuracy | 79.65% |
| Precision | 70.54% |
| Recall | 87.19% |
| F1-score | 77.99% |
| ROC-AUC | 0.8748 |
| Average precision | 0.8036 |
| Brier score | 0.1418 |

The ROC-AUC bootstrap 95% confidence interval was 0.8641–0.8862, while the F1-score bootstrap 95% confidence interval was 0.7640–0.7964.

These results indicate that the model identified a substantial proportion of clients who deposited within 30 days. However, its precision also means that some clients flagged as likely depositors did not deposit within that period. The model should therefore be assessed in terms of the business costs and benefits of onboarding interventions rather than accuracy alone.

### Comparison with the KYC Baseline

A simple baseline predicts a deposit when `kyc_status_day3` is marked as `Completed`.

| Metric | Logistic regression | KYC baseline |
|---|---:|---:|
| Accuracy | 79.65% | 79.27% |
| Precision | 70.54% | 71.00% |
| Recall | 87.19% | 84.31% |
| F1-score | 77.99% | 77.08% |

The logistic regression model achieved higher recall and F1-score, while the KYC baseline achieved slightly higher precision. The accuracy difference was 0.38 percentage points, with a bootstrap 95% confidence interval of -0.38 to 1.11 percentage points. Since this interval includes zero, the results do not establish a clear accuracy advantage for the model.

The KYC rule provides a useful benchmark and may remain valuable because of its simplicity. The results support evaluating the model as a potential decision-support tool alongside existing onboarding processes rather than treating it as an automatic replacement.

### SS3 Part C: Presentation

The presentation explains the STADIOEquities client deposit prediction problem and the progression from the earlier proxy-dataset modelling stages to the implementation using the supplied client data.

It discusses the dataset, preprocessing steps, measures taken to prevent data leakage, logistic regression modelling approach, and evaluation on the unseen test subset. The presentation also interprets the model's performance metrics and visualisations, compares the model with the KYC-completion baseline, and considers the limitations and responsible use of predictions in client onboarding.

**Presentation video:** [Watch the CAP182 SS3 Presentation](https://youtu.be/Hb36M6maSUo)

### Limitations and Responsible Use

The SS3 results relate to the supplied dataset and should not be treated as a guarantee of future performance. Changes in client behaviour, marketing, onboarding procedures, or the wider client population may affect the model's reliability.

Missing values in onboarding fields can carry meaning. For example, an absent KYC completion time may indicate that KYC was not completed, while an absent abandonment step may indicate that no abandonment was recorded. These patterns require careful handling and interpretation.

The model identifies predictive relationships; it does not establish causation. Before operational use, the model should undergo prospective testing, probability-calibration review, fairness assessment, and ongoing performance monitoring. Client information must be protected, and predictions should support human judgement rather than automatically denying services or assistance.

The selected classification threshold should also be reviewed against the business's intervention capacity and the relative costs of missed clients and unnecessary outreach.

## Reproducing the Project

### Earlier Proxy-Dataset Work

The earlier Parts B and C notebooks use the UCI Bank Marketing dataset.

1. Install the dependencies listed in `requirements.txt`.
2. Obtain the `bank-additional-full.csv` dataset from the UCI Machine Learning Repository.
3. Place the dataset in the location expected by the notebooks.
4. Open the notebooks in Jupyter and run them in the documented order, restarting the kernel and running all cells where appropriate.

**Dataset reference**

Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.

### SS3 Client-Data Work

The SS3 notebook expects the following five supplied client data tables in the `data/` directory:

- `table1_client_demographics_registration.csv`
- `table2_onboarding_kyc_day3.csv`
- `table3_app_web_behaviour_day3.csv`
- `table4_funding_account_status.csv`
- `table5_marketing_acquisition.csv`

Place the files in the expected location, verify that the notebook paths match the folder structure, and run `SS3_PartB.ipynb` from top to bottom. Use the results produced by a successful full run as the authoritative figures for reporting.

**Data privacy:** Do not commit the supplied client CSV files to a public repository unless you have confirmed that sharing them is authorised. Keep sensitive or restricted data out of public version control.

## Project Status

- **Part A:** Literature review.
- **Parts B and C:** Proxy-dataset preprocessing, feature engineering, model development, evaluation, and comparison.
- **Part D:** Client recommendations report.
- **SS3 Part B:** Logistic regression implementation, evaluation, and visualisation using the supplied STADIOEquities client data.
- **SS3 Part C:** Presentation video linked above.
- **SS3 Part D:** Follow the current study-session instructions for the required discussion and monitoring deliverables.

This repository documents the progression from proxy-data experimentation to a more business-specific client deposit prediction task. The proxy results and SS3 results should be interpreted separately because they use different datasets and prediction contexts.
