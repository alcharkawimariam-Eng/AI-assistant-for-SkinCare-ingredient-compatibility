from __future__ import annotations

from typing import Dict, FrozenSet

PAIR_RULES: Dict[FrozenSet[str], dict] = {
    frozenset({"retinol", "glycolic acid"}): {
        "risk_level": "high",
        "message": "Retinol and glycolic acid together may cause irritation when used in the same routine.",
        "recommendation": "Use them on alternating nights.",
    },
    frozenset({"retinol", "salicylic acid"}): {
        "risk_level": "high",
        "message": "Retinol and salicylic acid together may over-dry or irritate the skin.",
        "recommendation": "Separate their use by time or day.",
    },
    frozenset({"retinol", "benzoyl peroxide"}): {
        "risk_level": "high",
        "message": "Retinol and benzoyl peroxide together may be irritating and hard to tolerate.",
        "recommendation": "Do not layer them in the same routine.",
    },
    frozenset({"salicylic acid", "glycolic acid"}): {
        "risk_level": "high",
        "message": "Salicylic acid and glycolic acid together may over-exfoliate the skin.",
        "recommendation": "Use only one exfoliating product per routine.",
    },
    frozenset({"glycolic acid", "lactic acid"}): {
        "risk_level": "medium",
        "message": "Using multiple AHAs together can increase exfoliation and irritation risk.",
        "recommendation": "Avoid layering multiple AHA exfoliants in the same routine.",
    },
    frozenset({"vitamin c", "glycolic acid"}): {
        "risk_level": "medium",
        "message": "Vitamin C and glycolic acid may be too strong together for sensitive skin.",
        "recommendation": "Use one in the morning and the other at night.",
    },
    frozenset({"vitamin c", "salicylic acid"}): {
        "risk_level": "medium",
        "message": "Vitamin C and salicylic acid may increase irritation in some users.",
        "recommendation": "Patch test and avoid stacking if irritation occurs.",
    },
    frozenset({"aha", "bha"}): {
        "risk_level": "high",
        "message": "Combining AHA and BHA can over-exfoliate the skin and increase irritation risk.",
        "recommendation": "Avoid using multiple exfoliating acids in the same routine.",
    },
    frozenset({"retinol", "aha"}): {
        "risk_level": "high",
        "message": "Retinol combined with AHAs may strongly increase irritation and skin sensitivity.",
        "recommendation": "Use retinol and AHAs on different nights.",
    },
    frozenset({"benzoyl peroxide", "aha"}): {
        "risk_level": "high",
        "message": "Benzoyl peroxide combined with AHAs may cause excessive dryness and irritation.",
        "recommendation": "Do not layer benzoyl peroxide with exfoliating acids.",
    },
    frozenset({"vitamin c", "copper peptides"}): {
        "risk_level": "medium",
        "message": "Copper peptides may reduce vitamin C stability when used in the same routine.",
        "recommendation": "Use vitamin C and copper peptides at different times of day.",
    },
    frozenset({"retinol", "vitamin c"}): {
        "risk_level": "medium",
        "message": "Retinol and vitamin C together may increase irritation for sensitive skin.",
        "recommendation": "Use vitamin C in the morning and retinol at night.",
    },
    frozenset({"fragrance", "retinol"}): {
        "risk_level": "medium",
        "message": "Fragrance may increase irritation risk when combined with retinol.",
        "recommendation": "Avoid fragranced products when using retinol, especially on sensitive skin.",
    },
    frozenset({"fragrance", "aha"}): {
        "risk_level": "medium",
        "message": "Fragrance with acids may irritate sensitive skin.",
        "recommendation": "Use fragrance-free products when applying exfoliating acids.",
    },
    frozenset({"fragrance", "salicylic acid"}): {
        "risk_level": "medium",
        "message": "Fragrance combined with salicylic acid may increase irritation risk, especially for sensitive skin.",
        "recommendation": "Use a fragrance-free product when applying salicylic acid.",
    },
    frozenset({"aha", "physical exfoliant"}): {
        "risk_level": "high",
        "message": "Combining exfoliating acids with physical exfoliation may damage the skin barrier.",
        "recommendation": "Avoid using chemical and physical exfoliants in the same routine.",
    },

    # Haircare rules
    frozenset({"protein", "keratin"}): {
        "risk_level": "medium",
        "message": "Protein and keratin together may contribute to protein overload in haircare routines.",
        "recommendation": "Balance protein treatments with moisturizing products.",
    },
    frozenset({"sulfates", "color-treated hair"}): {
        "risk_level": "medium",
        "message": "Sulfates may fade color-treated hair.",
        "recommendation": "Use sulfate-free products for color-treated hair.",
    },
    frozenset({"silicones", "curly hair"}): {
        "risk_level": "medium",
        "message": "Heavy silicones may weigh down curly hair.",
        "recommendation": "Clarify periodically or choose lighter silicone-free products.",
    },
    frozenset({"dimethicone", "curly hair"}): {
        "risk_level": "medium",
        "message": "Dimethicone is a silicone that may build up or weigh down curly hair.",
        "recommendation": "Use clarifying shampoo occasionally if using dimethicone on curly hair.",
    },
}

STACKING_INGREDIENTS = {
    "retinol": {
        "risk_level": "high",
        "message": "Multiple retinoid products detected. This may increase irritation.",
        "recommendation": "Use only one retinoid product per routine.",
    },
    "salicylic acid": {
        "risk_level": "medium",
        "message": "Multiple salicylic acid products detected. This may over-dry the skin.",
        "recommendation": "Reduce frequency or avoid stacking.",
    },
    "glycolic acid": {
        "risk_level": "medium",
        "message": "Multiple glycolic acid products detected. This may over-exfoliate the skin.",
        "recommendation": "Use one exfoliating product at a time.",
    },
    "lactic acid": {
        "risk_level": "medium",
        "message": "Multiple lactic acid products detected. This may increase exfoliation and irritation risk.",
        "recommendation": "Use one AHA exfoliant per routine.",
    },
    "benzoyl peroxide": {
        "risk_level": "high",
        "message": "Multiple benzoyl peroxide products detected. This may strongly irritate the skin.",
        "recommendation": "Use only one benzoyl peroxide product per routine.",
    },
    "vitamin c": {
        "risk_level": "low",
        "message": "Multiple vitamin C products detected. This may be redundant or irritating for sensitive skin.",
        "recommendation": "One vitamin C product is usually enough.",
    },
    "protein": {
        "risk_level": "medium",
        "message": "Multiple protein-heavy hair products detected. This may contribute to protein overload.",
        "recommendation": "Balance protein treatments with moisturizing haircare products.",
    },
}


# ---------------------------------------------------------------------------
# Synergy rules — pairs that work well together
# ---------------------------------------------------------------------------
SYNERGY_RULES: dict = {
    frozenset({"niacinamide", "hyaluronic acid"}): "Niacinamide and hyaluronic acid are a supportive, non-irritating duo for hydration and barrier support.",
    frozenset({"retinol", "hyaluronic acid"}): "Hyaluronic acid helps buffer retinol dryness and supports hydration.",
    frozenset({"retinol", "ceramides"}): "Ceramides help support the skin barrier around retinol use.",
    frozenset({"vitamin c", "sunscreen"}): "Vitamin C and sunscreen work well together in a morning routine for antioxidant and UV protection.",
    frozenset({"niacinamide", "retinol"}): "Niacinamide can help calm potential retinol irritation.",
    frozenset({"salicylic acid", "niacinamide"}): "Niacinamide can help reduce dryness or redness after salicylic acid.",
}

INGREDIENT_STRENGTH: dict[str, str] = {
    "retinol": "High-potency retinoid. Start low and increase slowly.",
    "glycolic acid": "Strong AHA. Can cause sensitivity with frequent use.",
    "salicylic acid": "Moderate BHA. Helpful for oily/acne-prone skin but can be drying.",
    "benzoyl peroxide": "Strong acne treatment. Can be drying and irritating.",
    "vitamin c": "Potency depends on the form and concentration.",
    "niacinamide": "Generally low-irritation and useful for barrier support and oil control.",
    "hyaluronic acid": "Gentle humectant suitable for most skin types.",
    "ceramides": "Barrier-supporting lipids suitable for sensitive or dry skin.",
}

INGREDIENT_CAUTIONS: dict[str, str] = {
    "retinol": "May increase sensitivity. Use sunscreen and introduce slowly.",
    "glycolic acid": "May increase sun sensitivity. Use SPF.",
    "salicylic acid": "Can dry the skin if overused.",
    "benzoyl peroxide": "Can bleach fabrics and may irritate dry or sensitive skin.",
    "vitamin c": "Can be unstable in light or air depending on the form.",
    "fragrance": "Common sensitizer. Patch testing is recommended for reactive skin.",
}

INGREDIENT_PH: dict[str, str] = {
    "vitamin c": "Vitamin C effectiveness depends on form; L-ascorbic acid usually works best at low pH.",
    "glycolic acid": "Glycolic acid is typically most effective in an acidic pH range.",
    "salicylic acid": "Salicylic acid works best in an acidic pH range.",
    "retinol": "Retinol is generally compatible with a wider pH range.",
    "niacinamide": "Niacinamide is stable across a relatively wide pH range.",
    "hyaluronic acid": "Hyaluronic acid is generally effective across a skin-friendly pH range.",
}

