# STADIOEquities — Day-3 Activation Prediction: Data Extract

Five tables, **one row per client in each**, split by the operational system each field originates from, as requested. Clients registered between June 2024 and July 2026 — every one is at least 30 days past registration, so the outcome window is complete. `client_id` joins all five tables. Dates are `yyyy-MM-dd`. `acquisition_cost_zar` is ZAR.

## Files

### `table1_client_demographics_registration.csv`
Registration/CRM system — static client attributes fixed at registration.  
Rows: 24,259

| Column | Description |
|---|---|
| `client_id` | String |
| `registration_date` | Date |
| `age` | Integer |
| `province` | Categorical |
| `stated_investment_goal` | Categorical |
| `stated_risk_appetite` | Categorical |
| `acquisition_channel` | Categorical |

### `table2_onboarding_kyc_day3.csv`
Onboarding/KYC system — progress as observed at the day-3 checkpoint.  
Rows: 24,187

| Column | Description |
|---|---|
| `client_id` | String |
| `kyc_status_day3` | Categorical |
| `onboarding_steps_completed_day3` | Integer |
| `step_last_abandoned` | Categorical |
| `time_to_kyc_complete_hours` | Numeric |

### `table3_app_web_behaviour_day3.csv`
App analytics — first-session and day-3 window behaviour.  
Rows: 24,187

| Column | Description |
|---|---|
| `client_id` | String |
| `time_to_first_session_hours` | Numeric |
| `first_session_duration_minutes` | Numeric |
| `screens_viewed_first_session` | Integer |
| `sessions_by_day3` | Integer |
| `device_type` | Categorical |

### `table4_funding_account_status.csv`
Funding ledger — the target variable and day-30 descriptive status.  
Rows: 24,187

| Column | Description |
|---|---|
| `client_id` | String |
| `deposited_within_30_days` | Integer |
| `date_of_first_deposit` | Date |
| `account_status_day30` | Categorical |

### `table5_marketing_acquisition.csv`
Marketing platform — acquisition cost and day-3 nudge engagement.  
Rows: 24,187

| Column | Description |
|---|---|
| `client_id` | String |
| `acquisition_cost_zar` | Numeric |
| `nudge_engagement_day3` | Categorical |

## Data quality notes

This is an extract from live operational systems and has **not** been cleaned. Expect:

- Missing values in optional / conditionally-populated fields
- Inconsistent casing and stray whitespace in some free-text and categorical fields
- A small number of duplicate records
- Occasional out-of-range or implausible values from data-capture errors
- Some date fields captured in inconsistent formats

**Target:** `deposited_within_30_days` in `table4_funding_account_status.csv`.

**The day-3 discipline holds throughout.** Every field in tables 1, 2, 3 and 5 is observable by the **day-3 decision point**:
- `kyc_status_day3`, `onboarding_steps_completed_day3` and `step_last_abandoned` are the state **as at day 3**, not the final state. A client shown as `In Progress` here may well have completed KYC on day 6 — that is not visible in this extract, by design, because it would not have been visible to the model either.
- `time_to_kyc_complete_hours` is null wherever KYC was not complete by day 3, and is capped at 72 hours for the same reason.
- `time_to_first_session_hours` is likewise bounded by the 72-hour window.
- `nudge_engagement_day3` reflects engagement up to day 3 only.

**Only table 4 reaches past day 3**, and neither of its non-target fields is a predictor:
- `date_of_first_deposit` is null where the target is 0 — it is part of the label.
- `account_status_day30` is descriptive only, known after day 30. It distinguishes `Funded & active` from `Funded then dormant`, which is useful for a follow-on retention question but must not enter the activation model.

**`deposit_amount_first` has been excluded**, as you specified — it is only knowable after the outcome and would leak.

**Onboarding flow, confirmed:** **5 steps**, in order — ID Verification, Proof of Address, Bank Account Linking, Risk Questionnaire, Fund Account. `onboarding_steps_completed_day3` therefore ranges 0-5, and `step_last_abandoned` is `None` where the client either completed the flow or had not yet abandoned a step (status Not Started or In Progress).

_Synthetic data supplied for the CAP182 capstone project. Not real client data._