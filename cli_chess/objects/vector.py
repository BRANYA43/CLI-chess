class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'Expected integer for x, but got {type(value).__name__}.')
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'Expected integer for y, but got {type(value).__name__}.')
        self._y = value

    def __iter__(self):
        return iter((self._x, self._y))

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y
