from typing import Generator

from objects.enums import Direction
from objects.vector import Vector


class Position:
    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('x and y must be integer.')
        if x < 0 or y < 0:
            raise ValueError('x and y must be greate than or equal to 0')
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __repr__(self):
        return f'Position({self._x}, {self._y})'

    def __add__(self, other) -> 'Position':
        if isinstance(other, Vector):
            return Position(self._x + other.x, self._y + other.y)
        raise TypeError(f'Expected Vector, but got {type(other).__name__}.')

    def __sub__(self, other) -> Vector:
        self.__valid_position(other)
        return Vector(self._x - other.x, self._y - other.y)

    def __eq__(self, other):
        self.__valid_position(other)
        return self._x == other.x and self._y == other.y

    def __ne__(self, other):
        self.__valid_position(other)
        return self._x != other.x or self._y != other.y

    def get_direction(self, pos: 'Position') -> Direction:
        """
        Return vector direction between two positions.
        """
        vector = pos - self
        return Direction.get_direction(vector)

    def get_distance(self, pos: 'Position', *, diagonal_direction=True) -> int:
        """
        Return vector direction between two positions.
        'diagonal_direction' flag to considers diagonal directions for pieces being able to move by diagonals
        (Bishop, Queen). By default, True.
        """
        vector = pos - self
        direction = Direction.get_direction(vector)
        distance = abs(vector)
        if direction in Direction.get_diagonal_directions() and diagonal_direction:
            if distance % 2 != 0:
                raise ValueError(
                    'Positions must be on the same straight line, where between this line and x or y axis '
                    'angle is equal to 0, 90, 180 degrees.'
                )
            return distance // 2
        return distance

    def get_range_between(self, pos: 'Position') -> Generator['Position', None, None]:
        """
        Returns position range between start and end positions. Start and end positions are excluded to range.
        """
        vector = pos - self
        distance = abs(vector)

        if distance % 2 != 0:
            raise ValueError(
                'Positions must be on the same straight line, where between this line and x or y axis '
                'angle is equal to 0, 90, 180 degrees.'
            )

        direction = Direction.get_direction(vector)

        if direction in Direction.get_diagonal_directions():
            distance //= 2

        direction_vector = direction.vector

        next_pos = self
        for _ in range(distance - 1):
            next_pos += direction_vector
            yield next_pos

    @staticmethod
    def __valid_position(value):
        if not isinstance(value, Position):
            raise TypeError(f'Expected Position, but got {type(value).__name__}.')