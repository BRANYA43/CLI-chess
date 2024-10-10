from objects.enums import Color


class TestColorEnum:
    def test_enum_member_returns_opposite_color(self):
        assert Color.WHITE.opposite_color == Color.BLACK
        assert Color.BLACK.opposite_color == Color.WHITE
