import json
from pathlib import Path

from sklearn.metrics import precision_recall_fscore_support

from services.risk_engine.app.main import assess_ingredient_rules


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_CASES_PATH = PROJECT_ROOT / "data" / "golden_cases.json"


def normalize_expected_label(label):
    mapping = {
        "safe": "safe",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "caution": "medium",
        "avoid": "high",
    }
    return mapping[label]


def test_golden_cases_risk_level():
    with open(GOLDEN_CASES_PATH, "r", encoding="utf-8") as file:
        cases = json.load(file)

    y_true = []
    y_pred = []

    for case in cases:
        expected = normalize_expected_label(case["expected"])

        predicted, score, reasons = assess_ingredient_rules(
            case["input"],
            skin_type=case.get("skin_type"),
            sensitivity=case.get("sensitivity"),
        )

        y_true.append(expected)
        y_pred.append(predicted)

        assert predicted == expected, (
            f"Case failed: {case.get('name', case['input'])}. "
            f"Expected {expected}, got {predicted}. Reasons: {reasons}"
        )

    labels = ["safe", "low", "medium", "high"]

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )

    false_negatives = 0
    risky_cases = 0

    for true_label, pred_label in zip(y_true, y_pred):
        if true_label in ["medium", "high"]:
            risky_cases += 1
            if pred_label == "safe":
                false_negatives += 1

    fnr = false_negatives / risky_cases if risky_cases else 0.0

    print("\nGolden Regression Metrics")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1:        {f1:.3f}")
    print(f"FNR:       {fnr:.3f}")