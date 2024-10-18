from typing import Sequence

import pytest

from objects.board import Board
from objects.enums import Color, Direction
from objects.pieces import Piece, Queen, Bishop, Rook, Pawn, Knight, King
from objects.position import Position


def __make_god_piece(piece: Piece):
    piece.ALLOWED_MOVE_DIRECTIONS = frozenset(Direction)
    piece.MAX_MOVE_COUNT = 8


def get_position_list(coords: Sequence[tuple[int, int]]) -> list[Position]:
    return [Position(x, y) for x, y in coords]


@pytest.fixture()
def w_piece() -> Piece:
    """
    White Piece
    """
    return Piece(Color.WHITE)


@pytest.fixture()
def b_piece() -> Piece:
    """
    Black Piece
    """
    return Piece(Color.BLACK)


@pytest.fixture()
def w_god_piece(w_piece) -> Piece:
    """
    White God Piece
    """
    __make_god_piece(w_piece)
    return w_piece


@pytest.fixture()
def b_god_piece(b_piece) -> Piece:
    """
    Black God Piece
    """
    __make_god_piece(b_piece)
    return b_piece


@pytest.fixture()
def w_pawn() -> Pawn:
    """
    White Pawn
    """
    return Pawn(Color.WHITE)


@pytest.fixture()
def b_pawn() -> Pawn:
    """
    Black Pawn
    """
    return Pawn(Color.BLACK)


@pytest.fixture()
def w_rook() -> Rook:
    """
    White Rook
    """
    return Rook(Color.WHITE)


@pytest.fixture()
def b_rook() -> Rook:
    """
    Black Rook
    """
    return Rook(Color.BLACK)


@pytest.fixture()
def w_knight() -> Knight:
    """
    White Knight
    """
    return Knight(Color.WHITE)


@pytest.fixture()
def b_knight() -> Knight:
    """
    Black Knight
    """
    return Knight(Color.BLACK)


@pytest.fixture()
def w_bishop() -> Bishop:
    """
    White Bishop
    """
    return Bishop(Color.WHITE)


@pytest.fixture()
def b_bishop() -> Bishop:
    """
    Black Bishop
    """
    return Bishop(Color.BLACK)


@pytest.fixture()
def w_queen() -> Queen:
    """
    White Queen
    """
    return Queen(Color.WHITE)


@pytest.fixture()
def b_queen() -> Queen:
    """
    Black Queen
    """
    return Queen(Color.BLACK)


@pytest.fixture()
def w_king():
    """
    White King
    """
    return King(Color.WHITE)


@pytest.fixture()
def b_king() -> King:
    """
    Black King
    """
    return King(Color.BLACK)


@pytest.fixture()
def board() -> Board:
    """
    Board
    """
    return Board()
