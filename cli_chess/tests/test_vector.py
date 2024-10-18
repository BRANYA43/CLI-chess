import pytest
from pytest import raises

from objects.vector import Vector


class TestVector:
    def test_creating_vector(self):
        vector = Vector(-1, 2)
        assert vector.x == -1
        assert vector.y == 2

    def test_creating_vector_raises_error_if_x_or_y_dont_have_int_type(self):
        # invalid "x" type
        with raises(TypeError, match='x and y must be integer.'):
            Vector('1', 0)

        # invalid "y: type
        with raises(TypeError, match='x and y must be integer.'):
            Vector(0, '2')

    def test_vector_is_iterable(self):
        x, y = Vector(100, 200)
        assert x == 100
        assert y == 200

    def test_eq_comparing(self):
        main = Vector(1, 0)
        equal = Vector(1, 0)
        not_equal = Vector(1, 1)

        assert (main == equal) is True
        assert (main == not_equal) is False

    def test_abs_return_all_positive_integer(self):
        for coords in [(0, 0), (1, 1), (-1, 1), (-1, -1)]:
            vector = Vector(*coords)
            assert abs(vector) == abs(vector.x) + abs(vector.y)

    @pytest.mark.parametrize(
        'x, y, expected_angle',
        [
            (0, 0, 0.0),
            (0, 1, 0.0),
            (1, 1, 45.0),
            (1, 0, 90.0),
            (1, -1, 135.0),
            (0, -1, 180.0),
            (-1, -1, -135.0),
            (-1, 0, -90.0),
            (-1, 1, -45.0),
        ],
    )
    def test_angle_property(self, x, y, expected_angle):
        assert Vector(x, y).angle == expected_angle
