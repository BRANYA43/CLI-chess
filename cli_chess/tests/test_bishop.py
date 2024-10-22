from objects.enums import Direction
from objects.pieces import Bishop, Piece
from objects.position import Position
from tests.conftest import get_position_list


class TestBishop:
    def test_bishop_inherits_piece(self):
        assert issubclass(Bishop, Piece)

    def test_bishop_class_constance(self):
        assert Bishop.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction.get_diagonal_directions())
        assert Bishop.MAX_MOVE_COUNT == 8

    def test_bishop_is_in_stalemate_if_it_is_blocked(self, w_bishop, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [P] [ ] [P] [ ]
        2 [ ] [ ] [B] [ ] [ ]
        3 [ ] [P] [ ] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_bishop, start)
        for pos in get_position_list([(1, 1), (3, 1), (1, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_bishop.is_in_stalemate(start, board) is True

    def test_bishop_isnt_stalemate_if_it_isnt_blocked(self, w_bishop, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [B] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_bishop, start)

        assert w_bishop.is_in_stalemate(start, board) is False

    def test_bishop_isnt_stalemate_if_there_is_positions_being_not_blocked(self, w_bishop, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [P] [ ]
        2 [ ] [ ] [B] [ ] [ ]
        3 [ ] [P] [ ] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_bishop, start)
        for pos in get_position_list([(3, 1), (1, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_bishop.is_in_stalemate(start, board) is False

    def test_bishop_isnt_stalemate_if_it_can_attack(self, w_bishop, w_pawn, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [p] [ ] [P] [ ]
        2 [ ] [ ] [R] [ ] [ ]
        3 [ ] [P] [ ] [P] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_bishop, start)
        board.add_piece(b_pawn, Position(1, 1))
        for pos in get_position_list([(3, 1), (1, 3), (3, 3)]):
            board.add_piece(w_pawn, pos)

        assert w_bishop.is_in_stalemate(start, board) is False
