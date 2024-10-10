from pytest import raises

from objects.vector import Vector


class TestVector:
    def test_creating_vector(self):
        vector = Vector(-1, 2)
        assert vector.x == -1
        assert vector.y == 2

    def test_creating_vector_raises_error_if_x_or_y_dont_have_int_type(self):
        # invalid "x" type
        with raises(TypeError, match='Expected integer for x, but got str.'):
            Vector('1', 0)

        # invalid "y: type
        with raises(TypeError, match='Expected integer for y, but got str.'):
            Vector(0, '2')

    def test_setting_x_raises_error_if_value_isnt_int_type(self):
        vector = Vector(1, 0)

        assert vector.x == 1

        with raises(TypeError, match='Expected integer for x, but got str.'):
            vector.x = '3'

        assert vector.x == 1

    def test_setting_y_raises_error_if_value_isnt_int_type(self):
        vector = Vector(1, 0)

        assert vector.y == 0

        with raises(TypeError, match='Expected integer for y, but got str.'):
            vector.y = '4'

        assert vector.y == 0

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
