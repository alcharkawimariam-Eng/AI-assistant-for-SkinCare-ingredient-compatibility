from typing import Any, Dict, Optional
from urllib.parse import quote
import re

import requests
from bs4 import BeautifulSoup
from .ingredient_parser import extract_interaction_relevant_ingredients

class IncidecoderSearch:
    def search(self, query: str) -> Optional[Dict[str, Any]]:
        search_url = f"https://incidecoder.com/search?query={quote(query)}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        product_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(" ", strip=True)

            if href.startswith("/products/") and text:
                product_links.append({
                    "title": text,
                    "url": "https://incidecoder.com" + href
                })

        seen = set()
        unique_links = []
        for item in product_links:
            if item["url"] not in seen:
                seen.add(item["url"])
                unique_links.append(item)

        if not unique_links:
            return None

        top_result = unique_links[0]

        ingredients_data = self._extract_product_ingredients(top_result["url"])

        return {
            "found": True,
            "source": "incidecoder",
            "match_type": "external_search",
            "product_id": None,
            "brand": None,
            "product_name": top_result["title"],
            "category": None,
            "ingredients": ingredients_data["ingredients"],
            "active_ingredients": ingredients_data["active_ingredients"],
            "interaction_relevant_ingredients": extract_interaction_relevant_ingredients(
                ingredients_data["ingredients"]
            ),
            "source_url": top_result["url"],
}

    def _extract_product_ingredients(self, product_url: str) -> Dict[str, Optional[str]]:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(product_url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception:
            return {
                "ingredients": None,
                "active_ingredients": None,
            }

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text("\n", strip=True)
        print(page_text[:3000])
        active_text = self._extract_section(
        page_text,
        start_label="Active Ingredients",
        end_labels=["Inactive Ingredients", "Read more on", "Compare", "Report Error", "Embed"]
                                            )

        inactive_text = self._extract_section(
        page_text,
        start_label="Inactive Ingredients",
        end_labels=["Read more on", "Compare", "Report Error", "Embed", "Highlights", "Key Ingredients"]
                                        )

        full_ingredients = None
        if active_text and inactive_text:
            full_ingredients = f"Active Ingredients: {active_text} | Inactive Ingredients: {inactive_text}"
        elif inactive_text:
            full_ingredients = inactive_text
        elif active_text:
            full_ingredients = active_text

        return {
            "ingredients": self._clean_text(full_ingredients),
            "active_ingredients": self._clean_text(active_text),
        }

    def _extract_section(self, text: str, start_label: str, end_labels: list[str]) -> Optional[str]:
        start_idx = text.find(start_label)
        if start_idx == -1:
            return None

        start_idx += len(start_label)
        remaining = text[start_idx:]

        end_positions = []
        for label in end_labels:
            pos = remaining.find(label)
            if pos != -1:
                end_positions.append(pos)

        if end_positions:
            section = remaining[:min(end_positions)]
        else:
            section = remaining

        return section.strip()

    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        if not text:
            return None

        text = text.replace("[more]", "")
        text = text.replace("[less]", "")
        text = text.replace("​", "")

        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\s+,\s*", ", ", text)
        text = re.sub(r"\s+:\s*", ": ", text)
        text = re.sub(r":\s*:", ": ", text)

        if text.startswith(": "):
            text = text[2:]

        return text.strip()