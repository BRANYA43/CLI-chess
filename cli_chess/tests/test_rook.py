from objects.enums import Direction
from objects.pieces import Rook, Piece
from objects.position import Position
from tests.conftest import get_position_list


class TestRook:
    def test_rook_inherits_piece(self):
        assert issubclass(Rook, Piece)

    def test_rook_class_constance(self):
        assert Rook.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction.get_direct_directions())
        assert Rook.MAX_MOVE_COUNT == 8

    def test_rook_is_in_stalemate_if_it_is_blocked(self, w_rook, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [P] [ ] [ ]
        2 [ ] [P] [R] [P] [ ]
        3 [ ] [ ] [P] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_rook, start)
        for pos in get_position_list([(2, 1), (1, 2), (3, 2), (2, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_rook.is_in_stalemate(start, board) is True

    def test_rook_isnt_stalemate_if_it_isnt_blocked(self, w_rook, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [R] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_rook, start)

        assert w_rook.is_in_stalemate(start, board) is False

    def test_rook_isnt_stalemate_if_there_is_positions_being_not_blocked(self, w_rook, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [P] [R] [P] [ ]
        3 [ ] [ ] [P] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_rook, start)
        for pos in get_position_list([(1, 2), (3, 2), (2, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_rook.is_in_stalemate(start, board) is False

    def test_rook_isnt_stalemate_if_it_can_attack(self, w_rook, w_pawn, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [p] [ ] [ ]
        2 [ ] [P] [R] [P] [ ]
        3 [ ] [ ] [P] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_rook, start)
        board.add_piece(b_pawn, Position(2, 1))
        for pos in get_position_list([(1, 2), (3, 2), (2, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_rook.is_in_stalemate(start, board) is False
