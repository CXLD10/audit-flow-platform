from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import CurrentUser
from app.repositories.batch_repo import BatchRepository
from app.repositories.client_repo import ClientRepository
from app.services.storage.s3_client import S3StorageClient
from app.workers.tasks import process_batch


class UploadService:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id
        self.batch_repo = BatchRepository(db=db, tenant_id=tenant_id)
        self.client_repo = ClientRepository(db=db, tenant_id=tenant_id)
        self.storage = S3StorageClient()

    def upload_batch(self, *, current_user: CurrentUser, upload_file: UploadFile, client_gstin: str, return_period=None):
        extension = Path(upload_file.filename or "").suffix.lower()
        if extension not in settings.allowed_file_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format")
        content = upload_file.file.read()
        if len(content) > settings.max_upload_size_bytes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File exceeds 50MB limit")
        client = self.client_repo.get_by_gstin(client_gstin)
        if client is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client GSTIN not found")
        batch_id = uuid4()
        key = f"{self.tenant_id}/{client_gstin}/{batch_id}/raw/{upload_file.filename}"
        self.storage.upload_bytes(key=key, content=content, content_type=upload_file.content_type or "application/octet-stream")
        batch = self.batch_repo.create(
            id=batch_id,
            client_id=client.id,
            user_id=current_user.id,
            filename=upload_file.filename or f"upload-{batch_id}",
            file_path_s3=key,
            return_period=return_period,
        )
        self.db.commit()
        process_batch.delay(str(batch.id), str(self.tenant_id))
        return batch
