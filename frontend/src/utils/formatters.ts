export function formatCurrency(value: string | number) {
  const numeric = typeof value === "string" ? Number(value) : value;
  if (Number.isNaN(numeric)) {
    return String(value);
  }
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 }).format(numeric);
}

export function formatDate(value?: string | null) {
  if (!value) {
    return "—";
  }
  return new Date(value).toLocaleDateString("en-IN");
}
