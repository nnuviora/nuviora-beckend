from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from config import config_setting


class AbstractEmail(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def send_email(
        self, recipient: str, subject: str, body_text: Optional[str] = None
    ):
        pass


class MetaUaSender(AbstractEmail):
    conf = ConnectionConfig(
        MAIL_USERNAME=config_setting.MAIL_USERNAME,
        MAIL_PASSWORD=config_setting.MAIL_PASSWORD,
        MAIL_FROM=config_setting.MAIL_USERNAME,
        MAIL_PORT=config_setting.MAIL_PORT,
        MAIL_SERVER=config_setting.MAIL_SERVER,
        MAIL_FROM_NAME="Test Systems",
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    )

    def __init__(self) -> None:
        self.fm = FastMail(self.conf)

    async def send_email(
        self, recipient: str, subject: str, body_text: Optional[str] = None
    ):
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[recipient],
                body=body_text or "",
                subtype=MessageType.html,
            )
            await self.fm.send_message(message)
        except ConnectionErrors as err:
            raise Exception(f"Error sending email: {err}")
