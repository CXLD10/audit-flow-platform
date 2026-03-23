from collections.abc import Iterable

MANDATORY_FIELDS = {
    "invoice_number",
    "invoice_date",
    "supplier_gstin",
    "recipient_gstin",
    "hsn_sac_code",
    "taxable_value",
    "cgst_amount",
    "sgst_amount",
    "igst_amount",
    "total_invoice_value",
    "place_of_supply",
}

DEFAULT_COLUMN_ALIASES = {
    "invoice no": "invoice_number",
    "invoice_number": "invoice_number",
    "invoice date": "invoice_date",
    "invoice_date": "invoice_date",
    "supplier gstin": "supplier_gstin",
    "vendor gstin": "supplier_gstin",
    "recipient gstin": "recipient_gstin",
    "hsn": "hsn_sac_code",
    "hsn/sac": "hsn_sac_code",
    "taxable value": "taxable_value",
    "cgst": "cgst_amount",
    "sgst": "sgst_amount",
    "igst": "igst_amount",
    "total invoice value": "total_invoice_value",
    "total": "total_invoice_value",
    "place of supply": "place_of_supply",
    "supplier name": "supplier_name",
    "tax rate": "applicable_rate",
    "credit note flag": "credit_note_flag",
}


class ColumnMapper:
    def __init__(self, tenant_mapping: dict[str, str] | None = None):
        self.tenant_mapping = {self._normalize_key(k): v for k, v in (tenant_mapping or {}).items()}

    @staticmethod
    def _normalize_key(value: str) -> str:
        return value.strip().lower().replace("_", " ")

    def detect_header(self, rows: Iterable[list[object]]) -> int:
        for idx, row in enumerate(rows):
            normalized = {self._normalize_key(str(cell)) for cell in row if str(cell).strip()}
            if normalized & set(DEFAULT_COLUMN_ALIASES):
                return idx
        return 0

    def map_columns(self, columns: list[str]) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for column in columns:
            key = self._normalize_key(column)
            if key in self.tenant_mapping:
                mapping[column] = self.tenant_mapping[key]
            elif key in DEFAULT_COLUMN_ALIASES:
                mapping[column] = DEFAULT_COLUMN_ALIASES[key]
        return mapping

    def validate_mandatory_fields(self, mapped_columns: dict[str, str]) -> list[str]:
        present = set(mapped_columns.values())
        return sorted(MANDATORY_FIELDS - present)
