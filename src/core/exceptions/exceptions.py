class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class WrongUserDataException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class InvalidTokenException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=423)