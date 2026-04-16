import aioboto3
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

S3_SETTINGS = {
    "endpoint_url": os.getenv("MINIO_ENDPOINT"),
    "aws_access_key_id": os.getenv("MINIO_ROOT_USER"),
    "aws_secret_access_key": os.getenv("MINIO_ROOT_PASSWORD"),
    "region_name": "us-east-1",
}

class S3Storage:
    def __init__(self):
        self.session = aioboto3.Session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.client("s3", **S3_SETTINGS) as client:
            yield client

    async def upload_file(self, file_obj, bucket: str, key: str, content_type: str):
        async with self.get_client() as s3:
            # Загружаем напрямую из файлового объекта
            await s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=file_obj,
                ContentType=content_type
            )
            # Формируем итоговую ссылку для БД
            return f"{S3_SETTINGS['endpoint_url']}/{bucket}/{key}"

storage = S3Storage()
