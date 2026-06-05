from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import mlflow
from sklearn.metrics import f1_score, precision_score, recall_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from services.risk_engine.app.main import (
    AnalyzerRequest,
    ProductInput,
    analyze_payload,
)
from services.risk_engine.app.rules import PAIR_RULES, STACKING_INGREDIENTS


GOLDEN_CASES_PATH = PROJECT_ROOT / "data" / "golden_cases.json"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"
DECISION_LOG = MLRUNS_DIR / "decisions.log"


def normalize_expected_label(label: str) -> str:
    mapping = {
        "safe": "low",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "caution": "medium",
        "avoid": "high",
    }
    return mapping[label]


def build_request(ingredients: list[str]) -> AnalyzerRequest:
    products = [
        ProductInput(
            id=f"p{i + 1}",
            name=ingredient,
            found=True,
            interaction_relevant_ingredients=[ingredient],
        )
        for i, ingredient in enumerate(ingredients)
    ]

    return AnalyzerRequest(products=products, unknown_products=[])


def compute_fnr(y_true: list[str], y_pred: list[str]) -> float:
    false_negatives = 0
    risky_cases = 0

    for truth, pred in zip(y_true, y_pred):
        if truth in ["medium", "high"]:
            risky_cases += 1
            if pred == "low":
                false_negatives += 1

    return false_negatives / risky_cases if risky_cases else 0.0


def promotion_decision(fnr: float, f1: float) -> str:
    if fnr < 0.05 and f1 > 0.85:
        return "PROMOTE"
    if 0.05 <= fnr <= 0.10:
        return "HOLD"
    return "REJECT"


def analyzer_rule_version() -> str:
    return f"pair_rules={len(PAIR_RULES)};stacking_rules={len(STACKING_INGREDIENTS)}"


def main() -> None:
    MLRUNS_DIR.mkdir(exist_ok=True)

    with open(GOLDEN_CASES_PATH, "r", encoding="utf-8") as file:
        cases = json.load(file)

    y_true = []
    y_pred = []

    for case in cases:
        expected = normalize_expected_label(case["expected"])
        result = analyze_payload(build_request(case["input"]))
        predicted = result.risk_level

        y_true.append(expected)
        y_pred.append(predicted)

    labels = ["low", "medium", "high"]

    precision = precision_score(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )
    recall = recall_score(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )
    f1 = f1_score(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )
    fnr = compute_fnr(y_true, y_pred)
    decision = promotion_decision(fnr, f1)

    mlflow.set_tracking_uri(f"file:///{MLRUNS_DIR.as_posix()}")
    mlflow.set_experiment("analyzer-golden-evaluation")

    with mlflow.start_run(run_name="golden-regression-evaluation"):
        mlflow.log_param("analyzer_rule_version", analyzer_rule_version())
        mlflow.log_param("golden_cases_count", len(cases))
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("fnr", fnr)
        mlflow.log_param("promotion_decision", decision)

    with open(DECISION_LOG, "a", encoding="utf-8") as log:
        log.write(
            f"{datetime.now(timezone.utc).isoformat()} | "
            f"decision={decision} | "
            f"precision={precision:.4f} | "
            f"recall={recall:.4f} | "
            f"f1={f1:.4f} | "
            f"fnr={fnr:.4f}\n"
        )

    print("Evaluation completed.")
    print(f"Analyzer rule version: {analyzer_rule_version()}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1:        {f1:.3f}")
    print(f"FNR:       {fnr:.3f}")
    print(f"Decision:  {decision}")
    print(f"Decision log: {DECISION_LOG}")


if __name__ == "__main__":
    main()