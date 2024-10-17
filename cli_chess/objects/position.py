from typing import Generator

from objects.enums import Direction
from objects.vector import Vector


class Position:
    __match_args__ = ('x', 'y')

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

    def __str__(self):
        return f'x:{self._x}, y:{self._y}'

    def __hash__(self):
        return hash((self._x, self._y))

    def __repr__(self):
        return f'<Position(x:{self._x}, y:{self._y})>'

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

    def __gt__(self, other):
        self.__valid_position(other)
        return self._y > other.y or (self._y == other.y and self._x > other.x)

    def __ge__(self, other):
        self.__valid_position(other)
        return self > other or self == other

    def __lt__(self, other):
        self.__valid_position(other)
        return self._y < other.y or (self._y == other.y and self._x < other.x)

    def __le__(self, other):
        self.__valid_position(other)
        return self < other or self == other

    def get_direction(self, pos: 'Position') -> Direction:
        """
        Return vector direction between two positions.
        """
        vector = pos - self
        return Direction.get_direction(vector)

    def get_distance(self, pos: 'Position', *, is_difficult=False) -> int:
        """
        Return vector direction between two positions.
        'is_difficult' - flag to calculate difficult move pattern e.g. L-move of Knight
        """
        vector = pos - self
        direction = Direction.get_direction(vector)
        distance = abs(vector)
        if direction in Direction.get_direct_directions() or is_difficult:
            return distance
        return distance // 2

    def get_range_between(self, pos: 'Position') -> Generator['Position', None, None]:
        """
        Returns position range between start and end positions. Start and end positions are excluded to range.
        """
        vector = pos - self
        distance = abs(vector)
        direction = Direction.get_direction(vector)

        if distance % 2 != 0 and direction in Direction.get_diagonal_directions():
            raise ValueError(
                'Positions must be on the same straight line, where between this line and x or y axis '
                'angle is equal to 0, 45, 90 degrees.'
            )

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
