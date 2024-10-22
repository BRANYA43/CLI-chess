from objects.enums import Direction
from objects.pieces import Queen, Piece
from objects.position import Position
from tests.conftest import get_position_list


class TestQueen:
    def test_queen_inherits_piece(self):
        assert issubclass(Queen, Piece)

    def test_queen_class_constance(self):
        assert Queen.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction)
        assert Queen.MAX_MOVE_COUNT == 8

    def test_queen_is_in_stalemate_if_it_is_blocked(self, w_queen, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [P] [P] [P] [ ]
        2 [ ] [P] [Q] [P] [ ]
        3 [ ] [P] [P] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_queen, start)
        for pos in get_position_list([(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_queen.is_in_stalemate(start, board) is True

    def test_queen_isnt_stalemate_if_it_isnt_blocked(self, w_queen, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [Q] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_queen, start)

        assert w_queen.is_in_stalemate(start, board) is False

    def test_queen_isnt_stalemate_if_there_is_positions_being_not_blocked(self, w_queen, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [P] [P] [ ]
        2 [ ] [P] [Q] [P] [ ]
        3 [ ] [P] [P] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_queen, start)
        for pos in get_position_list([(2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_queen.is_in_stalemate(start, board) is False

    def test_queen_isnt_stalemate_if_it_can_attack(self, w_queen, w_pawn, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [p] [P] [P] [ ]
        2 [ ] [P] [R] [P] [ ]
        3 [ ] [P] [P] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_queen, start)
        board.add_piece(b_pawn, Position(1, 1))
        for pos in get_position_list([(2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_queen.is_in_stalemate(start, board) is False
