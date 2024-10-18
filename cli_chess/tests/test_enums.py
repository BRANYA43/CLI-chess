import pytest

from objects.enums import Color, Direction
from objects.vector import Vector

directions_vectors = [
    (Direction.UP, Vector(0, -1)),
    (Direction.DOWN, Vector(0, 1)),
    (Direction.LEFT, Vector(-1, 0)),
    (Direction.RIGHT, Vector(1, 0)),
    (Direction.UP_LEFT, Vector(-1, -1)),
    (Direction.UP_RIGHT, Vector(1, -1)),
    (Direction.DOWN_LEFT, Vector(-1, 1)),
    (Direction.DOWN_RIGHT, Vector(1, 1)),
]


class TestColorEnum:
    def test_enum_member_returns_opposite_color(self):
        assert Color.WHITE.opposite_color == Color.BLACK
        assert Color.BLACK.opposite_color == Color.WHITE


class TestDirectionEnum:
    def test_getting_direct_directions(self):
        expected = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)
        assert Direction.get_direct_directions() == expected

    def test_getting_diagonal_directions(self):
        expected = (Direction.UP_LEFT, Direction.UP_RIGHT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT)
        assert Direction.get_diagonal_directions() == expected

    @pytest.mark.parametrize('direction,vector', directions_vectors)
    def test_getting_direction_by_vector(self, direction, vector):
        assert Direction.get_direction(vector) == direction

    def test_getting_direction_by_vector_raises_error_for_vector_x0_y0(self):
        with pytest.raises(ValueError, match='Impossible determine a direction for x:0 y:0.'):
            Direction.get_direction(Vector(0, 0))

    @pytest.mark.parametrize('direction,vector', directions_vectors)
    def test_vector_property_of_direction(self, direction, vector):
        assert direction.vector == vector
