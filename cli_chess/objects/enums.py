from enum import IntEnum

from objects.vector import Vector


class Color(IntEnum):
    WHITE = 0
    BLACK = 1

    @property
    def opposite_color(self) -> 'Color':
        return Color.BLACK if self == Color.WHITE else Color.WHITE

    def __str__(self):
        return self.name


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7

    def __str__(self):
        return self.name.replace('_', ' ')

    @classmethod
    def get_direct_directions(cls) -> tuple['Direction', 'Direction', 'Direction', 'Direction']:
        return Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT

    @classmethod
    def get_diagonal_directions(cls) -> tuple['Direction', 'Direction', 'Direction', 'Direction']:
        return Direction.UP_LEFT, Direction.UP_RIGHT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT

    @classmethod
    def get_direction(cls, vector: Vector) -> 'Direction':
        x, y = vector
        if x == 0:
            if y > 0:
                return Direction.DOWN
            elif y < 0:
                return Direction.UP
        elif x > 0:
            if y == 0:
                return Direction.RIGHT
            elif y > 0:
                return Direction.DOWN_RIGHT
            elif y < 0:
                return Direction.UP_RIGHT
        elif x < 0:
            if y == 0:
                return Direction.LEFT
            elif y > 0:
                return Direction.DOWN_LEFT
            elif y < 0:
                return Direction.UP_LEFT
        raise ValueError('Impossible determine a direction for x:0 y:0.')

    @property
    def vector(self) -> Vector:
        vectors = {
            Direction.UP: Vector(0, -1),
            Direction.DOWN: Vector(0, 1),
            Direction.LEFT: Vector(-1, 0),
            Direction.RIGHT: Vector(1, 0),
            Direction.UP_LEFT: Vector(-1, -1),
            Direction.UP_RIGHT: Vector(1, -1),
            Direction.DOWN_LEFT: Vector(-1, 1),
            Direction.DOWN_RIGHT: Vector(1, 1),
        }
        return vectors[self]
