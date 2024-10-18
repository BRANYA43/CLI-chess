from pytest import fixture

from objects.board import Board
from objects.enums import Color, Direction
from objects.pieces import Piece, Queen, Bishop, Rook, Pawn, Knight, King


def __make_god_piece(piece: Piece):
    piece.ALLOWED_MOVE_DIRECTIONS = frozenset(Direction)
    piece.MAX_MOVE_COUNT = 8


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


@fixture
def w_pawn() -> Pawn:
    """
    White Pawn
    """
    return Pawn(Color.WHITE)


@fixture
def b_pawn() -> Pawn:
    """
    Black Pawn
    """
    return Pawn(Color.BLACK)


@fixture
def w_rook() -> Rook:
    """
    White Rook
    """
    return Rook(Color.WHITE)


@fixture
def b_rook() -> Rook:
    """
    Black Rook
    """
    return Rook(Color.BLACK)


@fixture
def w_knight() -> Knight:
    """
    White Knight
    """
    return Knight(Color.WHITE)


@fixture
def b_knight() -> Knight:
    """
    Black Knight
    """
    return Knight(Color.BLACK)


@fixture
def w_bishop() -> Bishop:
    """
    White Bishop
    """
    return Bishop(Color.WHITE)


@fixture
def b_bishop() -> Bishop:
    """
    Black Bishop
    """
    return Bishop(Color.BLACK)


@fixture
def w_queen() -> Queen:
    """
    White Queen
    """
    return Queen(Color.WHITE)


@fixture
def b_queen() -> Queen:
    """
    Black Queen
    """
    return Queen(Color.BLACK)


@fixture
def w_king():
    """
    White King
    """
    return King(Color.WHITE)


@fixture
def b_king() -> King:
    """
    Black King
    """
    return King(Color.BLACK)


@fixture
def board() -> Board:
    """
    Board
    """
    return Board()
