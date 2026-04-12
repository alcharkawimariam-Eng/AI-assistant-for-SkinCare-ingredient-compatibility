from typing import List


INTERACTION_KEYWORDS = [
    "retinol",
    "retinal",
    "tretinoin",
    "adapalene",
    "benzoyl peroxide",
    "salicylic acid",
    "glycolic acid",
    "lactic acid",
    "mandelic acid",
    "azelaic acid",
    "ascorbic acid",
    "vitamin c",
    "hydroquinone",
    "kojic acid",
    "avobenzone",
    "homosalate",
    "octisalate",
    "octocrylene",
    "urea",
    "ceramide",
]


def extract_interaction_relevant_ingredients(ingredients_text: str | None) -> List[str]:
    if not ingredients_text:
        return []

    text_lower = ingredients_text.lower()
    found = []

    for keyword in INTERACTION_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)

    return found