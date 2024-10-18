import math


class Vector:
    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('x and y must be integer.')
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def angle(self) -> float:
        radians = math.atan2(self._x, self._y)
        degrees = math.degrees(radians)
        return degrees

    def __repr__(self):
        return f'<Vector(x:{self._x}, y:{self._x})>'

    def __iter__(self):
        return iter((self._x, self._y))

    def __abs__(self):
        return abs(self._x) + abs(self._y)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y
