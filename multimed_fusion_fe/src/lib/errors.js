export function normalizeApiError(error, fallback = "Something went wrong.") {
  const data = error?.response?.data;

  if (!data) {
    return fallback;
  }
  if (typeof data === "string") {
    return data;
  }
  if (Array.isArray(data)) {
    return data.join(", ");
  }
  if (typeof data === "object") {
    if (data.detail) {
      return String(data.detail);
    }

    return Object.entries(data)
      .map(([key, value]) => {
        if (Array.isArray(value)) {
          return `${key}: ${value.join(", ")}`;
        }
        if (typeof value === "object" && value !== null) {
          return `${key}: ${JSON.stringify(value)}`;
        }
        return `${key}: ${String(value)}`;
      })
      .join(" | ");
  }

  return fallback;
}
