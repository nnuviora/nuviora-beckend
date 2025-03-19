import uuid
from typing import Protocol


class UserService(Protocol):
    def __init__(self) -> None:
        pass