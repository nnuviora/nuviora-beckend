import boto3
import uuid
import io
from PIL import Image, ImageOps
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile, HTTPException
from config import config_setting


class LoadService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config_setting.ACCESS_KEY,
            aws_secret_access_key=config_setting.SECRET_ACCESS_KEY,
            region_name=config_setting.AWS_REGION,
        )
        self.bucket = config_setting.AWS_BUCKET_NAME

    async def upload_image_to_s3(self, avatar: UploadFile) -> str:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG are allowed")

        try:
            # Обробка зображення
            file_bytes = await avatar.read()  # Читаємо весь файл
            image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            image = ImageOps.fit(image, (320, 320), centering=(0.5, 0.5))
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP")
            buffer.seek(0)

            # Створення ключа та завантаження
            avatar_key = f"avatars/{uuid.uuid4()}.webp"

            self.s3.upload_fileobj(
                buffer, self.bucket, avatar_key, ExtraArgs={"ContentType": "image/webp"}
            )
            avatar_url = f"https://{self.bucket}.s3.amazonaws.com/{avatar_key}"

            return avatar_url

        except (BotoCoreError, ClientError) as e:
            raise HTTPException(status_code=500, detail="Failed to upload avatar to S3")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Image processing failed: {str(e)}"
            )

    async def get_s3_image_from_db(self, user_uuid) -> str:
        key = f"avatars/{user_uuid}.webp"
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)

        except (BotoCoreError, ClientError) as e:
            raise HTTPException(status_code=500, detail="Failed to get avatar from S3")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image failed: {str(e)}")

        return f"https://{self.bucket}.s3.amazonaws.com/{key}"
