from objects.enums import Direction
from objects.pieces import Queen, Piece


class TestQueen:
    def test_queen_inherits_piece(self):
        assert issubclass(Queen, Piece)

    def test_queen_class_constance(self):
        assert Queen.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction)
        assert Queen.MAX_MOVE_COUNT == 8
