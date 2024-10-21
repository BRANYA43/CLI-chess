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


class AllyAttackError(PieceError):
    default_msg = 'Cannot attack an allied piece.'


class InvalidMoveDirectionError(PieceError):
    default_msg = '{name} cannot move in the {direction} direction.'


class BlockedMoveError(PieceError):
    default_msg = '{name} is blocked by another chess piece.'


class InvalidMovePathError(PieceError):
    default_msg = '{name} cannot move from {start} to {end} due to an invalid path'


class InvalidMoveDistanceError(PieceError):
    default_msg = '{name} cannot move {distance} squares. Maximum allowed distance is {max_moves} squares.'


class BoardError(CustomError):
    pass
