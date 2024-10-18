from unittest.mock import patch

import pytest
from pytest_lazy_fixtures import lf

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

    @pytest.mark.parametrize(
        'pawn,direction',
        [(lf('w_pawn'), Direction.DOWN), (lf('b_pawn'), Direction.UP)],
    )
    def test_pawn_cant_move_in_direction_if_it_attack(self, pawn, direction):
        assert pawn.check_move_in_direction(direction, is_attack=True) is False
        with pytest.raises(PieceError, match=rf'Pawn cannot move in the {direction} direction.'):
            pawn.check_move_in_direction(direction, is_attack=True, raise_exception=True)

    @pytest.mark.parametrize(
        'pawn,directions',
        [
            (lf('w_pawn'), [Direction.DOWN_LEFT, Direction.DOWN_RIGHT]),
            (lf('b_pawn'), [Direction.UP_LEFT, Direction.UP_RIGHT]),
        ],
    )
    def test_pawn_can_attack_in_direction_if_it_attack(self, pawn, directions, w_pawn, b_pawn):
        for direction in directions:
            assert pawn.check_move_in_direction(direction, is_attack=True) is True

    @pytest.mark.parametrize(
        'pawn,directions',
        [
            (lf('w_pawn'), [Direction.DOWN_LEFT, Direction.DOWN_RIGHT]),
            (lf('b_pawn'), [Direction.UP_LEFT, Direction.UP_RIGHT]),
        ],
    )
    def test_pawn_cant_attack_in_direction_if_it_doesnt_attack(self, pawn, directions, w_pawn, b_pawn):
        for direction in directions:
            assert pawn.check_move_in_direction(direction) is False
            with pytest.raises(PieceError, match=rf'Pawn cannot move in the {direction} direction.'):
                pawn.check_move_in_direction(direction, raise_exception=True)

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
        w_pawn.check(start, end, board, b_pawn)

        mock_parent_check.assert_called_with(start, end, board, b_pawn, raise_exception=True, is_attack=True)

    @patch.object(Piece, 'check', return_value=True)
    def test_check_method_passes_is_attack_arg_as_false_to_parent_check_method(self, mock_parent_check, w_pawn, board):
        start = Position(0, 0)
        end = Position(1, 0)
        w_pawn.check(start, end, board)

        mock_parent_check.assert_called_with(start, end, board, None, raise_exception=True, is_attack=False)
