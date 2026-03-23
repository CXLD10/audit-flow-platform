from io import BytesIO
from pathlib import Path

import boto3

from app.core.config import settings


class S3StorageClient:
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
        self.bucket = settings.s3_bucket_name

    def upload_bytes(self, *, key: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        self.client.put_object(Bucket=self.bucket, Key=key, Body=content, ContentType=content_type)
        return key

    def download_to_bytes(self, key: str) -> bytes:
        response = self.client.get_object(Bucket=self.bucket, Key=key)
        return response["Body"].read()

    def download_to_tempfile(self, key: str, target_path: Path) -> Path:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.bucket, key, str(target_path))
        return target_path
