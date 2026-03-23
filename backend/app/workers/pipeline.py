import asyncio
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.models.enums import BatchStatus, GSTNVerificationStatus, Severity
from app.repositories.batch_repo import BatchRepository
from app.repositories.client_repo import ClientRepository
from app.repositories.invoice_repo import InvoiceRepository
from app.repositories.error_repo import ErrorRepository
from app.services.parsing.parser import BatchParser
from app.services.normalization.normalizer import InvoiceNormalizer
from app.services.entity_resolution.resolver import EntityResolver
from app.services.gstn.client import GSTNApiClient
from app.services.progress_service import ProgressService
from app.services.reconciliation.reconciler import ReconciliationEngine
from app.services.storage.s3_client import S3StorageClient
from app.services.validation.engine import ValidationEngine
from app.models.validation_error import ValidationErrorRecord

log = get_logger(__name__)

STAGE_ORDER = ["PARSING", "NORMALIZATION", "ENTITY_RESOLUTION", "VALIDATION", "GSTN_VERIFICATION", "RECONCILIATION", "PRIORITIZATION"]


class PipelineRunner:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id
        self.batch_repo = BatchRepository(db=db, tenant_id=tenant_id)
        self.client_repo = ClientRepository(db=db, tenant_id=tenant_id)
        self.invoice_repo = InvoiceRepository(db=db, tenant_id=tenant_id)
        self.error_repo = ErrorRepository(db=db, tenant_id=tenant_id)
        self.progress = ProgressService()
        self.storage = S3StorageClient()
        self.gstn_client = GSTNApiClient()

    def _set_progress(self, *, batch_id: UUID, stage: str, pct: int, processed: int, total: int, status: str, error_message: str | None = None, degraded: bool = False):
        self.progress.set(batch_id, {"stage": stage, "pct": pct, "processed": processed, "total": total, "status": status, "error_message": error_message, "degraded": degraded})

    def _resume_should_skip(self, batch, stage: str) -> bool:
        if batch.last_completed_stage is None:
            return False
        return STAGE_ORDER.index(batch.last_completed_stage) >= STAGE_ORDER.index(stage)

    def run(self, batch_id: UUID) -> None:
        batch = self.batch_repo.get_by_id(batch_id)
        if batch is None:
            raise ValueError("Batch not found")
        if batch.status == BatchStatus.COMPLETE:
            log.info("batch_already_complete", batch_id=str(batch_id), tenant_id=str(self.tenant_id))
            return
        client = self.client_repo.get_by_id(batch.client_id)
        if client is None:
            raise ValueError("Client not found")
        batch.status = BatchStatus.PROCESSING
        self.db.commit()
        self._set_progress(batch_id=batch_id, stage="PARSING", pct=0, processed=0, total=max(batch.total_invoices, 1), status="PROCESSING")
        try:
            with TemporaryDirectory() as tmp_dir:
                local_path = self.storage.download_to_tempfile(batch.file_path_s3, Path(tmp_dir) / batch.filename)
                total_processed = batch.total_invoices
                if not self._resume_should_skip(batch, "PARSING"):
                    parser = BatchParser(self.db, self.tenant_id, batch, client)
                    total_processed = 0
                    for frame in parser.iter_chunks(local_path):
                        invoices = parser.parse_chunk(frame, total_processed)
                        total_processed += len(invoices)
                        self.db.flush()
                        self.db.commit()
                        self._set_progress(batch_id=batch_id, stage="PARSING", pct=10, processed=total_processed, total=total_processed, status="PROCESSING")
                    self.batch_repo.update_checkpoint(batch, stage="PARSING", total_invoices=total_processed)
                    self.db.commit()
                invoices = self.invoice_repo.list_all_by_batch(batch_id)
                total_processed = len(invoices)
                if not self._resume_should_skip(batch, "NORMALIZATION"):
                    for start in range(0, total_processed, settings.batch_chunk_size):
                        chunk = invoices[start:start + settings.batch_chunk_size]
                        for invoice in chunk:
                            InvoiceNormalizer.normalize(invoice, self.db)
                        self.db.flush(); self.db.commit(); del chunk
                        self._set_progress(batch_id=batch_id, stage="NORMALIZATION", pct=25, processed=min(start + settings.batch_chunk_size, total_processed), total=total_processed, status="PROCESSING")
                    self.batch_repo.update_checkpoint(batch, stage="NORMALIZATION")
                    self.db.commit()
                if not self._resume_should_skip(batch, "ENTITY_RESOLUTION"):
                    resolver = EntityResolver(self.db, self.tenant_id, batch.id)
                    resolver.resolve(invoices)
                    self.db.commit()
                    self.batch_repo.update_checkpoint(batch, stage="ENTITY_RESOLUTION")
                    self.db.commit()
                    self._set_progress(batch_id=batch_id, stage="ENTITY_RESOLUTION", pct=35, processed=total_processed, total=total_processed, status="PROCESSING")
                if not self._resume_should_skip(batch, "VALIDATION"):
                    validation_errors = ValidationEngine(self.db, self.tenant_id).validate_batch(invoices)
                    self.db.commit()
                    self.batch_repo.update_checkpoint(batch, stage="VALIDATION", error_count=len(validation_errors))
                    self.db.commit()
                    self._set_progress(batch_id=batch_id, stage="VALIDATION", pct=55, processed=total_processed, total=total_processed, status="PROCESSING")
                if not self._resume_should_skip(batch, "GSTN_VERIFICATION"):
                    unique_gstins = sorted({invoice.supplier_gstin for invoice in invoices if invoice.supplier_gstin})
                    gstin_results = asyncio.run(self.gstn_client.verify_many(unique_gstins)) if unique_gstins else {}
                    degraded = False
                    gstn_errors = []
                    for invoice in invoices:
                        result = gstin_results.get(invoice.supplier_gstin)
                        if result is None:
                            continue
                        if result.degraded:
                            degraded = True
                            invoice.gstn_verification_status = GSTNVerificationStatus.GSTIN_UNVERIFIED
                            continue
                        status_value = str(result.data.get("status", "GSTIN_UNVERIFIED")).upper()
                        invoice.gstn_verification_status = GSTNVerificationStatus(status_value) if status_value in GSTNVerificationStatus._value2member_map_ else GSTNVerificationStatus.GSTIN_UNVERIFIED
                        if invoice.gstn_verification_status in {GSTNVerificationStatus.CANCELLED, GSTNVerificationStatus.SUSPENDED}:
                            gstn_errors.append(
                                ValidationErrorRecord(
                                    tenant_id=self.tenant_id,
                                    invoice_id=invoice.id,
                                    batch_id=batch.id,
                                    rule_id="GSTIN_INACTIVE",
                                    severity=Severity.CRITICAL,
                                    field_name="supplier_gstin",
                                    actual_value=invoice.supplier_gstin,
                                    expected_value="ACTIVE GSTIN",
                                    message="Supplier GSTIN is cancelled or suspended in live GSTN verification",
                                )
                            )
                    if gstn_errors:
                        self.error_repo.create_many(gstn_errors)
                        batch.error_count += len(gstn_errors)
                    self.db.commit()
                    self.batch_repo.update_checkpoint(batch, stage="GSTN_VERIFICATION")
                    self.db.commit()
                    self._set_progress(batch_id=batch_id, stage="GSTN_VERIFICATION", pct=70, processed=total_processed, total=total_processed, status="PROCESSING", degraded=degraded)
                if not self._resume_should_skip(batch, "RECONCILIATION"):
                    period = batch.return_period.strftime("%Y-%m") if batch.return_period else ""
                    if period:
                        ReconciliationEngine(self.db, self.tenant_id).reconcile(invoices=invoices, client_id=client.id, period=period)
                    self.db.commit()
                    self.batch_repo.update_checkpoint(batch, stage="RECONCILIATION")
                    self.db.commit()
                    self._set_progress(batch_id=batch_id, stage="RECONCILIATION", pct=90, processed=total_processed, total=total_processed, status="PROCESSING")
                self.batch_repo.mark_complete(batch, total_invoices=total_processed, error_count=batch.error_count, last_completed_stage="PRIORITIZATION")
                self.db.commit()
                self._set_progress(batch_id=batch_id, stage="PRIORITIZATION", pct=100, processed=total_processed, total=total_processed, status="COMPLETE")
        except Exception as exc:  # noqa: BLE001
            log.error("pipeline_failed", batch_id=str(batch_id), tenant_id=str(self.tenant_id), error=str(exc), traceback=traceback.format_exc())
            self.batch_repo.mark_failed(batch, stage=batch.last_completed_stage or "PARSING", error_message=str(exc))
            self.db.commit()
            self._set_progress(batch_id=batch_id, stage=batch.last_completed_stage or "PARSING", pct=0, processed=batch.total_invoices, total=batch.total_invoices or 0, status="FAILED", error_message=str(exc))
            raise
