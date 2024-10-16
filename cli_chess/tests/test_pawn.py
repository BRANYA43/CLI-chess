from unittest.mock import patch

from pytest import raises

from errors import PieceError
from objects.enums import Color, Direction
from objects.pieces import Pawn, Piece
from objects.position import Position


class TestPawn:
    def test_pawn_inherits_piece(self):
        assert issubclass(Pawn, Piece)

    def test_pawn_constance(self):
        assert Pawn.ALLOWED_MOVE_DIRECTIONS == frozenset()
        assert Pawn.MAX_MOVE_COUNT == 1

    def test_creating_pawn(self):
        w_pawn = Pawn(Color.WHITE)
        assert w_pawn._moved is False
        assert w_pawn.ALLOWED_MOVE_DIRECTIONS == frozenset([Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT])

        b_pawn = Pawn(Color.BLACK)
        assert b_pawn._moved is False
        assert b_pawn.ALLOWED_MOVE_DIRECTIONS == frozenset([Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT])

    def test_is_moved_method_returns_value_from_moved(self, w_pawn):
        assert w_pawn.is_moved() is w_pawn._moved

        w_pawn._moved = True

        assert w_pawn.is_moved() is w_pawn._moved

    def test_doing_first_move_change_moved_value(self, w_pawn):
        assert w_pawn._moved is False

        w_pawn.do_first_move()

        assert w_pawn._moved is True

    def test_pawn_can_move_in_direction_if_it_doesnt_attack(self, w_pawn, b_pawn):
        assert w_pawn.check_move_in_direction(Direction.DOWN) is True
        assert b_pawn.check_move_in_direction(Direction.UP) is True

    def test_pawn_cant_move_in_direction_if_it_attack(self, w_pawn, b_pawn):
        assert w_pawn.check_move_in_direction(Direction.DOWN, is_attack=True) is False
        with raises(PieceError, match=r'Pawn cannot move in the DOWN direction.'):
            w_pawn.check_move_in_direction(Direction.DOWN, is_attack=True, raise_exception=True)

        assert b_pawn.check_move_in_direction(Direction.UP, is_attack=True) is False
        with raises(PieceError, match=r'Pawn cannot move in the UP direction.'):
            b_pawn.check_move_in_direction(Direction.UP, is_attack=True, raise_exception=True)

    def test_pawn_can_attack_in_direction_if_it_attack(self, w_pawn, b_pawn):
        assert w_pawn.check_move_in_direction(Direction.DOWN_LEFT, is_attack=True) is True
        assert w_pawn.check_move_in_direction(Direction.DOWN_RIGHT, is_attack=True) is True
        assert b_pawn.check_move_in_direction(Direction.UP_LEFT, is_attack=True) is True
        assert b_pawn.check_move_in_direction(Direction.UP_RIGHT, is_attack=True) is True

    def test_pawn_cant_attack_in_direction_if_it_doesnt_attack(self, w_pawn, b_pawn):
        assert w_pawn.check_move_in_direction(Direction.DOWN_LEFT) is False
        assert w_pawn.check_move_in_direction(Direction.DOWN_RIGHT) is False
        with raises(PieceError, match=r'Pawn cannot move in the DOWN LEFT direction.'):
            w_pawn.check_move_in_direction(Direction.DOWN_LEFT, raise_exception=True)
        with raises(PieceError, match=r'Pawn cannot move in the DOWN RIGHT direction.'):
            w_pawn.check_move_in_direction(Direction.DOWN_RIGHT, raise_exception=True)

        assert b_pawn.check_move_in_direction(Direction.UP_LEFT) is False
        assert b_pawn.check_move_in_direction(Direction.UP_RIGHT) is False
        with raises(PieceError, match=r'Pawn cannot move in the UP LEFT direction.'):
            b_pawn.check_move_in_direction(Direction.UP_LEFT, raise_exception=True)
        with raises(PieceError, match=r'Pawn cannot move in the UP RIGHT direction.'):
            b_pawn.check_move_in_direction(Direction.UP_RIGHT, raise_exception=True)

    def test_pawn_can_move_2_squares_once_for_only_first_move(self, w_pawn):
        assert w_pawn.is_moved() is False
        assert w_pawn.check_move_distance(2) is True

        w_pawn.do_first_move()

        assert w_pawn.check_move_distance(2) is False
        assert w_pawn.is_moved() is True

    def test_pawn_can_always_move_1_squares(self, w_pawn):
        assert w_pawn.is_moved() is False
        assert w_pawn.check_move_distance(1) is True

        w_pawn.do_first_move()

        assert w_pawn.check_move_distance(1) is True
        assert w_pawn.is_moved() is True

    def test_pawn_can_always_attack_1_squares(self, w_pawn):
        assert w_pawn.is_moved() is False
        assert w_pawn.check_move_distance(2, is_attack=True) is False
        assert w_pawn.check_move_distance(1, is_attack=True) is True

        w_pawn.do_first_move()

        assert w_pawn.is_moved() is True
        assert w_pawn.check_move_distance(2, is_attack=True) is False
        assert w_pawn.check_move_distance(1, is_attack=True) is True

    @patch.object(Piece, 'check', return_value=True)
    def test_check_method_passes_is_attack_arg_as_true_to_parent_check_method(
        self, mock_parent_check, w_pawn, b_pawn, board
    ):
        start = Position(0, 0)
        end = Position(1, 0)
        attacked_piece = b_pawn
        w_pawn.check(start, end, board, attacked_piece)

        mock_parent_check.assert_called_with(start, end, board, attacked_piece, raise_exception=True, is_attack=True)

    @patch.object(Piece, 'check', return_value=True)
    def test_check_method_passes_is_attack_arg_as_false_to_parent_check_method(self, mock_parent_check, w_pawn, board):
        start = Position(0, 0)
        end = Position(1, 0)
        w_pawn.check(start, end, board)

        mock_parent_check.assert_called_with(start, end, board, None, raise_exception=True, is_attack=False)
