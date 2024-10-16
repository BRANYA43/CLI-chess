from objects.enums import Direction
from objects.pieces import Bishop, Piece


class TestBishop:
    def test_bishop_inherits_piece(self):
        assert issubclass(Bishop, Piece)

    def test_bishop_class_constance(self):
        assert Bishop.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction.get_diagonal_directions())
        assert Bishop.MAX_MOVE_COUNT == 8
