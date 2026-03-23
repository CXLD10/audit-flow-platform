from collections.abc import Iterator
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import InvoiceState
from app.models.invoice import Invoice
from app.repositories.invoice_repo import InvoiceRepository
from app.services.parsing.column_mapper import ColumnMapper
from app.services.state_machine import transition_invoice
from app.utils.decimal_utils import to_decimal
from app.utils.date_utils import parse_date


class BatchParser:
    def __init__(self, db: Session, tenant_id, batch, client):
        self.db = db
        self.tenant_id = tenant_id
        self.batch = batch
        self.client = client
        self.invoice_repo = InvoiceRepository(db=db, tenant_id=tenant_id)
        self.mapper = ColumnMapper(client.column_mapping)

    def _excel_chunks(self, file_path: Path) -> Iterator[pd.DataFrame]:
        probe = pd.read_excel(file_path, header=None, nrows=20)
        header_row = self.mapper.detect_header(probe.fillna("").values.tolist())
        columns = pd.read_excel(file_path, header=header_row, nrows=0).columns.tolist()
        start = header_row + 1
        while True:
            frame = pd.read_excel(file_path, header=None, skiprows=start, nrows=settings.batch_chunk_size)
            if frame.empty:
                break
            frame.columns = columns[: len(frame.columns)]
            start += len(frame)
            yield frame

    def _csv_chunks(self, file_path: Path) -> Iterator[pd.DataFrame]:
        probe = pd.read_csv(file_path, header=None, nrows=20)
        header_row = self.mapper.detect_header(probe.fillna("").values.tolist())
        yield from pd.read_csv(file_path, header=header_row, chunksize=settings.batch_chunk_size)

    def iter_chunks(self, file_path: Path) -> Iterator[pd.DataFrame]:
        if file_path.suffix.lower() == ".csv":
            yield from self._csv_chunks(file_path)
        else:
            yield from self._excel_chunks(file_path)

    def parse_chunk(self, frame: pd.DataFrame, row_offset: int) -> list[Invoice]:
        column_map = self.mapper.map_columns([str(value) for value in frame.columns])
        missing_fields = self.mapper.validate_mandatory_fields(column_map)
        if missing_fields:
            raise ValueError(f"Missing mandatory columns: {', '.join(missing_fields)}")
        frame = frame.rename(columns=column_map)
        invoices: list[Invoice] = []
        for index, row in frame.iterrows():
            row_data = row.to_dict()
            if all((str(value).strip() == "" or pd.isna(value)) for value in row_data.values()):
                continue
            existing = self.invoice_repo.get_existing_unique(client_id=self.client.id, batch_id=self.batch.id, invoice_number=str(row_data.get("invoice_number", "")).strip(), supplier_gstin=str(row_data.get("supplier_gstin", "")).strip())
            if existing is not None:
                invoices.append(existing)
                continue
            invoice = Invoice(
                tenant_id=self.tenant_id,
                batch_id=self.batch.id,
                client_id=self.client.id,
                invoice_number=str(row_data.get("invoice_number", "")).strip(),
                invoice_date=parse_date(row_data.get("invoice_date")),
                supplier_name=(str(row_data.get("supplier_name", "")).strip() or None),
                supplier_gstin=str(row_data.get("supplier_gstin", "")).strip(),
                recipient_gstin=str(row_data.get("recipient_gstin", "")).strip(),
                hsn_sac_code=str(row_data.get("hsn_sac_code", "")).strip(),
                taxable_value=to_decimal(row_data.get("taxable_value")),
                cgst_amount=to_decimal(row_data.get("cgst_amount")),
                sgst_amount=to_decimal(row_data.get("sgst_amount")),
                igst_amount=to_decimal(row_data.get("igst_amount")),
                total_invoice_value=to_decimal(row_data.get("total_invoice_value")),
                place_of_supply=str(row_data.get("place_of_supply", "")).strip(),
                applicable_rate=to_decimal(row_data.get("applicable_rate")) if row_data.get("applicable_rate") not in (None, "") else None,
                credit_note_flag=str(row_data.get("credit_note_flag", "")).strip().lower() in {"1", "true", "yes"},
                source_row_number=row_offset + index + 1,
                state=InvoiceState.RAW,
            )
            self.db.add(invoice)
            self.db.flush()
            transition_invoice(invoice=invoice, new_state=InvoiceState.PARSED, actor="system", db=self.db)
            invoices.append(invoice)
        return invoices
