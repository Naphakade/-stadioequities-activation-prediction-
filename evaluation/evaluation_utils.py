"""Shared evaluation helpers for the STADIOEquities performance notebooks."""
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score,
                             average_precision_score, brier_score_loss, confusion_matrix)


def compute_metrics(y_true, y_prob, threshold=0.5):
    """Return a dictionary of classification metrics for one set of predictions."""
    y_true = np.asarray(y_true)
    y_pred = (np.asarray(y_prob) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Balanced accuracy": balanced_accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall (sensitivity)": recall_score(y_true, y_pred),
        "Specificity": tn / (tn + fp),
        "F1-Score": f1_score(y_true, y_pred),
        "ROC AUC": roc_auc_score(y_true, y_prob),
        "PR AUC (average precision)": average_precision_score(y_true, y_prob),
        "Brier score": brier_score_loss(y_true, y_prob),
    }


def bootstrap_metrics(y_true, y_prob, n_boot=1000, seed=42, threshold=0.5):
    """Point estimates with 95% bootstrap confidence intervals (percentile method)."""
    y_true, y_prob = np.asarray(y_true), np.asarray(y_prob)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    samples = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if y_true[idx].min() == y_true[idx].max():
            continue
        samples.append(compute_metrics(y_true[idx], y_prob[idx], threshold))
    samples = pd.DataFrame(samples)
    point = pd.Series(compute_metrics(y_true, y_prob, threshold))
    return pd.DataFrame({
        "Value": point,
        "95% CI lower": samples.quantile(0.025),
        "95% CI upper": samples.quantile(0.975),
    }).round(3)


def gains_table(y_true, y_prob, shares=(0.1, 0.2, 0.3, 0.5)):
    """Share of converters captured, and lift, when contacting the top-ranked customers."""
    y_true = np.asarray(y_true)
    order = np.argsort(-np.asarray(y_prob))
    gains = np.cumsum(y_true[order]) / y_true.sum()
    rows = []
    for s in shares:
        k = int(round(s * len(y_true)))
        captured = gains[k - 1]
        rows.append({"Top share contacted": f"{s:.0%}",
                     "Converters captured": round(captured, 3),
                     "Lift": round(captured / s, 2)})
    return pd.DataFrame(rows).set_index("Top share contacted")


def threshold_table(y_true, y_prob, thresholds=(0.3, 0.4, 0.5, 0.6, 0.7)):
    """Precision, recall and F1 at several classification thresholds."""
    rows = []
    for t in thresholds:
        m = compute_metrics(y_true, y_prob, t)
        rows.append({"Threshold": t,
                     "Share predicted 'yes'": round(float((np.asarray(y_prob) >= t).mean()), 3),
                     "Precision": round(m["Precision"], 3),
                     "Recall": round(m["Recall (sensitivity)"], 3),
                     "F1-Score": round(m["F1-Score"], 3),
                     "Accuracy": round(m["Accuracy"], 3)})
    return pd.DataFrame(rows).set_index("Threshold")


def paired_bootstrap_difference(y_true, prob_a, prob_b, n_boot=1000, seed=42, threshold=0.5):
    """Paired bootstrap of the difference (A minus B) in each metric, with a 95% CI and
    a two-sided bootstrap p-value for the null hypothesis of no difference."""
    y_true, prob_a, prob_b = map(np.asarray, (y_true, prob_a, prob_b))
    rng = np.random.default_rng(seed)
    n = len(y_true)
    diffs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if y_true[idx].min() == y_true[idx].max():
            continue
        a = compute_metrics(y_true[idx], prob_a[idx], threshold)
        b = compute_metrics(y_true[idx], prob_b[idx], threshold)
        diffs.append({k: a[k] - b[k] for k in a})
    diffs = pd.DataFrame(diffs)
    a_full = compute_metrics(y_true, prob_a, threshold)
    b_full = compute_metrics(y_true, prob_b, threshold)
    p = diffs.apply(lambda d: min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean())))
    return pd.DataFrame({
        "Difference (A - B)": pd.Series({k: a_full[k] - b_full[k] for k in a_full}),
        "95% CI lower": diffs.quantile(0.025),
        "95% CI upper": diffs.quantile(0.975),
        "Bootstrap p-value": p.apply(lambda v: "<0.001" if v < 0.001 else f"{v:.3f}"),
    }).round(3)
