from pathlib import Path
from typing import Any, Dict, List

from .incidecoder_search import IncidecoderSearch
from .local_search import LocalProductSearch
from .ingredient_parser import extract_interaction_relevant_ingredients


class SearchService:
    def __init__(self):
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