# STADIOEquities Activation Prediction

CAP182 Capstone Project. This project predicts whether a newly registered STADIOEquities customer will make a first deposit (activation). Because STADIOEquities data is not yet available, the approach is tested on the public UCI Bank Marketing dataset, whose binary target (whether a customer converts to a financial product) serves as a proxy.

## Part A: Literature review

See the [`literature-review`](literature-review) folder.

## Part B: Modelling

| Step | Description | Code |
|---|---|---|
| 1 | [Preprocessing](Preprocessing.MD) | `preprocessing/preprocessing.ipynb` |
| 2 | [Feature Engineering](FeatureEngineering.MD) | `feature-extraction/feature_engineering.ipynb` |
| 3 | [Model 1: Logistic Regression](Model1.MD) | `modelling/model1_logistic_regression.ipynb` |
| 4 | [Model 2: Decision Tree](Model2.MD) | `modelling/model2_decision_tree.ipynb` |

Run the notebooks in the order above.

## Setup

1. Install the required packages: `pip install -r requirements.txt`
2. Place `bank-additional-full.csv` in the `data` folder. It can be downloaded from https://archive.ics.uci.edu/dataset/222/bank+marketing
3. Open each notebook in Jupyter and run **Kernel → Restart Kernel and Run All Cells**.

## Dataset

Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [Dataset]. UCI Machine Learning Repository. doi: 10.24432/C5K306.
