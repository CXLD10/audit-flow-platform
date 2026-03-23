import re
from decimal import Decimal

from rapidfuzz import process
from rapidfuzz.fuzz import WRatio

from app.repositories.entity_mapping_repo import EntityMappingRepository

ABBREVIATIONS = {r"\bltd\b": "limited", r"\bpvt\b": "private", r"\bind\.?\b": "industries"}


class EntityResolver:
    def __init__(self, db, tenant_id, batch_id):
        self.db = db
        self.repo = EntityMappingRepository(db=db, tenant_id=tenant_id)
        self.batch_id = batch_id

    def normalize_name(self, name: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9\s]", " ", name.lower()).strip()
        for pattern, replacement in ABBREVIATIONS.items():
            value = re.sub(pattern, replacement, value)
        return re.sub(r"\s+", " ", value).strip()

    def resolve(self, invoices: list):
        names = [invoice.supplier_name for invoice in invoices if invoice.supplier_name]
        unresolved: dict[str, str] = {}
        for raw_name in names:
            existing = self.repo.get_by_raw_name(raw_name)
            if existing:
                unresolved[raw_name] = existing.canonical_name
            else:
                unresolved[raw_name] = self.normalize_name(raw_name)
        normalized_names = list(dict.fromkeys(unresolved.values()))
        deduped = process.dedupe(normalized_names, scorer=WRatio, threshold=85)
        canonical_by_normalized = {name: name for name in normalized_names}
        for cluster in deduped:
            choices = list(cluster)
            canonical = max(choices, key=len)
            for item in choices:
                canonical_by_normalized[item] = canonical
        for raw_name, normalized in unresolved.items():
            canonical = canonical_by_normalized.get(normalized, normalized)
            existing = self.repo.get_by_raw_name(raw_name)
            if existing is None:
                self.repo.create(
                    raw_name=raw_name,
                    canonical_name=canonical,
                    similarity_score=Decimal("100.00") if canonical == normalized else Decimal("85.00"),
                    source_batch_id=self.batch_id,
                    user_overridden=False,
                )
        for invoice in invoices:
            if invoice.supplier_name:
                mapping = self.repo.get_by_raw_name(invoice.supplier_name)
                invoice.canonical_supplier_name = mapping.canonical_name if mapping else invoice.supplier_name
        return invoices
