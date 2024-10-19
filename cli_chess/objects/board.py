from collections import ChainMap
from functools import lru_cache
from types import MappingProxyType
from typing import Optional

from errors import BoardError
from objects.enums import Color, Direction
from objects.pieces import Piece
from objects.position import Position


class Board:
    def __init__(self):
        self._limit_pos = Position(7, 7)
        self._pieces_by_color: dict[Color, dict[Position, Piece]] = {Color.WHITE: {}, Color.BLACK: {}}

    @property
    def pieces_by_color(self) -> MappingProxyType[Color, MappingProxyType[Position, Piece]]:
        return self.__get_pieces_by_color()

    @lru_cache
    def __get_pieces_by_color(self) -> MappingProxyType[Color, MappingProxyType[Position, Piece]]:
        return MappingProxyType({color: MappingProxyType(pieces) for color, pieces in self._pieces_by_color.items()})

    @property
    def pieces(self) -> ChainMap[Position, Piece]:
        return self.__get_pieces()

    @lru_cache
    def __get_pieces(self) -> ChainMap[Position, Piece]:
        return ChainMap(
            self._pieces_by_color[Color.WHITE],
            self._pieces_by_color[Color.BLACK],
        )

    def has_piece_at_position(self, pos: Position, color: Optional[Color] = None) -> bool:
        """
        Return True if Board has the chess piece at the positions.
        """
        if color:
            return pos in self._pieces_by_color[color]
        return pos in self.pieces

    def add_piece(self, piece: Piece, pos: Position):
        """
        Adds the chess piece to the board at the position.
        """
        self.validate_position_on_board(pos)
        if self.has_piece_at_position(pos):
            raise BoardError(f'Cannot add the chess piece, position {pos} is occupied another chess piece.')
        self._pieces_by_color[piece.color][pos] = piece

    def remove_piece(self, piece: Piece, pos: Position):
        """
        Removes the chess piece from the board at the position.
        """
        self.validate_position_on_board(pos)
        if not self.has_piece_at_position(pos):
            raise BoardError(f'Cannot remove the chess piece, position {pos} is empty.')
        got_piece = self._pieces_by_color[Color.WHITE].get(pos) or self._pieces_by_color[Color.BLACK].get(pos)
        if piece is not got_piece:
            raise BoardError(f'Cannot remove the chess piece, there is a different chess piece at position {pos}.')
        del self._pieces_by_color[piece.color][pos]

    def get_piece(self, pos: Position) -> Piece:
        """
        Returns the chess piece from the board at the position.
        """
        self.validate_position_on_board(pos)
        if not self.has_piece_at_position(pos):
            raise BoardError(f'Cannot get the chess piece, position {pos} is empty.')
        got_piece = self._pieces_by_color[Color.WHITE].get(pos) or self._pieces_by_color[Color.BLACK].get(pos)
        assert got_piece is not None  # clue for mypy
        return got_piece

    def move_piece(self, start: Position, end: Position):
        """
        Moves the chess piece from the start position to the end position.
        """
        if start == end:
            raise BoardError(f'Cannot move chess piece, start position {start} and end position {end} match.')

        moving_piece = self.get_piece(start)

        if self.has_piece_at_position(end):
            attacked_piece = self.get_piece(end)
        else:
            attacked_piece = None

        moving_piece.check(start, end, self, attacked_piece)

        if attacked_piece is not None:
            self.remove_piece(attacked_piece, end)
        self.remove_piece(moving_piece, start)
        self.add_piece(moving_piece, end)

    def validate_position_on_board(self, pos: Position):
        if pos > self._limit_pos:
            raise BoardError('x and y cannot be greate then 7.')

    def get_possible_directions(self, pos: Position, piece: Piece) -> set[Direction]:
        """
        Returns a set of possible directions for a piece to move based on its position on the board and allowed directions of piece.
        """
        self.validate_position_on_board(pos)

        possible_direction = set(Direction)

        if pos.x == 0:
            possible_direction -= {Direction.LEFT, Direction.UP_LEFT, Direction.DOWN_LEFT}
        elif pos.x == 7:
            possible_direction -= {Direction.RIGHT, Direction.UP_RIGHT, Direction.DOWN_RIGHT}

        if pos.y == 0:
            possible_direction -= {Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT}
        if pos.y == 7:
            possible_direction -= {Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT}

        return possible_direction & piece.ALLOWED_MOVE_DIRECTIONS
