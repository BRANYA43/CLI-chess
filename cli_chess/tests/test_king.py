from pytest import raises

from errors import PieceError
from objects.enums import Direction
from objects.pieces import Piece, King
from objects.position import Position

position_as_tuple = tuple[int, int]


class TestKing:
    def test_king_inherits_piece(self):
        assert issubclass(King, Piece)

    def test_king_constants(self):
        assert King.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction)
        assert King.MAX_MOVE_COUNT == 1

    def test_king_can_get_to_end_position_if_it_is_safe(self, w_king, board):
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
        ends = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]

        for coords in ends:
            end = Position(*coords)
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

    def test_king_cant_get_to_end_position_if_end_position_is_under_attack(self, w_king, b_rook, board):
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

        ends = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        for coords in ends:
            end = Position(*coords)
            assert w_king.check_get_to_end_position(start, end, board) is False

            with raises(
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

        with raises(
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

        with raises(
            PieceError, match=r'King cannot move to the end position that is on attack line of enemy chess piece.'
        ):
            w_king.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_king_is_in_check_of_pawn(self, w_king, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [p] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(3, 3)
        board.add_piece(b_pawn, check_pos)

        assert w_king.is_in_check(king_pos, check_pos, b_pawn, board) is True

    def test_king_is_in_check_of_rook(self, w_king, b_rook, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [r] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(2, 0)
        board.add_piece(b_rook, check_pos)

        assert w_king.is_in_check(king_pos, check_pos, b_rook, board) is True

    def test_king_is_in_check_of_knight(self, w_king, b_knight, board):
        """
           0   1   2   3   4
        0 [ ] [n] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(1, 0)
        board.add_piece(b_knight, check_pos)

        assert w_king.is_in_check(king_pos, check_pos, b_knight, board) is True

    def test_king_is_in_check_of_bishop(self, w_king, b_bishop, board):
        """
           0   1   2   3   4
        0 [b] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(0, 0)
        board.add_piece(b_bishop, check_pos)

        assert w_king.is_in_check(king_pos, check_pos, b_bishop, board) is True

    def test_king_is_in_check_of_queen(self, w_king, b_queen, board):
        """
           0   1   2   3   4
        0 [q] [ ] [q] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos_1 = Position(0, 0)
        board.add_piece(b_queen, check_pos_1)

        check_pos_2 = Position(2, 0)
        board.add_piece(b_queen, check_pos_2)

        assert w_king.is_in_check(king_pos, check_pos_1, b_queen, board) is True
        assert w_king.is_in_check(king_pos, check_pos_2, b_queen, board) is True

    def test_king_isnt_in_check_of_pawn(self, w_king, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [p] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        not_check_pos = Position(2, 3)
        board.add_piece(b_pawn, not_check_pos)

        assert w_king.is_in_check(king_pos, not_check_pos, b_pawn, board) is False

    def test_king_isnt_in_check_of_rook(self, w_king, b_rook, board):
        """
           0   1   2   3   4
        0 [ ] [r] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        not_check_pos = Position(1, 0)
        board.add_piece(b_rook, not_check_pos)

        assert w_king.is_in_check(king_pos, not_check_pos, b_rook, board) is False

    def test_king_isnt_in_check_of_knight(self, w_king, b_knight, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [n] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        not_check_pos = Position(2, 0)
        board.add_piece(b_knight, not_check_pos)

        assert w_king.is_in_check(king_pos, not_check_pos, b_knight, board) is False

    def test_king_isnt_in_check_of_bishop(self, w_king, b_bishop, board):
        """
           0   1   2   3   4
        0 [ ] [b] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        not_check_pos = Position(1, 0)
        board.add_piece(b_bishop, not_check_pos)

        assert w_king.is_in_check(king_pos, not_check_pos, b_bishop, board) is False

    def test_king_isnt_in_check_of_queen(self, w_king, b_queen, board):
        """
           0   1   2   3   4
        0 [ ] [q] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        not_check_pos = Position(1, 0)
        board.add_piece(b_queen, not_check_pos)

        assert w_king.is_in_check(king_pos, not_check_pos, b_queen, board) is False

    def test_king_is_in_checkmate_of_pawn(self, w_king, b_rook, b_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [r] [ ] [r] [ ]
        1 [r] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [r] [ ] [ ] [p] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(3, 3)
        board.add_piece(b_pawn, check_pos)

        for coords in [(1, 0), (3, 0), (0, 1), (0, 3)]:
            board.add_piece(b_rook, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_pawn, board) is True

    def test_king_is_in_checkmate_of_rook(self, w_king, b_rook, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [r] [ ] [ ] [ ] [ ]
        2 [r] [ ] [K] [ ] [ ]
        3 [r] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(0, 2)
        board.add_piece(b_rook, check_pos)
        for coords in [(0, 1), (0, 3)]:
            board.add_piece(b_rook, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_rook, board) is True

    def test_king_is_in_checkmate_of_knight(self, w_king, b_rook, b_knight, board):
        """
           0   1   2   3   4
        0 [ ] [r] [ ] [r] [ ]
        1 [r] [ ] [ ] [ ] [n]
        2 [ ] [ ] [K] [ ] [ ]
        3 [r] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(4, 1)
        board.add_piece(b_knight, check_pos)
        for coords in [(1, 0), (3, 0), (0, 1), (0, 3)]:
            board.add_piece(b_rook, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_knight, board) is True

    def test_king_is_in_checkmate_of_bishop(self, w_king, b_queen, b_bishop, board):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_bishop, board) is True

    def test_king_is_in_checkmate_of_queen(self, w_king, b_queen, b_rook, board):
        """
           0   1   2   3   4
        0 [ ] [r] [q] [r] [ ]
        1 [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)

        check_pos = Position(2, 0)
        board.add_piece(b_queen, check_pos)
        for coords in [(1, 0), (3, 0)]:
            board.add_piece(b_rook, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

    def test_king_is_in_checkmate_if_allied_pawn_cannot_stopped_attack_to_king(
        self, w_king, w_pawn, b_queen, b_bishop, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [P]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_pawn, Position(4, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

    def test_king_is_in_checkmate_if_allied_rook_cannot_stopped_attack_to_king(
        self, w_king, w_rook, b_queen, b_bishop, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [r] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_rook, Position(2, 3))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

    def test_king_is_in_checkmate_if_allied_knight_cannot_stopped_attack_to_king(
        self, w_king, w_knight, b_queen, b_bishop, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [N]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_knight, Position(4, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

    #
    def test_king_is_in_checkmate_if_allied_bishop_cannot_stopped_attack_to_king(
        self, w_king, w_bishop, b_queen, b_bishop, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [B] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_bishop, Position(3, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

    def test_king_is_in_checkmate_if_allied_queen_cannot_stopped_attack_to_king(
        self, w_king, w_queen, b_queen, b_bishop, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [Q] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_queen, Position(2, 3))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is True

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
        for coords in [(1, 0), (4, 3)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

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
        for coords in [(1, 0), (4, 3)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_pawn_can_attack_piece_that_made_the_check(
        self, w_king, w_pawn, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [P] [ ]
        1 [ ] [ ] [ ] [ ] [b]
        2 [q] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [K] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        5 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_pawn, Position(3, 0))

        check_pos = Position(4, 1)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 2), (3, 5)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_rook_can_attack_piece_that_made_the_check(
        self, w_king, w_rook, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [R] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_rook, Position(2, 0))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_knight_can_attack_piece_that_made_the_check(
        self, w_king, w_knight, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [N] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_knight, Position(3, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_bishop_can_attack_piece_that_made_the_check(
        self, w_king, w_bishop, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4   5
        0 [ ] [ ] [ ] [ ] [b] [ ]
        1 [q] [ ] [ ] [ ] [ ] [B]
        2 [ ] [ ] [K] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_bishop, Position(5, 1))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_queen_can_attack_piece_that_made_the_check(
        self, w_king, w_queen, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [Q] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_queen, Position(1, 0))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_pawn_can_stand_on_attack_line_before_king(
        self, w_king, w_pawn, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [P] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_pawn, Position(3, 0))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_rook_can_stand_on_attack_line_before_king(
        self, w_king, w_rook, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [R] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_rook, Position(3, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_knight_can_stand_on_attack_line_before_king(
        self, w_king, w_knight, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [N] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_knight, Position(1, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_bishop_can_stand_on_attack_line_before_king(
        self, w_king, w_bishop, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [K] [ ] [B]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_bishop, Position(4, 2))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False

    def test_king_isnt_in_checkmate_if_allied_queen_can_stand_on_attack_line_before_king(
        self, w_king, w_queen, b_bishop, b_queen, board
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [b]
        1 [q] [ ] [Q] [ ] [ ]
        2 [ ] [ ] [K] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [q] [ ]
        """
        king_pos = Position(2, 2)
        board.add_piece(w_king, king_pos)
        board.add_piece(w_queen, Position(2, 1))

        check_pos = Position(4, 0)
        board.add_piece(b_bishop, check_pos)
        for coords in [(0, 1), (3, 4)]:
            board.add_piece(b_queen, Position(*coords))

        assert w_king.is_in_checkmate(king_pos, check_pos, b_queen, board) is False
