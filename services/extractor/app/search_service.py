import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from .incidecoder_search import IncidecoderSearch
from .local_search import LocalProductSearch
from .ingredient_parser import extract_interaction_relevant_ingredients
from .llm_search import extract_with_llm, is_llm_available

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self):
        dataset_path_env = os.getenv("DATASET_PATH")
        if dataset_path_env:
            dataset_path = Path(dataset_path_env)
        else:
            dataset_path = Path(__file__).resolve().parents[3] / "data" / "main_skincare_dataset.csv"

        self.local_search = LocalProductSearch(dataset_path)
        self.incidecoder_search = IncidecoderSearch()

    def search_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        normalized_products = []
        unknown_products = []

        for product in products:
            product_id = product.get("id")
            product_name = product.get("name")
            ingredients_text = product.get("ingredients_text")

            result = None
            full_ingredients_text = None

            # Case 1: manual ingredients text provided directly
            if ingredients_text and str(ingredients_text).strip():
                full_ingredients_text = ingredients_text
                result = {
                    "name": product_name,
                    "full_ingredients_text": full_ingredients_text,
                }

            # Case 2: search by product name
            elif product_name and str(product_name).strip():
                result = self.local_search.search(product_name)

                if not result:
                    result = self.incidecoder_search.search(product_name)

                # Tier 4 — LLM fallback: only if local + Incidecoder both failed
                # and a product name is available (not ingredients_text path)
                if not result and is_llm_available():
                    try:
                        llm_result = extract_with_llm(product_name)
                        if llm_result and not llm_result.rejected and llm_result.ingredients:
                            # Convert LLM ingredient list to the same dict shape
                            # that local/incidecoder return (comma-joined text)
                            full_ingredients_text = ", ".join(llm_result.ingredients)
                            result = {
                                "name": product_name,
                                "full_ingredients_text": full_ingredients_text,
                                "_source": "llm",
                            }
                            logger.info(
                                f"LLM fallback succeeded for '{product_name}' "
                                f"(confidence={llm_result.confidence:.2f})"
                            )
                        elif llm_result:
                            logger.info(
                                f"LLM fallback rejected for '{product_name}': "
                                f"{llm_result.reject_reason}"
                            )
                    except Exception as e:
                        logger.warning(f"LLM fallback error for '{product_name}': {e}")

                if result:
                    full_ingredients_text = result.get("full_ingredients_text") or result.get("ingredients_text")

            # Build normalized contract response
            if result and full_ingredients_text:
                interaction_relevant_ingredients = extract_interaction_relevant_ingredients(full_ingredients_text)

                normalized_products.append({
                    "id": product_id,
                    "name": product_name,
                    "found": True,
                    "full_ingredients_text": full_ingredients_text,
                    "interaction_relevant_ingredients": interaction_relevant_ingredients,
                })
            else:
                normalized_products.append({
                    "id": product_id,
                    "name": product_name,
                    "found": False,
                    "full_ingredients_text": None,
                    "interaction_relevant_ingredients": [],
                })

                if product_name:
                    unknown_products.append(product_name)

        return {
            "products": normalized_products,
            "unknown_products": unknown_products,
        }