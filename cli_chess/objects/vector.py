import math


class Vector:
    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError(f'x and y must be integer, but got: x={type(x).__name__}, y={type(y).__name__}.')
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
        radians = math.atan2(*self)
        degrees = math.degrees(radians)
        return degrees

    def __repr__(self):
        return f'<Vector(x:{self.x}, y:{self.x})>'

    def __iter__(self):
        return iter((self.x, self.y))

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, vector):
        if isinstance(vector, Vector):
            return tuple(self) == tuple(vector)
        raise TypeError(f'Expected Vector, but got {type(vector).__name__}.')
