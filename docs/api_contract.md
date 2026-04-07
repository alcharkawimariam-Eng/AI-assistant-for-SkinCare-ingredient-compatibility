# API Contract

## POST /scan
Input:
- products: list[str]
- skin_type: optional
- sensitivity: optional

Output:
- decision
- normalized ingredients
- risk_level
- explanations
