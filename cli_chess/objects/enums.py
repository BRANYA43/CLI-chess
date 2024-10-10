from enum import IntEnum


class Color(IntEnum):
    WHITE = 0
    BLACK = 1

    @property
    def opposite_color(self) -> 'Color':
        return Color.BLACK if self == Color.WHITE else Color.WHITE
