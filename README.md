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







