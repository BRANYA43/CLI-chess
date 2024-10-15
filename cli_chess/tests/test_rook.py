from objects.enums import Direction
from objects.pieces import Rook, Piece


class TestRook:
    def test_rook_inherits_piece(self):
        assert issubclass(Rook, Piece)

    def test_rook_class_constance(self):
        assert Rook.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction.get_direct_directions())
        assert Rook.MAX_MOVE_COUNT == 8
        assert Rook.CAN_MOVE_OR_ATTACK_THROUGH is False
