const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function scanProducts(payload) {
  const response = await fetch(`${API_BASE_URL}/scan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return response.json();
}

export function buildScanPayload({
  products,
  skinType,
  sensitivity,
  age,
  concerns,
}) {
  return {
    products: products
      .filter((product) => product.name.trim() !== "")
      .map((product) => product.name.trim()),

    skin_type: skinType || null,
    sensitivity: sensitivity || null,
    age: age || null,
    concerns: concerns || [],

    profile: {
      skin_type: skinType || null,
      sensitivity: sensitivity || null,
      age: age || null,
      concerns: concerns || [],
    },
  };
}