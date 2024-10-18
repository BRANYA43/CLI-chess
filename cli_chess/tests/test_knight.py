from unittest.mock import patch

import pytest
from pytest import raises

from errors import PieceError
from objects.enums import Direction
from objects.pieces import Piece, Knight
from objects.position import Position
from tests.conftest import get_position_list


class TestKnight:
    def test_knight_inherits_piece(self):
        assert issubclass(Knight, Piece)

    def test_knight_class_constants(self):
        assert Knight.ALLOWED_MOVE_DIRECTIONS == frozenset(Direction.get_diagonal_directions())
        assert Knight.MAX_MOVE_COUNT == 3

    def test_knight_always_move_3_squares(self, w_knight):
        assert w_knight.check_move_distance(3) is True

        for distance in (2, 4):
            assert w_knight.check_move_distance(distance) is False
            with raises(PieceError, match=rf'Knight cannot move {distance} squares.'):
                w_knight.check_move_distance(distance, raise_exception=True)

    @pytest.mark.parametrize('end', get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]))
    def test_knight_can_get_to_end_position(self, w_knight, board, end):
        """
           0   1   2   3   4
        0 [ ] [x] [ ] [x] [ ]
        1 [x] [ ] [ ] [ ] [x]
        2 [ ] [ ] [N] [ ] [ ]
        3 [x] [ ] [ ] [ ] [x]
        4 [ ] [x] [ ] [x] [ ]
        """
        start = Position(2, 2)
        direction = start.get_direction(end)
        assert w_knight.check_get_to_end_position(start, end, board, _direction=direction) is True

    @pytest.mark.parametrize('end', get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]))
    def test_knight_can_get_to_end_position_through_pieces(self, w_knight, w_piece, board, end):
        """
           0   1   2   3   4
        0 [ ] [x] [ ] [x] [ ]
        1 [x] [P] [P] [P] [x]
        2 [ ] [P] [N] [P] [ ]
        3 [x] [P] [P] [P] [x]
        4 [ ] [x] [ ] [x] [ ]
        """
        start = Position(2, 2)
        for pos in get_position_list([(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]):
            board.add_piece(w_piece, pos)

        direction = start.get_direction(end)
        assert w_knight.check_get_to_end_position(start, end, board, _direction=direction) is True

    @pytest.mark.parametrize('end', get_position_list([(0, 0), (4, 0), (1, 1), (3, 1), (1, 3), (3, 3), (0, 4), (4, 4)]))
    def test_knight_cant_get_to_end_position(self, w_knight, w_pawn, board, end):
        """
           0   1   2   3   4
        0 [x] [ ] [ ] [ ] [x]
        1 [ ] [x] [ ] [x] [ ]
        2 [ ] [ ] [N] [ ] [ ]
        3 [ ] [x] [ ] [x] [ ]
        4 [x] [ ] [ ] [ ] [x]
        """
        start = Position(2, 2)
        direction = start.get_direction(end)
        assert w_knight.check_get_to_end_position(start, end, board, _direction=direction) is False

        with raises(PieceError, match=rf'Knight cannot get from start\({start}\) to end\({end}\) position.'):
            w_knight.check_get_to_end_position(start, end, board, raise_exception=True, _direction=direction)

    @patch.object(Piece, 'check', return_value=True)
    def test_check_method_passed_direction_and_distance_to_kwargs(self, mock_parent_check, w_knight, board):
        start = Position(2, 2)
        end = Position(1, 0)
        assert w_knight.check(start, end, board) is True

        mock_parent_check.assert_called_with(
            start, end, board, None, raise_exception=True, _direction=Direction.UP_LEFT, _distance=3
        )
