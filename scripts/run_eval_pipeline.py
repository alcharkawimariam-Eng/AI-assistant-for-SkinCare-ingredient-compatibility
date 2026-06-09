"""
MLflow Evaluation Pipeline — Skincare AI Copilot
=================================================

Loads golden_cases.json, runs every case through the risk engine,
computes precision / recall / F1 / false-negative rate, logs all metrics
and artifacts to MLflow, and prints a PROMOTE / REVIEW / REJECT decision.

Usage
-----
# With Docker Compose running (mlflow on port 5000):
    python scripts/run_eval_pipeline.py

# Against a remote MLflow server:
    MLFLOW_TRACKING_URI=http://<host>:5000 python scripts/run_eval_pipeline.py

# Against a specific experiment name:
    MLFLOW_EXPERIMENT_NAME=skincare-risk-v2 python scripts/run_eval_pipeline.py

Promotion thresholds (can be overridden via env vars)
-----------------------------------------------------
    MIN_F1=0.80          Macro F1 across low/medium/high
    MAX_FNR=0.10         False-negative rate on risky cases (medium+high missed as low)
    MIN_HIGH_RECALL=0.90 Recall specifically for high-risk cases

Exit codes
----------
    0 — PROMOTE (all thresholds met)
    1 — REVIEW  (some thresholds not met but no hard failure)
    2 — error   (exception during evaluation)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mlflow
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)

from services.risk_engine.app.analyzer import analyze_payload
from services.risk_engine.app.schemas import AnalyzerRequest, ProductInput

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "skincare-risk-engine")

GOLDEN_CASES_PATH = ROOT / "data" / "golden_cases.json"

# Promotion thresholds
MIN_F1 = float(os.getenv("MIN_F1", "0.80"))
MAX_FNR = float(os.getenv("MAX_FNR", "0.10"))
MIN_HIGH_RECALL = float(os.getenv("MIN_HIGH_RECALL", "0.90"))

LABEL_MAP = {
    "safe": "low",
    "low": "low",
    "caution": "medium",
    "medium": "medium",
    "avoid": "high",
    "high": "high",
}
LABELS = ["low", "medium", "high"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_analyzer_request(ingredients: list[str]) -> AnalyzerRequest:
    products = [
        ProductInput(
            id=f"p{i+1}",
            name=ingredient,
            found=True,
            interaction_relevant_ingredients=[ingredient],
        )
        for i, ingredient in enumerate(ingredients)
    ]
    return AnalyzerRequest(products=products, unknown_products=[])


def evaluate_golden_cases(cases: list[dict]) -> dict:
    y_true: list[str] = []
    y_pred: list[str] = []
    failures: list[dict] = []

    for case in cases:
        expected = LABEL_MAP[case["expected"]]
        result = analyze_payload(build_analyzer_request(case["input"]))
        predicted = result.risk_level

        y_true.append(expected)
        y_pred.append(predicted)

        if predicted != expected:
            failures.append({
                "input": case["input"],
                "expected": expected,
                "predicted": predicted,
                "issues": [i.message for i in result.issues],
            })

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, average="macro", zero_division=0
    )

    per_class_p, per_class_r, per_class_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, average=None, zero_division=0
    )

    # False negative rate: risky cases (medium/high) predicted as low
    risky_indices = [i for i, t in enumerate(y_true) if t in ("medium", "high")]
    fn_count = sum(1 for i in risky_indices if y_pred[i] == "low")
    fnr = fn_count / len(risky_indices) if risky_indices else 0.0

    # High-risk recall
    high_indices = [i for i, t in enumerate(y_true) if t == "high"]
    high_correct = sum(1 for i in high_indices if y_pred[i] == "high")
    high_recall = high_correct / len(high_indices) if high_indices else 1.0

    report = classification_report(y_true, y_pred, labels=LABELS, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=LABELS).tolist()

    return {
        "total_cases": len(cases),
        "correct": len(cases) - len(failures),
        "failures": failures,
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "macro_f1": round(float(f1), 4),
        "fnr": round(float(fnr), 4),
        "high_risk_recall": round(float(high_recall), 4),
        "per_class": {
            label: {
                "precision": round(float(per_class_p[i]), 4),
                "recall": round(float(per_class_r[i]), 4),
                "f1": round(float(per_class_f1[i]), 4),
            }
            for i, label in enumerate(LABELS)
        },
        "classification_report": report,
        "confusion_matrix": cm,
    }


def make_promotion_decision(metrics: dict) -> tuple[str, list[str]]:
    """Return (decision, reasons). Decision is PROMOTE, REVIEW, or REJECT."""
    reasons = []

    if metrics["macro_f1"] < MIN_F1:
        reasons.append(
            f"macro_f1={metrics['macro_f1']:.3f} < threshold {MIN_F1:.3f}"
        )

    if metrics["fnr"] > MAX_FNR:
        reasons.append(
            f"fnr={metrics['fnr']:.3f} > threshold {MAX_FNR:.3f} "
            f"(risky cases missed as low risk)"
        )

    if metrics["high_risk_recall"] < MIN_HIGH_RECALL:
        reasons.append(
            f"high_risk_recall={metrics['high_risk_recall']:.3f} "
            f"< threshold {MIN_HIGH_RECALL:.3f}"
        )

    if not reasons:
        return "PROMOTE", []
    return "REVIEW", reasons


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"MLflow tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"Experiment: {MLFLOW_EXPERIMENT_NAME}")
    print(f"Golden cases path: {GOLDEN_CASES_PATH}")

    if not GOLDEN_CASES_PATH.exists():
        print(f"ERROR: Golden cases file not found at {GOLDEN_CASES_PATH}")
        return 2

    with open(GOLDEN_CASES_PATH, encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} golden cases.")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="golden-eval"):
        # Log thresholds as params
        mlflow.log_param("golden_cases_count", len(cases))
        mlflow.log_param("min_f1_threshold", MIN_F1)
        mlflow.log_param("max_fnr_threshold", MAX_FNR)
        mlflow.log_param("min_high_recall_threshold", MIN_HIGH_RECALL)
        mlflow.log_param("prompt_version", os.getenv("PROMPT_VERSION", "v1"))

        # Evaluate
        metrics = evaluate_golden_cases(cases)

        # Log metrics
        mlflow.log_metric("macro_precision", metrics["macro_precision"])
        mlflow.log_metric("macro_recall", metrics["macro_recall"])
        mlflow.log_metric("macro_f1", metrics["macro_f1"])
        mlflow.log_metric("false_negative_rate", metrics["fnr"])
        mlflow.log_metric("high_risk_recall", metrics["high_risk_recall"])
        mlflow.log_metric("total_cases", metrics["total_cases"])
        mlflow.log_metric("correct_cases", metrics["correct"])
        mlflow.log_metric("failed_cases", len(metrics["failures"]))

        for label, scores in metrics["per_class"].items():
            mlflow.log_metric(f"precision_{label}", scores["precision"])
            mlflow.log_metric(f"recall_{label}", scores["recall"])
            mlflow.log_metric(f"f1_{label}", scores["f1"])

        # Log artifacts
        report_path = ROOT / "mlops" / "eval_report.txt"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(metrics["classification_report"])
        mlflow.log_artifact(str(report_path))

        failures_path = ROOT / "mlops" / "eval_failures.json"
        failures_path.write_text(
            json.dumps(metrics["failures"], indent=2, ensure_ascii=False)
        )
        mlflow.log_artifact(str(failures_path))

        # Promotion decision
        decision, reasons = make_promotion_decision(metrics)
        mlflow.log_param("promotion_decision", decision)

        # Print summary
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        print(f"  Total cases:      {metrics['total_cases']}")
        print(f"  Correct:          {metrics['correct']}")
        print(f"  Failures:         {len(metrics['failures'])}")
        print(f"  Macro F1:         {metrics['macro_f1']:.3f}  (threshold ≥ {MIN_F1})")
        print(f"  FNR:              {metrics['fnr']:.3f}  (threshold ≤ {MAX_FNR})")
        print(f"  High-risk recall: {metrics['high_risk_recall']:.3f}  (threshold ≥ {MIN_HIGH_RECALL})")
        print()
        print(metrics["classification_report"])

        if reasons:
            print("Thresholds NOT met:")
            for r in reasons:
                print(f"  ✗ {r}")
        else:
            print("All thresholds met.")

        print()
        print(f"DECISION: {decision}")
        print("=" * 60)

        if decision == "PROMOTE":
            print("Model PROMOTED. Safe to deploy.")
            return 0
        else:
            print("Model flagged for REVIEW. Do not promote without investigation.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
