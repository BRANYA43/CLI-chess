from typing import Optional


class CustomError(Exception):
    """Base class of all errors"""

    default_msg = None

    def __init__(self, msg: Optional[str] = None):
        message = self.default_msg if msg is None else msg
        super().__init__(message)
