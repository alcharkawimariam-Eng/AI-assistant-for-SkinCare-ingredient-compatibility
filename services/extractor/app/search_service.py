from pathlib import Path
from typing import Any, Dict, List

from .incidecoder_search import IncidecoderSearch
from .local_search import LocalProductSearch


class SearchService:
    def __init__(self):
        dataset_path = Path(__file__).resolve().parents[3] / "data" / "main_skincare_dataset.csv"
        self.local_search = LocalProductSearch(dataset_path)
        self.incidecoder_search = IncidecoderSearch()

    def search_products(self, products: List[str]) -> Dict[str, Any]:
        found_products = []
        unknown_products = []

        for product in products:
            result = self.local_search.search(product)

            if not result:
                result = self.incidecoder_search.search(product)

            if result:
                found_products.append(result)
            else:
                unknown_products.append(product)

        return {
            "found_products": found_products,
            "unknown_products": unknown_products,
            "message": "Search completed."
        }