from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import CurrentUser, require_role
from app.schemas.batch import BatchProgressResponse, BatchResultsResponse, BatchUploadResponse
from app.services.batch_service import BatchService
from app.services.ingestion.upload_service import UploadService

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post("/upload", response_model=BatchUploadResponse)
def upload_batch(
    client_gstin: str,
    return_period: date | None = None,
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(require_role("CA", "CLIENT", "ADMIN")),
    db: Session = Depends(get_db),
):
    batch = UploadService(db=db, tenant_id=current_user.tenant_id).upload_batch(current_user=current_user, upload_file=file, client_gstin=client_gstin, return_period=return_period)
    return BatchUploadResponse(batch_id=batch.id, status="QUEUED")


@router.get("/{batch_id}/progress", response_model=BatchProgressResponse)
def get_progress(batch_id: UUID, current_user: CurrentUser = Depends(require_role("CA", "CLIENT", "ADMIN")), db: Session = Depends(get_db)):
    return BatchService(db=db, tenant_id=current_user.tenant_id).get_progress(batch_id)


@router.get("/{batch_id}/results", response_model=BatchResultsResponse)
def get_results(batch_id: UUID, current_user: CurrentUser = Depends(require_role("CA", "CLIENT", "ADMIN")), db: Session = Depends(get_db)):
    return BatchService(db=db, tenant_id=current_user.tenant_id).get_results(batch_id)


@router.get("/{batch_id}/export")
def export_batch(batch_id: UUID, type: str = Query("validation"), current_user: CurrentUser = Depends(require_role("CA", "ADMIN")), db: Session = Depends(get_db)):
    content, media_type, filename = BatchService(db=db, tenant_id=current_user.tenant_id).export(batch_id, type)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=content, media_type=media_type, headers=headers)
