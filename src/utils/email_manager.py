from abc import ABC, abstractmethod
from typing import Optional

import boto3

from config import config_setting


class AbstractEmail(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def send_email(
        self,
        recipient: str,
        subject: str,
        body_text: Optional[str] = None,
    ):
        pass


class AwsSender(AbstractEmail):
    SENDER = config_setting.SENDER
    CHARSET = config_setting.CHARSET
    CONFIGURATION_SET = config_setting.CONFIGURATION_SET

    def __init__(self) -> None:
        self.client = boto3.client(
            "ses",
            region_name=config_setting.AWS_REGION,
            aws_access_key_id=config_setting.ACCESS_KEY,
            aws_secret_access_key=config_setting.SECRET_ACCESS_KEY,
        )

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body_text: Optional[str] = None,
    ):
        try:
            response = self.client.send_email(
                Destination={
                    "ToAddresses": [
                        recipient,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": self.CHARSET,
                            "Data": "<h1>Hello</h1>",  # BODY_HTML,
                        },
                        "Text": {
                            "Charset": self.CHARSET,
                            "Data": body_text,
                        },
                    },
                    "Subject": {
                        "Charset": self.CHARSET,
                        "Data": subject,
                    },
                },
                Source=self.SENDER,
                ConfigurationSetName=self.CONFIGURATION_SET,
            )
            return response
        except Exception as e:
            raise Exception(f"Error send email: {e}")
