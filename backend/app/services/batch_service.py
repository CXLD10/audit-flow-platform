from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.batch_repo import BatchRepository
from app.repositories.error_repo import ErrorRepository
from app.repositories.invoice_repo import InvoiceRepository
from app.repositories.reconciliation_repo import ReconciliationRepository
from app.services.export.excel_exporter import ExcelExporter
from app.services.export.gstr1_generator import GSTR1Generator
from app.services.prioritization.prioritizer import ErrorPrioritizer
from app.services.progress_service import ProgressService


class BatchService:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.batch_repo = BatchRepository(db=db, tenant_id=tenant_id)
        self.invoice_repo = InvoiceRepository(db=db, tenant_id=tenant_id)
        self.error_repo = ErrorRepository(db=db, tenant_id=tenant_id)
        self.recon_repo = ReconciliationRepository(db=db, tenant_id=tenant_id)
        self.progress_service = ProgressService()
        self.exporter = ExcelExporter()
        self.gstr1_generator = GSTR1Generator()

    def get_batch(self, batch_id: UUID):
        batch = self.batch_repo.get_by_id(batch_id)
        if batch is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
        return batch

    def get_progress(self, batch_id: UUID) -> dict:
        return self.progress_service.get(batch_id) or {"stage": "QUEUED", "pct": 0, "processed": 0, "total": 0, "status": "QUEUED", "error_message": None, "degraded": False}

    def get_results(self, batch_id: UUID) -> dict:
        batch = self.get_batch(batch_id)
        invoices = self.invoice_repo.list_all_by_batch(batch_id)
        errors = self.error_repo.list_by_batch(batch_id)
        invoice_map = {invoice.id: invoice for invoice in invoices}
        errors = ErrorPrioritizer.sort_errors(errors, invoice_map)
        degraded = []
        if any(invoice.gstn_verification_status and invoice.gstn_verification_status.value == "GSTIN_UNVERIFIED" for invoice in invoices):
            degraded.append("Live GSTN verification unavailable. Results show format validation only.")
        return {"batch": batch, "invoices": invoices, "errors": errors, "degraded_messages": degraded}

    def export(self, batch_id: UUID, export_type: str) -> tuple[bytes, str, str]:
        batch = self.get_batch(batch_id)
        invoices = self.invoice_repo.list_all_by_batch(batch_id)
        errors = self.error_repo.list_by_batch(batch_id)
        invoice_map = {invoice.id: invoice for invoice in invoices}
        errors = ErrorPrioritizer.sort_errors(errors, invoice_map)
        recon_results = [invoice.reconciliation_result for invoice in invoices if invoice.reconciliation_result is not None]
        if export_type == "validation":
            content = self.exporter.build_validation_report(batch=batch, invoices=invoices, errors=errors, reconciliation_results=recon_results)
            return content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", f"batch-{batch_id}-validation.xlsx"
        if export_type == "gstr1":
            critical_errors = [error for error in errors if error.severity.value == "CRITICAL"]
            if critical_errors:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot generate draft GSTR-1 while CRITICAL errors exist")
            content = self.gstr1_generator.build_draft(invoices=invoices)
            return content, "application/json", f"batch-{batch_id}-gstr1.json"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported export type")
