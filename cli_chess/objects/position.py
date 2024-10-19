from typing import Generator

from objects.enums import Direction
from objects.vector import Vector


class Position:
    __match_args__ = ('x', 'y')

    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError(f'x and y must be integer, but got: x={type(x).__name__}, y={type(y).__name__}.')
        if x < 0 or y < 0:
            raise ValueError(f'Expected x >= 0 and y >= 0, but got x={x} < 0, y={y} < 0.')
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __str__(self):
        return f'x:{self.x}, y:{self.y}'

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return f'<Position(x:{self.x}, y:{self.y})>'

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, vector) -> 'Position':
        if isinstance(vector, Vector):
            return Position(self.x + vector.x, self.y + vector.y)
        raise TypeError(f'Expected Vector, but got {type(vector).__name__}.')

    def __sub__(self, position) -> Vector:
        self.__valid_position(position)
        return Vector(self.x - position.x, self.y - position.y)

    def __eq__(self, position):
        self.__valid_position(position)
        return tuple(self) == tuple(position)

    def __ne__(self, position):
        self.__valid_position(position)
        return self.x != position.x or self.y != position.y

    def __gt__(self, position):
        self.__valid_position(position)
        return self.y > position.y or (self.y == position.y and self.x > position.x)

    def __ge__(self, position):
        self.__valid_position(position)
        return self > position or self == position

    def __lt__(self, position):
        self.__valid_position(position)
        return self.y < position.y or (self.y == position.y and self.x < position.x)

    def __le__(self, position):
        self.__valid_position(position)
        return self < position or self == position

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

        if abs(vector.angle) not in (0.0, 45.0, 90.0, 135.0, 180.0):
            raise ValueError(
                'The angle between the vector of two positions and the x or y axis must be one of the following: '
                '0°, 45°, 90°, 135°, or 180°.'
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
