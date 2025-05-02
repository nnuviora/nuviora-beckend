import uuid
import io
import boto3
from PIL import Image
from config import config_setting  # або settings, якщо потрібно

s3 = boto3.client(
    "s3",
    aws_access_key_id=config_setting.ACCESS_KEY,
    aws_secret_access_key=config_setting.SECRET_ACCESS_KEY,
    region_name=config_setting.AWS_REGION
)

def upload_avatar(file_bytes: bytes, filename: str, content_type: str) -> str:
    # Відкрити зображення
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")
    image = image.resize((320, 320))

    # Зберегти в WebP у пам’ять
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP")
    buffer.seek(0)

    # Унікальне ім’я
    key = f"avatars/{uuid.uuid4()}.webp"

    # Завантажити в S3
    s3.put_object(
        Bucket=config_setting.AWS_BUCKET_NAME,
        Key=key,
        Body=buffer,
        ContentType="image/webp"
    )

    # Повернути URL
    url = f"https://{config_setting.AWS_BUCKET_NAME}.s3.{config_setting.AWS_REGION}.amazonaws.com/{key}"
    return url
