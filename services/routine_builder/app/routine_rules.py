"""
Routine builder rules.

Each entry maps (skin_type, concern) -> a full routine recommendation.
Fallback keys: ("any", concern) and ("any", "general").
"""
from __future__ import annotations

from typing import Dict, List


class RoutineTemplate:
    def __init__(
        self,
        title: str,
        summary: str,
        morning_routine: List[str],
        night_routine: List[str],
        suggested_products: List[str],
        usage_order: List[str],
        ai_notes: List[str],
    ):
        self.title = title
        self.summary = summary
        self.morning_routine = morning_routine
        self.night_routine = night_routine
        self.suggested_products = suggested_products
        self.usage_order = usage_order
        self.ai_notes = ai_notes


# ---------------------------------------------------------------------------
# Template registry: key = (skin_type, concern)
# ---------------------------------------------------------------------------
ROUTINE_TEMPLATES: Dict[tuple, RoutineTemplate] = {

    # ── OILY / ACNE ──────────────────────────────────────────────────────────
    ("oily", "acne"): RoutineTemplate(
        title="Oily Skin Acne-Control Routine",
        summary="A balancing routine targeting excess sebum and breakouts without over-stripping the skin barrier.",
        morning_routine=[
            "Gentle foaming or gel cleanser (look for salicylic acid 0.5–1%)",
            "Lightweight alcohol-free toner (niacinamide 5–10%)",
            "Oil-free moisturizer (gel texture preferred)",
            "Broad-spectrum sunscreen SPF 50 (non-comedogenic)",
        ],
        night_routine=[
            "Double cleanse: micellar water first, then gel cleanser",
            "BHA exfoliant (salicylic acid 2%), 3× per week maximum",
            "Niacinamide or azelaic acid serum",
            "Lightweight non-comedogenic moisturizer",
            "Spot treatment (benzoyl peroxide 2.5%) on active breakouts only",
        ],
        suggested_products=[
            "Gel cleanser with salicylic acid",
            "Paula's Choice BHA 2% Exfoliant or similar",
            "The Ordinary Niacinamide 10% + Zinc 1%",
            "Oil-free gel moisturizer (e.g. Neutrogena Hydro Boost)",
            "Non-comedogenic SPF 50 sunscreen",
        ],
        usage_order=[
            "Cleanser → Toner → Treatment serum → Moisturizer → SPF (AM)",
            "Cleanser → Exfoliant (3×/week) OR Serum → Spot treatment → Moisturizer (PM)",
        ],
        ai_notes=[
            "Avoid harsh scrubs — physical exfoliation worsens inflammation.",
            "Niacinamide and salicylic acid can be safely layered.",
            "Use benzoyl peroxide as a spot treatment, not all-over, to avoid excessive dryness.",
            "Change pillowcases frequently and avoid touching your face.",
        ],
    ),

    ("oily", "dryness"): RoutineTemplate(
        title="Oily Skin — Hydration Without Heaviness",
        summary="Oily skin can still be dehydrated. This routine adds lightweight hydration without triggering excess sebum.",
        morning_routine=[
            "Gentle foaming cleanser",
            "Hydrating toner (hyaluronic acid, no alcohol)",
            "Lightweight water-based serum (hyaluronic acid)",
            "Oil-free gel moisturizer",
            "Non-comedogenic SPF 50",
        ],
        night_routine=[
            "Gentle foaming cleanser",
            "Hydrating essence or toner",
            "Hyaluronic acid serum",
            "Gel-cream moisturizer",
        ],
        suggested_products=[
            "CeraVe Foaming Cleanser",
            "The Ordinary Hyaluronic Acid 2% + B5",
            "Neutrogena Hydro Boost Water Gel",
            "Non-comedogenic broad-spectrum SPF",
        ],
        usage_order=[
            "Cleanser → Toner → Serum → Moisturizer → SPF (AM)",
            "Cleanser → Essence → Serum → Moisturizer (PM)",
        ],
        ai_notes=[
            "Oily skin can be simultaneously dehydrated — don't skip moisturizer.",
            "Use hyaluronic acid on slightly damp skin to lock in moisture.",
            "Avoid alcohol-based toners — they strip oil temporarily but worsen dehydration.",
        ],
    ),

    ("oily", "pigmentation"): RoutineTemplate(
        title="Oily Skin Brightening & Pigmentation Routine",
        summary="Targets dark spots and uneven tone while managing oil and preventing new breakouts.",
        morning_routine=[
            "Gentle gel cleanser",
            "Vitamin C serum (L-ascorbic acid 10–15% or ascorbyl glucoside)",
            "Oil-free moisturizer",
            "SPF 50+ broad-spectrum (non-negotiable for pigmentation)",
        ],
        night_routine=[
            "Double cleanse",
            "AHA exfoliant (glycolic acid 5–7%), 2–3× per week",
            "Niacinamide serum or azelaic acid 10%",
            "Lightweight moisturizer",
            "Retinol 0.025–0.05% (alternate nights from AHA)",
        ],
        suggested_products=[
            "Vitamin C serum (SkinCeuticals CE Ferulic or budget: TruSkin C serum)",
            "The Ordinary Glycolic Acid 7% Toning Solution",
            "The Ordinary Azelaic Acid 10%",
            "Retinol 0.025% or 0.05% starter formula",
            "SPF 50+ non-comedogenic sunscreen",
        ],
        usage_order=[
            "Cleanser → Vitamin C → Moisturizer → SPF (AM)",
            "Cleanser → AHA (3×/wk) OR Niacinamide → Retinol (alternate nights) → Moisturizer (PM)",
        ],
        ai_notes=[
            "Never skip SPF — UV exposure directly reverses pigmentation treatment.",
            "Do not use Vitamin C and AHA at the same time — separate AM/PM.",
            "Introduce retinol gradually: once a week for 2 weeks, then increase.",
        ],
    ),

    ("oily", "general"): RoutineTemplate(
        title="Oily Skin — General Maintenance Routine",
        summary="A simple, effective daily routine for oily skin with no specific concern.",
        morning_routine=[
            "Gel or foaming cleanser",
            "Niacinamide toner or serum",
            "Lightweight oil-free moisturizer",
            "Non-comedogenic SPF 30–50",
        ],
        night_routine=[
            "Gel cleanser",
            "Optional: BHA 2% exfoliant 2× per week",
            "Niacinamide or lightweight serum",
            "Oil-free moisturizer",
        ],
        suggested_products=[
            "CeraVe Foaming Facial Cleanser",
            "The Ordinary Niacinamide 10% + Zinc 1%",
            "Neutrogena Oil-Free Moisturizer SPF 35",
        ],
        usage_order=[
            "Cleanser → Serum → Moisturizer → SPF (AM)",
            "Cleanser → Exfoliant (2×/wk) → Serum → Moisturizer (PM)",
        ],
        ai_notes=[
            "Keep routines simple — oily skin does not need multiple layers.",
            "Niacinamide regulates sebum production over time.",
        ],
    ),

    # ── DRY / DRYNESS ────────────────────────────────────────────────────────
    ("dry", "dryness"): RoutineTemplate(
        title="Dry Skin Deep Hydration Routine",
        summary="A rich yet non-occlusive routine focused on restoring and locking in moisture.",
        morning_routine=[
            "Cream or milk cleanser (no foaming agents)",
            "Hydrating toner (hyaluronic acid + glycerin)",
            "Hyaluronic acid serum (apply on damp skin)",
            "Rich moisturizer with ceramides and glycerin",
            "Sunscreen SPF 30+ (cream formula preferred)",
        ],
        night_routine=[
            "Cream cleanser or cleansing balm",
            "Hydrating essence",
            "Hyaluronic acid + peptide serum",
            "Rich barrier moisturizer (ceramides, shea butter, or squalane)",
            "Optional: facial oil (squalane or rosehip) as last step to seal",
        ],
        suggested_products=[
            "CeraVe Hydrating Cleanser",
            "The Ordinary Hyaluronic Acid 2% + B5",
            "CeraVe Moisturizing Cream",
            "Rosehip or squalane facial oil",
            "Mineral or chemical SPF 30+ in cream format",
        ],
        usage_order=[
            "Cleanser → Toner → Serum → Moisturizer → SPF (AM)",
            "Cleanser → Essence → Serum → Moisturizer → Facial oil (PM)",
        ],
        ai_notes=[
            "Apply hyaluronic acid immediately after cleansing while skin is still damp.",
            "Avoid hot water — lukewarm only.",
            "Layer from thinnest to thickest consistency.",
            "Look for ceramide NP, AP, and EOP — these are the most skin-identical lipids.",
        ],
    ),

    ("dry", "acne"): RoutineTemplate(
        title="Dry Skin with Acne — Balancing Routine",
        summary="Treats breakouts without further drying out already-parched skin.",
        morning_routine=[
            "Creamy gentle cleanser",
            "Hydrating toner (no alcohol)",
            "Niacinamide serum",
            "Lightweight ceramide moisturizer",
            "Non-comedogenic SPF 30+",
        ],
        night_routine=[
            "Cream cleanser",
            "Azelaic acid 10% serum (less drying than BHA for dry-acne skin)",
            "Ceramide moisturizer",
            "Optional: low-dose retinol (0.025%) 2× weekly — always follow with moisturizer",
        ],
        suggested_products=[
            "CeraVe Hydrating Cleanser",
            "The Ordinary Azelaic Acid 10% or Paula's Choice",
            "CeraVe PM Lotion",
            "Low-concentration retinol 0.025–0.05%",
        ],
        usage_order=[
            "Cleanser → Toner → Niacinamide → Moisturizer → SPF (AM)",
            "Cleanser → Azelaic acid → Moisturizer (nightly) + Retinol (2×/wk, last before moisturizer)",
        ],
        ai_notes=[
            "Azelaic acid is gentler than salicylic acid for dry, acne-prone skin.",
            "Always moisturize after any active to avoid barrier disruption.",
            "Avoid drying spot treatments — benzoyl peroxide is too harsh for dry skin types.",
        ],
    ),

    ("dry", "pigmentation"): RoutineTemplate(
        title="Dry Skin Brightening Routine",
        summary="Addresses dark spots and uneven tone while intensely nourishing dry skin.",
        morning_routine=[
            "Cream cleanser",
            "Vitamin C serum (stabilized forms like ascorbyl glucoside for dry skin)",
            "Rich ceramide moisturizer",
            "SPF 50+ sunscreen",
        ],
        night_routine=[
            "Cream cleanser or oil cleanser",
            "Lactic acid 5–10% (gentler AHA, hydrating effect) 2× weekly",
            "Niacinamide or tranexamic acid serum",
            "Rich barrier moisturizer",
            "Facial oil or squalane to seal",
        ],
        suggested_products=[
            "Vitamin C serum (ascorbyl glucoside or magnesium ascorbyl phosphate — more stable)",
            "The Ordinary Lactic Acid 5% + HA",
            "The Inkey List Tranexamic Acid Serum",
            "CeraVe Moisturizing Cream",
        ],
        usage_order=[
            "Cleanser → Vitamin C → Moisturizer → SPF (AM)",
            "Cleanser → AHA (2×/wk) OR Tranexamic acid → Moisturizer → Facial oil (PM)",
        ],
        ai_notes=[
            "Lactic acid is preferred over glycolic for dry skin — it also attracts moisture.",
            "SPF is the single most effective pigmentation treatment available.",
            "Tranexamic acid is very gentle and can be used nightly.",
        ],
    ),

    ("dry", "general"): RoutineTemplate(
        title="Dry Skin — Everyday Nourishing Routine",
        summary="A gentle, moisturizer-focused daily routine for dry skin.",
        morning_routine=[
            "Cream or milk cleanser",
            "Hydrating toner",
            "Moisturizer with ceramides and hyaluronic acid",
            "Sunscreen SPF 30+",
        ],
        night_routine=[
            "Cream cleanser",
            "Hyaluronic acid serum",
            "Rich moisturizer",
            "Optional: sleeping mask or facial oil as occlusive",
        ],
        suggested_products=[
            "CeraVe Hydrating Cleanser",
            "Laneige Water Sleeping Mask (as occasional occlusive)",
            "CeraVe or Vanicream moisturizer",
        ],
        usage_order=[
            "Cleanser → Toner → Moisturizer → SPF (AM)",
            "Cleanser → Serum → Moisturizer → Occlusive (PM)",
        ],
        ai_notes=[
            "Dry skin benefits most from consistent, rich moisturizers applied immediately after cleansing.",
            "Avoid foaming cleansers — they strip the protective lipid layer.",
        ],
    ),

    # ── SENSITIVE ────────────────────────────────────────────────────────────
    ("sensitive", "acne"): RoutineTemplate(
        title="Sensitive Acne-Prone Skin Routine",
        summary="Clears breakouts with minimal irritation — only the gentlest actives.",
        morning_routine=[
            "Fragrance-free cream cleanser",
            "Centella asiatica or allantoin calming toner",
            "Niacinamide 5% serum (not higher — less risk of flushing)",
            "Fragrance-free lightweight moisturizer",
            "Mineral SPF 30+ (zinc oxide based)",
        ],
        night_routine=[
            "Fragrance-free cream cleanser",
            "Azelaic acid 10% — anti-inflammatory and anti-acne, excellent for sensitive skin",
            "Fragrance-free ceramide moisturizer",
            "Optional: low-potency retinol (0.025%) once a week to start",
        ],
        suggested_products=[
            "Vanicream Gentle Cleanser",
            "The Ordinary Azelaic Acid 10%",
            "La Roche-Posay Toleriane Double Repair",
            "EltaMD UV Clear SPF 46 (zinc oxide, fragrance-free)",
        ],
        usage_order=[
            "Cleanser → Calming toner → Niacinamide → Moisturizer → Mineral SPF (AM)",
            "Cleanser → Azelaic acid → Moisturizer (nightly) + Retinol (1×/wk) (PM)",
        ],
        ai_notes=[
            "Always patch test on inner arm before full face application.",
            "Introduce one new product at a time — wait 2 weeks before adding another.",
            "Mineral sunscreens (zinc oxide) are less likely to irritate sensitive skin.",
            "Avoid fragrances, essential oils, alcohol denat, and witch hazel.",
        ],
    ),

    ("sensitive", "dryness"): RoutineTemplate(
        title="Sensitive Dry Skin — Gentle Hydration Routine",
        summary="Maximum moisture with minimum irritation risk.",
        morning_routine=[
            "Fragrance-free cream cleanser",
            "Fragrance-free hydrating toner (no alcohol)",
            "Hyaluronic acid serum",
            "Rich fragrance-free moisturizer (ceramides + glycerin)",
            "Mineral SPF 30+",
        ],
        night_routine=[
            "Fragrance-free cream cleanser or oil cleanser",
            "Soothing essence (centella, panthenol)",
            "Fragrance-free barrier repair moisturizer",
            "Optional: squalane oil to seal",
        ],
        suggested_products=[
            "Vanicream Gentle Cleanser",
            "CeraVe Moisturizing Cream",
            "The Ordinary Hyaluronic Acid 2% + B5",
            "EltaMD UV Physical SPF 41",
        ],
        usage_order=[
            "Cleanser → Toner → Serum → Moisturizer → SPF (AM)",
            "Cleanser → Essence → Moisturizer → Oil (PM)",
        ],
        ai_notes=[
            "Keep ingredient lists short — fewer ingredients = fewer potential irritants.",
            "Centella asiatica and panthenol are excellent for soothing reactive skin.",
        ],
    ),

    ("sensitive", "pigmentation"): RoutineTemplate(
        title="Sensitive Skin Brightening Routine",
        summary="Gently fades pigmentation without triggering sensitivity reactions.",
        morning_routine=[
            "Fragrance-free cream cleanser",
            "Tranexamic acid serum (very well tolerated)",
            "Fragrance-free moisturizer",
            "Mineral SPF 50+ (non-negotiable)",
        ],
        night_routine=[
            "Fragrance-free cream cleanser",
            "Mandelic acid 5% (gentlest AHA, antibacterial bonus) 2× weekly",
            "Niacinamide 5% serum",
            "Rich fragrance-free moisturizer",
        ],
        suggested_products=[
            "The Inkey List Tranexamic Acid Serum",
            "The Ordinary Mandelic Acid 10% + HA",
            "La Roche-Posay Toleriane Hydrating Gentle Cleanser",
            "Mineral SPF 50+ broad spectrum",
        ],
        usage_order=[
            "Cleanser → Tranexamic acid → Moisturizer → Mineral SPF (AM)",
            "Cleanser → Mandelic acid (2×/wk) OR Niacinamide → Moisturizer (PM)",
        ],
        ai_notes=[
            "Tranexamic acid is ideal for sensitive skin — minimal irritation, effective brightening.",
            "Mandelic acid is gentler than glycolic or lactic acid and has larger molecular size.",
            "Avoid vitamin C in L-ascorbic acid form — try more stable, gentler derivatives.",
        ],
    ),

    ("sensitive", "general"): RoutineTemplate(
        title="Sensitive Skin — Gentle Everyday Routine",
        summary="A minimal, soothing routine that maintains skin health without triggering reactions.",
        morning_routine=[
            "Fragrance-free cream cleanser",
            "Soothing calming toner (centella, allantoin, or panthenol)",
            "Fragrance-free moisturizer with ceramides",
            "Mineral SPF 30+",
        ],
        night_routine=[
            "Fragrance-free cream cleanser",
            "Barrier repair moisturizer",
        ],
        suggested_products=[
            "Vanicream Gentle Cleanser",
            "La Roche-Posay Toleriane Double Repair",
            "CeraVe PM Facial Moisturizing Lotion",
            "EltaMD UV Clear Broad-Spectrum SPF 46",
        ],
        usage_order=[
            "Cleanser → Toner → Moisturizer → Mineral SPF (AM)",
            "Cleanser → Moisturizer (PM)",
        ],
        ai_notes=[
            "Less is more for sensitive skin — 4–5 products maximum.",
            "Look for 'fragrance-free', not just 'unscented' (unscented may still contain masking fragrances).",
            "Patch test everything. Barrier repair before adding any actives.",
        ],
    ),

    # ── COMBINATION ──────────────────────────────────────────────────────────
    ("combination", "acne"): RoutineTemplate(
        title="Combination Skin Acne Routine",
        summary="Targets breakouts on the T-zone while maintaining balance in drier cheek areas.",
        morning_routine=[
            "Gentle gel cleanser",
            "Niacinamide serum (across the whole face)",
            "Lightweight moisturizer (gel for T-zone, slightly richer on cheeks)",
            "Non-comedogenic SPF 30+",
        ],
        night_routine=[
            "Gel cleanser",
            "BHA 2% (salicylic acid) on T-zone only, 3× weekly",
            "Niacinamide or azelaic acid serum",
            "Moisturizer (lighter gel on T-zone, cream on cheeks)",
        ],
        suggested_products=[
            "CeraVe Foaming Cleanser",
            "Paula's Choice BHA 2% Exfoliant",
            "The Ordinary Niacinamide 10% + Zinc 1%",
            "Lightweight gel-cream moisturizer",
        ],
        usage_order=[
            "Cleanser → Niacinamide → Moisturizer → SPF (AM)",
            "Cleanser → BHA (T-zone, 3×/wk) → Serum → Moisturizer (PM)",
        ],
        ai_notes=[
            "Multi-masking (clay mask on T-zone, hydrating mask on cheeks) works well weekly.",
            "Avoid heavy products on the T-zone.",
        ],
    ),

    ("combination", "dryness"): RoutineTemplate(
        title="Combination Skin — Targeted Hydration",
        summary="Hydrates dry patches without making the T-zone oilier.",
        morning_routine=[
            "Gentle gel cleanser",
            "Hyaluronic acid serum (all over)",
            "Gel moisturizer on T-zone, cream moisturizer on cheeks",
            "Non-comedogenic SPF 30+",
        ],
        night_routine=[
            "Gentle gel cleanser",
            "Hyaluronic acid or hydrating essence",
            "Lightweight gel moisturizer on T-zone, heavier cream on cheeks",
        ],
        suggested_products=[
            "CeraVe Hydrating Cleanser",
            "The Ordinary Hyaluronic Acid 2% + B5",
            "Neutrogena Hydro Boost (for T-zone) + CeraVe Cream (for cheeks)",
        ],
        usage_order=[
            "Cleanser → Serum → Zone-specific moisturizer → SPF (AM)",
            "Cleanser → Serum → Zone-specific moisturizer (PM)",
        ],
        ai_notes=[
            "You can use two different moisturizers — one for each zone.",
            "Hyaluronic acid is suitable for the whole face.",
        ],
    ),

    ("combination", "pigmentation"): RoutineTemplate(
        title="Combination Skin Brightening Routine",
        summary="Evens out skin tone while balancing the T-zone.",
        morning_routine=[
            "Gentle gel cleanser",
            "Vitamin C serum",
            "Lightweight moisturizer",
            "SPF 50+",
        ],
        night_routine=[
            "Gel cleanser",
            "AHA exfoliant (glycolic 5%) on dark spots, 2–3× weekly",
            "Niacinamide or tranexamic acid serum",
            "Zone-appropriate moisturizer",
        ],
        suggested_products=[
            "Vitamin C serum 10–15%",
            "The Ordinary Glycolic Acid 7%",
            "The Ordinary Niacinamide 10% + Zinc",
            "SPF 50+ non-comedogenic",
        ],
        usage_order=[
            "Cleanser → Vitamin C → Moisturizer → SPF (AM)",
            "Cleanser → AHA (3×/wk) → Niacinamide → Moisturizer (PM)",
        ],
        ai_notes=[
            "Do not use vitamin C and AHA at the same time.",
            "Daily SPF is non-negotiable when targeting pigmentation.",
        ],
    ),

    ("combination", "general"): RoutineTemplate(
        title="Combination Skin — Balanced Everyday Routine",
        summary="A simple balanced routine for combination skin with no specific concern.",
        morning_routine=[
            "Gentle gel cleanser",
            "Lightweight serum (hyaluronic acid or niacinamide)",
            "Gel moisturizer or gel-cream",
            "SPF 30+",
        ],
        night_routine=[
            "Gel cleanser",
            "Optional serum",
            "Zone-balanced moisturizer",
        ],
        suggested_products=[
            "CeraVe Foaming Cleanser",
            "Niacinamide serum",
            "Neutrogena Hydro Boost",
        ],
        usage_order=[
            "Cleanser → Serum → Moisturizer → SPF (AM)",
            "Cleanser → Serum → Moisturizer (PM)",
        ],
        ai_notes=[
            "Combination skin benefits from consistent, simple routines.",
        ],
    ),
}

# Fallback templates per concern (any skin type)
FALLBACK_BY_CONCERN: Dict[str, RoutineTemplate] = {
    "acne": ROUTINE_TEMPLATES[("oily", "acne")],
    "dryness": ROUTINE_TEMPLATES[("dry", "dryness")],
    "pigmentation": ROUTINE_TEMPLATES[("combination", "pigmentation")],
    "general": ROUTINE_TEMPLATES[("combination", "general")],
    "anti_aging": RoutineTemplate(
        title="Anti-Aging Routine",
        summary="A science-backed routine targeting fine lines, wrinkles, and loss of firmness.",
        morning_routine=[
            "Gentle cream cleanser",
            "Vitamin C serum (L-ascorbic acid 10–15%)",
            "Peptide eye cream",
            "Rich moisturizer with peptides and hyaluronic acid",
            "SPF 50+ broad-spectrum (critical for anti-aging)",
        ],
        night_routine=[
            "Gentle cream cleanser",
            "Retinol 0.025–0.05% (start 2× weekly, increase gradually)",
            "Peptide serum",
            "Rich moisturizer with ceramides",
        ],
        suggested_products=[
            "SkinCeuticals CE Ferulic or budget vitamin C serum",
            "The Ordinary Granactive Retinoid 2% Emulsion (gentler start)",
            "Olay Regenerist Micro-Sculpting Cream",
            "SPF 50+ broad-spectrum daily sunscreen",
        ],
        usage_order=[
            "Cleanser → Vitamin C → Eye cream → Moisturizer → SPF 50+ (AM)",
            "Cleanser → Retinol (2–3×/wk) → Peptide serum → Moisturizer (PM)",
        ],
        ai_notes=[
            "Retinol is the gold standard for anti-aging — be patient, results take 12+ weeks.",
            "SPF is the single most effective anti-aging product available.",
            "Introduce retinol very gradually to avoid the retinol purge.",
            "Peptides and retinol can be layered safely.",
        ],
    ),
}


def get_routine(skin_type: str, concern: str) -> RoutineTemplate:
    """Return the best matching routine template."""
    key = (skin_type.lower(), concern.lower())
    if key in ROUTINE_TEMPLATES:
        return ROUTINE_TEMPLATES[key]
    # fallback: try by concern only
    if concern.lower() in FALLBACK_BY_CONCERN:
        return FALLBACK_BY_CONCERN[concern.lower()]
    # final fallback
    return FALLBACK_BY_CONCERN["general"]
