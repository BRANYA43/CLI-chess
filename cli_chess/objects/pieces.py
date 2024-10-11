from typing import Optional

from errors import PieceError
from objects.enums import Color, Direction
from objects.position import Position


class Piece:
    """Base class of all chess pieces"""

    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset()

    MAX_MOVE_COUNT = 0

    CAN_MOVE_OR_ATTACK_THROUGH = False

    def __init__(self, color: int):
        self._color = Color(color)

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
        attacked_piece: Optional['Piece'] = None,
        *,
        raise_exception=True,
        **kwargs,
    ) -> bool:
        """
        Checks whether the chess piece moves from the start position to the end position.
        :keyword diagonal_direction: if True then it considers diagonal directions (e.g. Bishop, Queen).
        """

        if attacked_piece is not None:
            is_ally = self.is_ally_for(attacked_piece)
            if is_ally and raise_exception:
                raise PieceError('Ally pieces cannot attacked each other.')
            elif is_ally:
                return False

        direction = start.get_direction(end)
        can_move_to_direction = self.can_move_in_direction(direction, raise_exception=raise_exception, **kwargs)
        if not can_move_to_direction:
            return False

        distance = start.get_distance(end, diagonal_direction=kwargs.pop('diagonal_direction', True))
        can_move_distance = self.can_move_distance(distance, raise_exception=raise_exception, **kwargs)
        if not can_move_distance:
            return False

        can_move_through = self.can_move_through_another_piece(raise_exception=raise_exception, **kwargs)
        if not can_move_through:
            return False

        return True

    def can_move_in_direction(self, direction: Direction, *, raise_exception=False, **kwargs) -> bool:
        """
        Returns True if the chess piece can move in a direction else False.
        """
        result = direction in self.ALLOWED_MOVE_DIRECTIONS
        if raise_exception and not result:
            raise PieceError(f'{self.name} cannot move in the {direction} direction.')
        return result

    def can_move_through_another_piece(self, *, raise_exception=False, **kwargs) -> bool:
        """
        Returns True if the chess piece can move through another chess piece else False.
        """
        result = self.CAN_MOVE_OR_ATTACK_THROUGH
        if raise_exception and not result:
            raise PieceError(f'{self.name} cannot move through another chess piece.')
        return result

    def can_move_distance(self, distance: int, *, raise_exception=False, **kwargs) -> bool:
        """
        Returns True if the chess piece can move the distance of squares else False.
        """
        result = 1 <= distance <= self.MAX_MOVE_COUNT
        if raise_exception and not result:
            raise PieceError(f'{self.name} cannot move {distance} squares.')
        return result
