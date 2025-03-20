from abc import ABC, abstractmethod
from typing import Optional

import boto3


class AbstractEmail(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body_text: Optional[str]=None
        ) -> bool:
        pass


class AwsSender(AbstractEmail):
    SENDER = None
    CHARSET = None
    CONFIGURATION_SET = None

    def __init__(self):
        self.client = None

    async def send_email(self, recipient: str, subject: str, body_text: Optional[str]=None):
        try:
            response = self.client.send_email(
                Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': self.CHARSET,
                        'Data': None,#BODY_HTML,
                    },
                    'Text': {
                        'Charset': self.CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': self.CHARSET,
                    'Data': subject,
                },
            },
            Source=self.SENDER,
            ConfigurationSetName=self.CONFIGURATION_SET,
            )
            return response
        except Exception as e:
            raise Exception(f"Error send email: {e}")