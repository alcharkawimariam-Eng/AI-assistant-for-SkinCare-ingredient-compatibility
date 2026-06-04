# Positioning and Novelty

## Problem Statement

Skincare and haircare routines are becoming more complex as users combine multiple products with active ingredients such as retinoids, acids, vitamin C, benzoyl peroxide, peptides, sulfates, silicones, and protein-based treatments. While each product may be safe when used alone, problems often appear when products are layered together without considering ingredient interactions, user sensitivity, routine frequency, or hair/skin context. For example, a user may combine retinol with exfoliating acids, use several high-protein hair products in the same routine, or apply fragrance-heavy products on sensitive skin. These combinations can increase irritation, dryness, breakouts, barrier damage, color fading, buildup, or brittleness.

The problem is not simply identifying whether one ingredient is “good” or “bad.” The real challenge is analyzing a messy routine made of multiple product names or ingredient lists, extracting the relevant active ingredients, detecting cumulative risk across products, and adjusting the result based on the user profile. Most users do not have the time or scientific background to manually inspect every ingredient list and reason about pairwise or cumulative interactions. Our system addresses this gap by providing an AI-assisted ingredient compatibility checker for skincare and haircare routines.

## Non-AI Baseline

A reasonable non-AI baseline is manual lookup. A user can search each product or ingredient using online resources such as INCIDecoder, brand websites, ingredient dictionaries, dermatology blogs, or product reviews. The user can then manually compare ingredient descriptions and try to decide whether the products are compatible. Another baseline is a simple pairwise rule checklist: for example, checking whether retinol appears with benzoyl peroxide, or whether glycolic acid appears with salicylic acid.

This baseline is useful for isolated cases. If a user only wants to know what one ingredient does, manual lookup can be enough. It can also help when the exact product exists in a public database and the ingredient list is clearly available. However, this approach does not scale well to real routines. A typical routine may include cleansers, toners, serums, moisturizers, sunscreens, shampoos, conditioners, masks, and treatments. Each product can contain many ingredients, and the user may not know which ones matter for interaction risk.

## Why the Baseline Fails

The manual baseline fails in four main ways.

First, it does not handle cumulative risk well. Many tools explain ingredients one by one, but they do not always reason about the full routine. Two products may each be acceptable alone, but together they may increase irritation or over-exfoliation risk. Similarly, repeated use of the same category, such as multiple retinoids, multiple BHAs, or multiple protein hair treatments, can create stacking risk that is not obvious from single-product lookup.

Second, the baseline is not personalized. A combination that is acceptable for normal or resilient skin may be risky for sensitive skin. A fragrance-containing product may not be a problem for every user, but it can become more concerning for a high-sensitivity profile. Haircare also depends on context: sulfates may be more problematic for color-treated hair, while heavy silicones may be more concerning for curly hair if the routine does not include clarifying.

Third, manual lookup assumes clean input. Real users often enter partial product names, misspellings, incomplete ingredient lists, screenshots, or vague descriptions. A strict lookup system may fail if the product name does not exactly match a known database entry. This creates friction and reduces reliability.

Fourth, the baseline does not provide a structured engineering pipeline. It may give useful information, but it does not produce consistent risk levels, reasons, fallback behavior, or monitoring outputs that can be tested and evaluated. For a software engineering project, we need a system that is explainable, testable, and robust enough to handle uncertainty.

## How Our System Is Different

Our system improves on the baseline by combining extraction, analysis, personalization, and explainability in a modular pipeline.

The extractor is designed as a four-tier system. The first tier uses local CSV data for fast known-product or known-ingredient lookup. The second tier can use INCIDecoder-style search or scraping for broader product coverage. The third tier supports OCR-style handling for messy inputs such as screenshots or product labels. The fourth tier uses an LLM fallback when deterministic methods are insufficient. This hybrid approach avoids relying on a language model for every request, while still supporting messy real-world input.

The analyzer and risk engine are role-aware. Instead of treating all ingredients equally, it focuses on interaction-relevant ingredients and applies rules based on their role in a routine. For example, it can identify conflicts such as retinol with benzoyl peroxide, AHA with BHA, or fragrance with sensitive actives. It can also detect stacking situations, such as duplicate retinoids, repeated exfoliating acids, or repeated hair protein treatments. This makes the system more useful than a simple ingredient dictionary.

The personalizer adjusts risk interpretation using profile information such as skin type, sensitivity, age group, and concerns. This is important because compatibility is not universal. A strong active may be acceptable for one user but risky for another. By including personalization, the system moves beyond generic ingredient lookup and toward context-aware recommendations.

The system is also explainable. Instead of returning only a label, it returns a risk level, score, and reasons. This allows the user to understand why a combination was flagged. Explainability is especially important for a safety-oriented application because users should not blindly trust a black-box result.

Finally, the project is structured as microservices: a gateway, extractor, risk engine/analyzer, and personalizer. This makes the system easier to test, monitor, and extend. It also supports future observability through Prometheus, Grafana, and MLflow. The architecture therefore supports both the product goal and the engineering rubric.

## Target Users

The primary target users are skincare and haircare consumers who use multiple products and want to avoid harmful combinations. This includes users with sensitive skin, acne-prone skin, anti-aging routines, color-treated hair, curly hair, or damaged hair. These users often combine products from different brands and may not know whether the routine is safe.

A second target group is beauty advisors, pharmacists, or content creators who want a quick compatibility check before recommending routines. The system can help them identify obvious conflicts and explain the reasoning clearly.

A third target group is beginner users who are overwhelmed by ingredient lists. For them, the system acts as a guided assistant that translates technical ingredient information into understandable risk warnings.

## Novelty Claim

The novelty of our system is not that it “knows ingredients.” Existing tools already provide ingredient descriptions. Our novelty is the combination of messy input handling, multi-tier extraction, role-aware interaction analysis, cumulative risk detection, personalization, and explainable safety-focused output in one workflow. Compared with manual lookup or simple pairwise checks, our system is more practical for real routines because it considers the routine as a whole, handles uncertain inputs, and adapts the result to the user profile.
