from typing import Optional
import re


class CustomError(Exception):
    """Base class of all errors"""

    default_msg: str = ''

    def __init__(self, msg: Optional[str] = None, **kwargs):
        if msg is None:
            msg = self.default_msg
            if re.search(r'{\w+}', self.default_msg) is not None:
                msg = msg.format(**kwargs)
        super().__init__(msg)


class PieceError(CustomError):
    pass


class BoardError(CustomError):
    pass
