# stadioequities-activation-prediction-
Predicting first-deposit activation for a fictional South African fintech (STADIOEquities) using a day-3 decision point to forecast 30-day conversion

## Part A: Motivation

STADIOEquities has successfully created a digital investment platform that makes investing more accessible to South Africans, including first-time investors who can open an account and purchase fractional shares using relatively small amounts of money. However, the company currently faces a significant challenge in converting registered accounts into funded and active clients. It has approximately 2.3 million registered accounts, but only about 760,000 are classified as funded and active, with 41% of registered accounts never funded (STADIOEquities, 2026). This creates a substantial gap between account acquisition and actual customer engagement. The problem has become more pressing for both the growth and marketing team, who are responsible for designing onboarding nudges, and finance and leadership, who track acquisition spend against recovered revenue: the conversion rate from sign-up to first deposit has declined from 64% to 59%, while the company spends approximately R180 to acquire each account, recovered only once the account becomes active (STADIOEquities, 2026). Customers who register but never deposit therefore represent a missed opportunity that is costly on both fronts.

The briefing pack indicates that customers who drop out of the activation process display patterns relating to their acquisition source, onboarding progress, first-session behaviour and time taken to make their first deposit (STADIOEquities, 2026). However, STADIOEquities currently uses fixed-schedule onboarding emails and nudges for its customer base rather than identifying which individual customers are most likely to activate or disengage. This project will therefore investigate whether Data Science can be used to anticipate which newly registered customers are unlikely to activate, so that the growth team can prioritise interventions and leadership can better forecast recovery of acquisition spend (the precise prediction window and decision point are defined in Part B). The project directly supports the company's 2030 strategic priority of activating existing accounts, and is feasible given that STADIOEquities already holds relevant data covering app and web behaviour, account registration and funding, demographics, marketing activity and onboarding progress — providing the information needed to investigate behavioural patterns and develop a predictive model.

Predicting first-deposit activation is therefore a valuable Data Science problem for STADIOEquities.

## Part B: Problem Statement

STADIOEquities does not currently know, at the level of an individual client, which newly registered accounts are unlikely to progress to a first deposit, or how early in the registration journey that outcome becomes meaningfully predictable. This gap matters directly to the growth and marketing team, who currently send the same fixed-schedule onboarding emails and nudges to every new registrant regardless of their likelihood of activating (STADIOEquities, 2026), and to finance and leadership, who need to distinguish accounts likely to recover the R180 acquisition cost from those unlikely to activate at all (STADIOEquities, 2026).

This project investigates whether Data Science can predict, within 30 days of registration, whether a newly registered client will make a first deposit, using a decision point at day 3 — early enough in the funnel that onboarding progress and first-session behaviour are already observable, but before most drop-off has occurred, so that an intervention can still change the outcome. The outcome variable is binary (first deposit made within 30 days: yes/no), making this a supervised classification problem rather than a regression or clustering one.

The problem is answerable using data STADIOEquities already holds: app and web behaviour, account registration and funding records, client demographics, marketing and acquisition data, and onboarding progress are all captured from the point of registration (STADIOEquities, 2026), providing the features needed to model the day-3 decision point against the 30-day outcome.

This problem statement is scoped to first-deposit activation only. It does not address dormancy or churn among accounts that have already activated, client segmentation by investing style, or transaction-monitoring/compliance alerting — each of which appears as a separate, related priority in STADIOEquities' 2030 strategy and headwinds (STADIOEquities, 2026), but falls outside the scope of this project.

## Repository Structure

- data/ - Part C data request and datasets
- preprocessing/ - cleaning and preparing the data
- feature-extraction/ - building model features
- modelling/ - training and fitting the model
- evaluation/ - testing and evaluating model performance
- visualisation/ - charts and graphics
- utils/ - helper and comparison scripts


## RAAIDD Log
CAP182 Capstone Project: STADIOEquities

**Risks**

| # | Risk | Mitigation |
|---|---|---|
| 1 | The day-3 window may not contain enough signal to predict a 30-day outcome reliably: onboarding and first-session behaviour this early could be too sparse or noisy to separate future depositors from non-depositors. | Benchmark day-3 model performance against a later checkpoint (e.g. day-7) during evaluation to quantify the accuracy trade-off of intervening earlier. |
| 2 | Class imbalance in the target variable: roughly 41% of accounts never fund at all, but the exact split within a 30-day window is unknown, so the model may default to predicting the majority class rather than genuinely discriminating. | Check class balance during EDA; apply resampling, class weighting, or threshold adjustment if the split is skewed. |

**Actions**

| # | Action | Stage |
|---|---|---|
| 1 | Clean and merge the five data-request tables into a single modelling dataset, resolving the client_id joins and handling nulls (e.g. time_to_kyc_complete_hours where KYC isn't finished by day 3). | Data preparation |
| 2 | Engineer features from raw fields where the day-3 signal isn't already in usable form (e.g. converting step_last_abandoned into a one-hot encoded flag, deriving a funnel-progress score from onboarding steps completed). | Feature engineering |

**Assumptions**

| # | Assumption | Why it needs stating |
|---|---|---|
| 1 | Day-3 behavioural and onboarding signals are genuinely informative of the 30-day deposit outcome; this is the core premise of the problem statement and hasn't yet been tested against real data. | If false, the whole day-3/day-30 framing (and the intervention timing it supports) would need revisiting. |
| 2 | STADIOEquities can supply all requested fields at the granularity specified in Part C (e.g. per-session timestamps, exact onboarding step counts); the briefing pack describes the data landscape at a high level but doesn't guarantee field-level availability. | Missing or coarser data than requested would force feature substitutions or a revised scope. |

**Issues**

| # | Issue |
|---|---|
| 1 | The briefing pack does not specify the exact number or definition of onboarding steps, so onboarding_steps_completed_day3's valid range (0-N) could not be finalised in Part C and was flagged for the client to confirm. |

**Decisions**

| # | Decision |
|---|---|
| 1 | Framed the problem as binary supervised classification (deposited within 30 days: yes/no) rather than regression or clustering, using a day-3 decision point and 30-day outcome window, and excluded deposit_amount_first as a predictor to avoid data leakage. |

**Dependencies**

| # | Dependency |
|---|---|
| 1 | The requested data (Part C) must be received from STADIOEquities before any data cleaning or exploratory analysis can begin. |
| 2 | Feature engineering and the day-3/day-7 benchmark comparison (Risk 1's mitigation) must be completed before model training and evaluation, since both depend on a finalised, leakage-checked feature set. |






