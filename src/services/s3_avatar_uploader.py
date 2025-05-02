import uuid
import io
from PIL import Image
import boto3

from config import config_setting
from utils.abstract_storage import AbstractStorage


class S3AvatarUploader(AbstractStorage):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config_setting.ACCESS_KEY,
            aws_secret_access_key=config_setting.SECRET_ACCESS_KEY,
            region_name=config_setting.AWS_REGION
        )
        self.bucket = config_setting.AWS_BUCKET_NAME
        self.region = config_setting.AWS_REGION

    def upload_avatar(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        image = Image.open(io.BytesIO(file_bytes))
        image = image.convert("RGB")
        image = image.resize((320, 320))

        buffer = io.BytesIO()
        image.save(buffer, format="WEBP")
        buffer.seek(0)

        key = f"avatars/{uuid.uuid4()}.webp"

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=buffer,
            ContentType="image/webp",
        )

        url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        return url
