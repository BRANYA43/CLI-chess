import pytest

from objects.vector import Vector


class TestVector:
    def test_creating_vector(self):
        vector = Vector(-1, 2)
        assert vector.x == -1
        assert vector.y == 2

    @pytest.mark.parametrize('x, y', [(None, 1), (1, None)])
    def test_creating_vector_raises_error_if_x_or_y_dont_have_int_type(self, x, y):
        with pytest.raises(
            TypeError, match=rf'x and y must be integer, but got: x={type(x).__name__}, y={type(y).__name__}.'
        ):
            Vector(x, y)

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

    def test_eq_comparing_raises_error_if_second_operand_isnt_vector(self):
        main = Vector(1, 0)
        not_vector = (1, 1)
        with pytest.raises(TypeError, match=r'Expected Vector, but got tuple.'):
            main == not_vector

    @pytest.mark.parametrize('x, y, expected_abs', [(0, 0, 0), (1, 1, 2), (-1, 1, 2), (1, -1, 2), (-1, -1, 2)])
    def test_abs_return_all_positive_integer(self, x, y, expected_abs):
        assert abs(Vector(x, y)) == expected_abs

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
