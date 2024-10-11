from pytest import fixture

from objects.enums import Color, Direction
from objects.pieces import Piece


def __make_god_piece(piece: Piece):
    piece.ALLOWED_MOVE_DIRECTIONS = frozenset(Direction)
    piece.MAX_MOVE_COUNT = 8
    piece.CAN_MOVE_OR_ATTACK_THROUGH = True


@fixture
def w_piece() -> Piece:
    """
    White Piece
    """
    return Piece(Color.WHITE)


@fixture
def b_piece() -> Piece:
    """
    Black Piece
    """
    return Piece(Color.BLACK)


@fixture
def w_god_piece(w_piece) -> Piece:
    """
    White God Piece
    """
    __make_god_piece(w_piece)
    return w_piece


@fixture
def b_god_piece(b_piece) -> Piece:
    """
    Black God Piece
    """
    __make_god_piece(b_piece)
    return b_piece
