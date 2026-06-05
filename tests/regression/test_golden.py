import json
from pathlib import Path

from sklearn.metrics import precision_recall_fscore_support

from services.risk_engine.app.main import (
    AnalyzerRequest,
    ProductInput,
    analyze_payload,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_CASES_PATH = PROJECT_ROOT / "data" / "golden_cases.json"


def normalize_expected_label(label):
    mapping = {
        "safe": "low",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "caution": "medium",
        "avoid": "high",
    }
    return mapping[label]


def build_request(ingredients):
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


def test_golden_cases_risk_level():
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

        assert predicted == expected, (
            f"Case failed: {case.get('name', case['input'])}. "
            f"Expected {expected}, got {predicted}. Issues: {result.issues}"
        )

    labels = ["low", "medium", "high"]

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
            if pred_label == "low":
                false_negatives += 1

    fnr = false_negatives / risky_cases if risky_cases else 0.0

    print("\nGolden Regression Metrics")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1:        {f1:.3f}")
    print(f"FNR:       {fnr:.3f}")