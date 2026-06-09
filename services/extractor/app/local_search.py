from __future__ import annotations

from pathlib import Path
from difflib import get_close_matches
from typing import Any, Dict, List, Optional

import pandas as pd

from .ingredient_parser import extract_interaction_relevant_ingredients


class LocalProductSearch:
    def __init__(self, csv_path: str | Path):
        self.csv_path = Path(csv_path)
        self.df = self._load_dataset()

    def _load_dataset(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.csv_path}")

        df = pd.read_csv(self.csv_path, encoding="latin1")

        required_columns = ["product_name", "full_ingredients_text"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in dataset: {missing_columns}")

        for col in [
            "product_id",
            "brand",
            "category",
            "source_url",
            "active_ingredients",
            "official_active_ingredients",
            "key_ingredients",
        ]:
            if col not in df.columns:
                df[col] = None

        df["product_name"] = df["product_name"].fillna("").astype(str)
        df["brand"] = df["brand"].fillna("").astype(str)
        df["full_ingredients_text"] = df["full_ingredients_text"].fillna("").astype(str)
        df["active_ingredients"] = df["active_ingredients"].fillna("").astype(str)

        df["product_name_normalized"] = df["product_name"].apply(self._normalize_text)
        df["brand_normalized"] = df["brand"].apply(self._normalize_text)

        return df

    @staticmethod
    def _normalize_text(text: str) -> str:
        return (
            str(text)
            .lower()
            .strip()
            .replace("-", " ")
            .replace("_", " ")
        )

    def search_exact(self, query: str) -> Optional[Dict[str, Any]]:
        query_norm = self._normalize_text(query)
        matches = self.df[self.df["product_name_normalized"] == query_norm]

        if matches.empty:
            return None

        return self._row_to_result(matches.iloc[0], "exact")

    def search_fuzzy(self, query: str, cutoff: float = 0.80) -> Optional[Dict[str, Any]]:
        query_norm = self._normalize_text(query)

        product_names: List[str] = (
            self.df["product_name_normalized"].dropna().unique().tolist()
        )

        close_matches = get_close_matches(query_norm, product_names, n=1, cutoff=cutoff)
        if not close_matches:
            return None

        matched_name = close_matches[0]
        row = self.df[self.df["product_name_normalized"] == matched_name].iloc[0]
        return self._row_to_result(row, "fuzzy")

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        result = self.search_exact(query)
        if result:
            return result

        result = self.search_fuzzy(query)
        if result:
            return result

        return None

    @staticmethod
    def _row_to_result(row: pd.Series, match_type: str) -> Dict[str, Any]:
        ingredients = row.get("full_ingredients_text")
        active_ingredients = row.get("active_ingredients")

        base_text_parts = []

        if active_ingredients is not None and not pd.isna(active_ingredients) and str(active_ingredients).strip():
            base_text_parts.append(str(active_ingredients))

        if ingredients is not None and not pd.isna(ingredients) and str(ingredients).strip():
            base_text_parts.append(str(ingredients))

        base_text = " ".join(base_text_parts)
        interaction_value = extract_interaction_relevant_ingredients(base_text)

        key_ingredients = row.get("key_ingredients")
        if pd.isna(key_ingredients):
            key_ingredients = None

        official_active_ingredients = row.get("official_active_ingredients")
        if pd.isna(official_active_ingredients):
            official_active_ingredients = None

        return {
            "found": True,
            "source": "local_dataset",
            "match_type": match_type,
            "product_id": row.get("product_id"),
            "brand": row.get("brand"),
            "product_name": row.get("product_name"),
            "category": row.get("category"),
            "full_ingredients_text": row.get("full_ingredients_text"),
            "active_ingredients": row.get("active_ingredients"),
            "official_active_ingredients": official_active_ingredients,
            "key_ingredients": key_ingredients,
            "interaction_relevant_ingredients": interaction_value,
            "source_url": row.get("source_url"),
        }