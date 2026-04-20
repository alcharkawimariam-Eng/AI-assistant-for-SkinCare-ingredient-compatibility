# API Contract

## Overview

This document defines the agreed JSON contracts between all parts of the system so the team can work in parallel without blocking each other.

### Team ownership

- **Frontend**: Jumana
- **External Endpoint (EEP) + Internal Endpoint 1 (Extractor/Search)**: Mariam
- **Internal Endpoint 2 (Analyzer/Compatibility)**: Julia

---

## System flow

```text
Frontend
  -> External Endpoint (EEP)
  -> Internal Endpoint 1: Extractor/Search
  -> Internal Endpoint 2: Analyzer/Compatibility
  -> External Endpoint (EEP)
  -> Frontend
```

---

## 1. Frontend -> External Endpoint

This request is sent from the frontend to the public API.

### Purpose
The user can submit product names and, if needed, manual ingredient text.

### Request body

```json
{
  "products": [
    {
      "id": "p1",
      "name": "Eucerin Complete Repair Moisturizing Lotion",
      "ingredients_text": null
    },
    {
      "id": "p2",
      "name": "La Roche-Posay ANTHELIOS SUNSCREEN FOR KIDS SPF 60",
      "ingredients_text": null
    }
  ]
}
```

### Field definitions

- `id`: frontend-side identifier for the product entry
- `name`: product name entered by the user
- `ingredients_text`: manually entered ingredients text if product search is not used

### Rules

- At least one of `name` or `ingredients_text` must be provided for each product
- `id` must be unique inside the request
- Maximum number of products per request: `6`

---

## 2. External Endpoint -> Internal Endpoint 1

Since the External Endpoint and Internal Endpoint 1 are currently owned by the same person, the same structure can be reused internally.

### Request body

```json
{
  "products": [
    {
      "id": "p1",
      "name": "Eucerin Complete Repair Moisturizing Lotion",
      "ingredients_text": null
    },
    {
      "id": "p2",
      "name": "La Roche-Posay ANTHELIOS SUNSCREEN FOR KIDS SPF 60",
      "ingredients_text": null
    }
  ]
}
```

### Responsibility of Internal Endpoint 1

Internal Endpoint 1 is responsible for:

- searching the local dataset first
- if not found, searching the external source
- if needed later, handling manual ingredients and OCR fallback
- extracting the raw ingredient information
- identifying interaction-relevant ingredients
- returning normalized product objects

---

## 3. Internal Endpoint 1 -> Internal Endpoint 2

This is the normalized output produced by the extractor/search service and sent to the analyzer/compatibility service.

### Response body from Internal Endpoint 1
### Request body to Internal Endpoint 2

```json
{
  "products": [
    {
      "id": "p1",
      "name": "Eucerin Complete Repair Moisturizing Lotion",
      "found": true,
      "full_ingredients_text": "Water, Glycerin, Urea, Cetearyl Alcohol, Glyceryl Glucoside, Cyclomethicone, Sodium Lactate, Butyrospermum Parkii (Shea) Butter, ...",
      "interaction_relevant_ingredients": ["lactic acid", "urea", "ceramide"]
    },
    {
      "id": "p2",
      "name": "La Roche-Posay ANTHELIOS SUNSCREEN FOR KIDS SPF 60",
      "found": true,
      "full_ingredients_text": "Active Ingredients: Avobenzone (3%), Homosalate (10%), Octisalate (5%), Octocrylene (7%) | Inactive Ingredients: Water, ...",
      "interaction_relevant_ingredients": ["avobenzone", "homosalate", "octisalate", "octocrylene"]
    }
  ],
  "unknown_products": []
}
```

### Field definitions

- `id`: product identifier coming from the frontend
- `name`: product name
- `found`: whether the product was found and successfully processed
- `full_ingredients_text`: raw ingredient text extracted from the data source
- `interaction_relevant_ingredients`: the important ingredients used for compatibility logic
- `unknown_products`: list of product names that could not be found

### Notes

- This structure should stay minimal
- Internal Endpoint 2 should rely mainly on `interaction_relevant_ingredients`
- `full_ingredients_text` is included for traceability and future use

---

## 4. Internal Endpoint 2 -> External Endpoint

This is the response sent back by the analyzer/compatibility service.

### Response body

```json
{
  "compatible": true,
  "risk_level": "medium",
  "summary": "These products can be used together with caution.",
  "issues": [
    {
      "product_ids": ["p1", "p2"],
      "ingredients": ["lactic acid", "octocrylene"],
      "message": "Possible irritation or sensitivity depending on routine."
    }
  ],
  "recommendations": [
    "Patch test first.",
    "Avoid layering too many strong actives at the same time."
  ]
}
```

### Field definitions

- `compatible`: overall boolean result
- `risk_level`: expected values such as `low`, `medium`, or `high`
- `summary`: short explanation of the overall result
- `issues`: detailed compatibility issues
- `recommendations`: practical suggestions for the user

### Issue object

Each item inside `issues` contains:

- `product_ids`: the products involved in the issue
- `ingredients`: the ingredients causing the issue
- `message`: human-readable explanation

---

## 5. External Endpoint -> Frontend

This is the final response returned to the frontend.

### Response body

```json
{
  "products": [
    {
      "id": "p1",
      "name": "Eucerin Complete Repair Moisturizing Lotion",
      "found": true,
      "full_ingredients_text": "Water, Glycerin, Urea, Cetearyl Alcohol, Glyceryl Glucoside, Cyclomethicone, Sodium Lactate, ...",
      "interaction_relevant_ingredients": ["lactic acid", "urea", "ceramide"]
    },
    {
      "id": "p2",
      "name": "La Roche-Posay ANTHELIOS SUNSCREEN FOR KIDS SPF 60",
      "found": true,
      "full_ingredients_text": "Active Ingredients: Avobenzone (3%), Homosalate (10%), Octisalate (5%), Octocrylene (7%) | Inactive Ingredients: Water, ...",
      "interaction_relevant_ingredients": ["avobenzone", "homosalate", "octisalate", "octocrylene"]
    }
  ],
  "analysis": {
    "compatible": true,
    "risk_level": "medium",
    "summary": "These products can be used together with caution.",
    "issues": [
      {
        "product_ids": ["p1", "p2"],
        "ingredients": ["lactic acid", "octocrylene"],
        "message": "Possible irritation or sensitivity depending on routine."
      }
    ],
    "recommendations": [
      "Patch test first.",
      "Avoid layering too many strong actives at the same time."
    ]
  },
  "unknown_products": []
}
```

### Purpose

This response is designed for frontend display. It intentionally excludes unnecessary technical fields.

---

## 6. Unknown product behavior

If a product cannot be found by Internal Endpoint 1, it should not break the flow.

### Example

```json
{
  "products": [
    {
      "id": "p1",
      "name": "Known Product",
      "found": true,
      "full_ingredients_text": "Water, Glycerin, ...",
      "interaction_relevant_ingredients": ["salicylic acid"]
    },
    {
      "id": "p2",
      "name": "Unknown Product",
      "found": false,
      "full_ingredients_text": null,
      "interaction_relevant_ingredients": []
    }
  ],
  "unknown_products": ["Unknown Product"]
}
```

### Rule

- A product that is not found should remain in the response with `found: false`
- It should also appear in `unknown_products`

---

## 7. Contract stability rules

To avoid breaking parallel work:

- Do not rename fields without agreement from all team members
- Do not add unnecessary fields unless they are really needed
- Keep the contract minimal and stable
- If a new field is required later, discuss it before changing the structure

---

## 8. Final agreed minimal fields

### Frontend input
- `id`
- `name`
- `ingredients_text`

### Extractor output
- `id`
- `name`
- `found`
- `full_ingredients_text`
- `interaction_relevant_ingredients`

### Analyzer output
- `compatible`
- `risk_level`
- `summary`
- `issues`
- `recommendations`

### Final response to frontend
- `products`
- `analysis`
- `unknown_products`

---

## 9. Current implementation direction

- Internal Endpoint 1 currently supports local dataset search and external fallback
- Internal Endpoint 2 will perform compatibility analysis using interaction-relevant ingredients
- Frontend will consume the final EEP response and display results to the user

This contract should be used as the shared reference