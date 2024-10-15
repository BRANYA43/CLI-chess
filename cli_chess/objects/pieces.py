from collections import deque
from typing import Optional

from errors import PieceError
from objects.enums import Color, Direction
from objects.position import Position
from functools import partial


class Piece:
    """Base class of all chess pieces"""

    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset()

    MAX_MOVE_COUNT = 0

    CAN_MOVE_OR_ATTACK_THROUGH = False

    def __init__(self, color: int):
        self._color = Color(color)

    def __str__(self):
        return f'{self.color.name.title()} {self.name}'

    def __repr__(self):
        return f'<Piece(id:{id(self)}, color:{self.color}>'

    @property
    def color(self) -> Color:
        return self._color

    @property
    def name(self) -> str:
        return type(self).__name__

    def is_ally_for(self, piece: 'Piece') -> bool:
        return self.color == piece.color

    def check(
        self,
        start: Position,
        end: Position,
        board,
        attacked_piece: Optional['Piece'] = None,
        *,
        raise_exception=True,
        **kwargs,
    ) -> bool:
        """
        Checks whether the chess piece moves from the start position to the end position.
        :keyword diagonal_direction: if True then it considers diagonal directions (e.g. Bishop, Queen).
        """
        direction = start.get_direction(end)
        distance = start.get_distance(end, diagonal_direction=kwargs.pop('diagonal_direction', True))
        check_methods = deque(
            [
                partial(self.check_move_in_direction, direction, raise_exception=raise_exception, **kwargs),
                partial(self.check_move_distance, distance, raise_exception=raise_exception, **kwargs),
                partial(self.check_get_to_end_position, start, end, board, raise_exception=raise_exception, **kwargs),
            ]
        )
        if attacked_piece is not None:
            check_methods.appendleft(partial(self.check_attack, attacked_piece, raise_exception=raise_exception))

        for check in check_methods:
            if not check():
                return False
        return True

    def check_attack(self, attacked_piece: 'Piece', *, raise_exception=False) -> bool:
        """
        Checks whether the chess piece attack the ally chess piece.
        """
        if self.is_ally_for(attacked_piece):
            if raise_exception:
                raise PieceError('Ally pieces cannot attacked each other.')
            return False
        return True

    def check_move_in_direction(self, direction: Direction, *, raise_exception=False, **kwargs) -> bool:
        """
        Checks whether the chess piece can move in a direction.
        """
        result = direction in self.ALLOWED_MOVE_DIRECTIONS
        if raise_exception and not result:
            raise PieceError(f'{self.name} cannot move in the {direction} direction.')
        return result

    def check_get_to_end_position(
        self, start: Position, end: Position, board, *, raise_exception=False, **kwargs
    ) -> bool:
        """
        Checks whether the chess piece can get from the start to the end position.
        """
        if self.CAN_MOVE_OR_ATTACK_THROUGH:
            return True

        try:
            for next_pos in start.get_range_between(end):
                if board.has_piece_at_position(next_pos):
                    if raise_exception:
                        raise PieceError(f'{self.name} cannot move through another chess piece.')
                    return False
        except ValueError:
            if raise_exception:
                raise PieceError(f'{self.name} cannot get from start({start}) to end({end}) position.')
            return False

        return True

    def check_move_distance(self, distance: int, *, raise_exception=False, **kwargs) -> bool:
        """
        Checks whether the chess piece can move the distance of squares.
        """
        result = 1 <= distance <= self.MAX_MOVE_COUNT
        if raise_exception and not result:
            raise PieceError(f'{self.name} cannot move {distance} squares.')
        return result


class Rook(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction.get_direct_directions())

    MAX_MOVE_COUNT = 8


class Bishop(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction.get_diagonal_directions())

    MAX_MOVE_COUNT = 8


class Queen(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction)

    MAX_MOVE_COUNT = 8
