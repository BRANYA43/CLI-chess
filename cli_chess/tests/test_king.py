import pytest
from pytest_lazy_fixtures import lf

from errors import PieceError
from objects.enums import Direction
from objects.pieces import Piece, King
from objects.position import Position
from tests.conftest import get_position_list

position_as_tuple = tuple[int, int]


class TestKing:
    def test_king_inherits_piece(self):
        assert issubclass(King, Piece)

    def test_king_constants(self):
        assert King.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction)
        assert King.MAX_MOVE_COUNT == 1

    @pytest.mark.parametrize('end', get_position_list([(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]))
    def test_king_can_get_to_end_position_if_it_is_safe(self, w_king, board, end):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [x] [x] [x] [ ]
        2 [ ] [x] [K] [x] [ ]
        3 [ ] [x] [x] [x] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_king, start)
        assert w_king.check_get_to_end_position(start, end, board) is True

    def test_king_can_get_to_end_position_if_end_position_has_enemy_piece(self, w_king, b_queen, board):
        """
           0   1   2   3   4
        0 [K] [q] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(0, 0)
        board.add_piece(w_king, start)
        end = Position(1, 0)
        board.add_piece(b_queen, end)

        assert w_king.check_get_to_end_position(start, end, board) is True

    @pytest.mark.parametrize('end', get_position_list([(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]))
    def test_king_cant_get_to_end_position_if_end_position_is_under_attack(self, w_king, b_rook, board, end):
        """
           0   1   2   3   4
        0 [ ] [r] [ ] [r] [ ]
        1 [r] [x] [x] [x] [ ]
        2 [ ] [x] [K] [x] [ ]
        3 [r] [x] [x] [x] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_king, start)
        for coords in [(1, 0), (3, 0), (0, 1), (0, 3)]:
            board.add_piece(b_rook, Position(*coords))

        assert w_king.check_get_to_end_position(start, end, board) is False

        with pytest.raises(
            PieceError, match=r'King cannot move to the end position that is on attack line of enemy chess piece.'
        ):
            w_king.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_king_cant_get_to_end_position_if_end_position_is_king_back_and_will_be_under_attack(
        self, w_king, b_rook, board
    ):
        """
           0   1   2   3   4
        0 [r] [ ] [K] [x] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 0)
        end = Position(3, 0)
        board.add_piece(b_rook, Position(0, 0))

        assert w_king.check_get_to_end_position(start, end, board) is False

        with pytest.raises(
            PieceError, match=r'King cannot move to the end position that is on attack line of enemy chess piece.'
        ):
            w_king.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_king_cant_get_to_end_position_if_end_position_has_enemy_piece_and_is_on_attack_line_of_another_enemy_piece(
        self, w_king, b_queen, b_rook, board
    ):
        """
           0   1   2   3   4
        0 [K] [q] [r] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(0, 0)
        board.add_piece(w_king, start)
        end = Position(1, 0)
        board.add_piece(b_queen, end)
        board.add_piece(b_rook, Position(2, 0))

        assert w_king.check_get_to_end_position(start, end, board) is False

        with pytest.raises(
            PieceError, match=r'King cannot move to the end position that is on attack line of enemy chess piece.'
        ):
            w_king.check_get_to_end_position(start, end, board, raise_exception=True)

    @pytest.mark.parametrize(
        'piece,check_pos',
        [
            (lf('b_pawn'), Position(3, 3)),
            (lf('b_rook'), Position(2, 0)),
            (lf('b_knight'), Position(1, 0)),
            (lf('b_bishop'), Position(0, 0)),
            (lf('b_queen'), Position(0, 0)),
            (lf('b_queen'), Position(2, 0)),
        ],
    )
    def test_king_is_in_check(self, w_king, board, piece: Piece, check_pos):
        """
           2   3       2        1   2      0   1   2       0   1   2
        2 [K] [ ]   0 [r]    0 [n] [ ]  0 [b] [ ] [ ]   0 [q] [ ] [q]
        3 [ ] [p]   1 [ ]    1 [ ] [ ]  1 [ ] [ ] [ ]   1 [ ] [ ] [ ]
                    2 [K]    2 [ ] [K]  2 [ ] [ ] [K]   2 [ ] [ ] [K]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        board.add_piece(piece, check_pos)

        assert w_king.is_in_check(king_pos, check_pos, piece, board) is True

    @pytest.mark.parametrize(
        'piece,not_check_pos',
        [
            (lf('b_pawn'), Position(2, 3)),
            (lf('b_rook'), Position(1, 0)),
            (lf('b_knight'), Position(2, 0)),
            (lf('b_bishop'), Position(1, 0)),
            (lf('b_queen'), Position(1, 0)),
        ],
    )
    def test_king_isnt_in_check(self, w_king, board, piece, not_check_pos):
        """
           2       1   2       2       1   2       1   2
        2 [K]   0 [r] [ ]   0 [n]   0 [b] [ ]   0 [q] [ ]
        3 [p]   1 [ ] [ ]   1 [ ]   1 [ ] [ ]   1 [ ] [ ]
                2 [ ] [K]   2 [K]   2 [ ] [K]   2 [ ] [K]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        board.add_piece(piece, not_check_pos)
        assert w_king.is_in_check(king_pos, not_check_pos, piece, board) is False

    @pytest.mark.parametrize(
        'piece,check_pos,extra_piece,extra_pos',
        [
            (lf('b_pawn'), Position(3, 3), lf('b_rook'), [(1, 0), (3, 0), (0, 1), (0, 3)]),
            (lf('b_rook'), Position(0, 2), lf('b_rook'), [(0, 1), (0, 3)]),
            (lf('b_knight'), Position(4, 1), lf('b_rook'), [(1, 0), (3, 0), (0, 1), (0, 3)]),
            (lf('b_bishop'), Position(4, 0), lf('b_queen'), [(0, 1), (3, 4)]),
            (lf('b_queen'), Position(2, 0), lf('b_rook'), [(1, 0), (3, 0)]),
        ],
    )
    def test_king_is_in_checkmate(self, w_king, b_rook, board, piece, check_pos, extra_piece, extra_pos):
        """
           0   1   2   3       0   1   2   3       0   1   2   3   4       0   1   2   3   4       1   2   3
        0 [ ] [r] [ ] [r]   1 [r] [ ] [ ] [ ]   0 [ ] [r] [ ] [r] [ ]   0 [ ] [ ] [ ] [ ] [b]   0 [r] [q] [r]
        1 [r] [ ] [ ] [ ]   2 [r] [ ] [K] [ ]   1 [r] [ ] [ ] [ ] [n]   1 [q] [ ] [ ] [ ] [ ]   1 [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ]   3 [r] [ ] [ ] [ ]   2 [ ] [ ] [K] [ ] [ ]   2 [ ] [ ] [K] [ ] [ ]   2 [ ] [K] [ ]
        3 [r] [ ] [ ] [p]                       3 [r] [ ] [ ] [ ] [ ]   3 [ ] [ ] [ ] [ ] [ ]
                                                                        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        board.add_piece(piece, check_pos)

        for pos in get_position_list(extra_pos):
            board.add_piece(extra_piece, pos)

        assert w_king.is_in_checkmate(king_pos, check_pos, piece, board) is True

    @pytest.mark.parametrize(
        'defend_piece,defend_pos,',
        [
            (lf('w_pawn'), Position(4, 2)),
            (lf('w_rook'), Position(2, 3)),
            (lf('w_knight'), Position(4, 2)),
            (lf('w_bishop'), Position(3, 2)),
            (lf('w_queen'), Position(2, 3)),
        ],
    )
    def test_king_is_in_checkmate_if_allied_pawn_cannot_stopped_attack_to_king(
        self, w_king, b_queen, b_bishop, board, defend_piece, defend_pos
    ):
        """
           0   1   2   3   4        0   1   2   3   4        0   1   2   3   4        0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]    0 [ ] [ ] [ ] [ ] [b]    0 [ ] [ ] [ ] [ ] [b]    0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]    1 [q] [ ] [ ] [ ] [ ]    1 [q] [ ] [ ] [ ] [ ]    1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [P]    2 [ ] [ ] [K] [ ] [ ]    2 [ ] [ ] [K] [ ] [N]    2 [ ] [ ] [K] [B] [ ]
        3 [ ] [ ] [ ] [ ] [ ]    3 [ ] [ ] [R] [ ] [ ]    3 [ ] [ ] [ ] [ ] [ ]    3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]    4 [ ] [ ] [ ] [q] [ ]    4 [ ] [ ] [ ] [q] [ ]    4 [ ] [ ] [ ] [q] [ ]

           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [Q] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]

        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(defend_piece, defend_pos)

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for pos in get_position_list([(0, 1), (3, 4)]):
            board.add_piece(b_queen, pos)

        assert w_king.is_in_checkmate(king_pos, check_pos, b_bishop, board) is True

    def test_king_isnt_in_checkmate_if_it_can_attack_piece_that_made_check(self, w_king, b_queen, b_bishop, board):
        """
           0   1   2   3   4
        0 [ ] [q] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [b] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [q]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(3, 1)
        board.add_piece(b_bishop, check_pos)
        for pos in get_position_list([(1, 0), (4, 3)]):
            board.add_piece(b_queen, pos)

        assert w_king.is_in_checkmate(king_pos, check_pos, b_bishop, board) is False

    def test_king_isnt_in_checkmate_if_it_can_flee(self, w_king, b_knight, b_queen, board):
        """
           0   1   2   3   4
        0 [ ] [q] [ ] [n] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [q]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(3, 0)
        board.add_piece(b_knight, check_pos)
        for pos in get_position_list([(1, 0), (4, 3)]):
            board.add_piece(b_queen, pos)

        assert w_king.is_in_checkmate(king_pos, check_pos, b_knight, board) is False

    @pytest.mark.parametrize(
        'defend_piece,defend_pos',
        [
            (lf('w_pawn'), Position(3, 0)),
            (lf('w_rook'), Position(2, 1)),
            (lf('w_knight'), Position(3, 3)),
            (lf('w_bishop'), Position(5, 2)),
            (lf('w_queen'), Position(1, 1)),
        ],
    )
    def test_king_isnt_in_checkmate_if_allied_pawn_can_attack_piece_that_made_the_check(
        self, w_king, b_bishop, b_queen, board, defend_piece, defend_pos
    ):
        """
           0   1   2   3   4       0   1   2   3   4       0   1   2   3   4       0   1   2   3   4   5
        0 [ ] [ ] [ ] [P] [ ]   1 [ ] [ ] [R] [ ] [b]   1 [ ] [ ] [ ] [ ] [b]   1 [ ] [ ] [ ] [ ] [b] [ ]
        1 [ ] [ ] [ ] [ ] [b]   2 [q] [ ] [ ] [ ] [ ]   2 [q] [ ] [ ] [ ] [ ]   2 [q] [ ] [ ] [ ] [ ] [B]
        2 [q] [ ] [ ] [ ] [ ]   3 [ ] [ ] [K] [ ] [ ]   3 [ ] [ ] [K] [N] [ ]   3 [ ] [ ] [K] [ ] [ ] [ ]
        3 [ ] [ ] [K] [ ] [ ]   4 [ ] [ ] [ ] [ ] [ ]   4 [ ] [ ] [ ] [ ] [ ]   4 [ ] [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]   5 [ ] [ ] [ ] [q] [ ]   5 [ ] [ ] [ ] [q] [ ]   5 [ ] [ ] [ ] [q] [ ] [ ]
        5 [ ] [ ] [ ] [q] [ ]

           0   1   2   3   4
        1 [ ] [Q] [ ] [ ] [b]
        2 [q] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [K] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        5 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(defend_piece, defend_pos)

        check_pos = Position(4, 1)
        board.add_piece(b_bishop, check_pos)
        for pos in get_position_list([(0, 2), (3, 5)]):
            board.add_piece(b_queen, pos)

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    @pytest.mark.parametrize(
        'defend_piece,defend_pos',
        [
            (lf('w_pawn'), Position(3, 0)),
            (lf('w_rook'), Position(3, 2)),
            (lf('w_knight'), Position(1, 2)),
            (lf('w_bishop'), Position(4, 2)),
            (lf('w_queen'), Position(2, 1)),
        ],
    )
    def test_king_isnt_in_checkmate_if_allied_pawn_can_stand_on_attack_line_before_king(
        self, w_king, b_bishop, b_queen, board, defend_piece, defend_pos
    ):
        """
           0   1   2   3   4          0   1   2   3   4          0   1   2   3   4          0   1   2   3   4
        0 [ ] [ ] [ ] [P] [b]      0 [ ] [ ] [ ] [ ] [b]      0 [ ] [ ] [ ] [ ] [b]      0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]      1 [q] [ ] [ ] [ ] [ ]      1 [q] [ ] [ ] [ ] [ ]      1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]      2 [ ] [ ] [K] [R] [ ]      2 [ ] [N] [K] [ ] [ ]      2 [ ] [ ] [K] [ ] [B]
        3 [ ] [ ] [ ] [ ] [ ]      3 [ ] [ ] [ ] [ ] [ ]      3 [ ] [ ] [ ] [ ] [ ]      3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]      4 [ ] [ ] [ ] [q] [ ]      4 [ ] [ ] [ ] [q] [ ]      4 [ ] [ ] [ ] [q] [ ]

           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [Q] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(defend_piece, defend_pos)

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_bishop, board) is False
