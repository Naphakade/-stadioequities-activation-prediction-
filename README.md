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
