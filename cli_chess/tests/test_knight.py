from unittest.mock import patch

import pytest
from pytest import raises

from errors import InvalidMovePathError, InvalidMoveDistanceError
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
            with raises(InvalidMoveDistanceError):
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

        with raises(InvalidMovePathError):
            w_knight.check_get_to_end_position(start, end, board, raise_exception=True, _direction=direction)

    @patch.object(Piece, 'check', return_value=True)
    def test_check_method_passed_direction_and_distance_to_kwargs(self, mock_parent_check, w_knight, board):
        start = Position(2, 2)
        end = Position(1, 0)
        assert w_knight.check(start, end, board) is True

        mock_parent_check.assert_called_with(
            start, end, board, None, raise_exception=True, _direction=Direction.UP_LEFT, _distance=3
        )

    def test_knight_is_stalemate_if_it_is_blocked_in_middle(self, w_knight, w_pawn, board):
        """
           0   1   2   3   4
        0 [ ] [P] [ ] [P] [ ]
        1 [P] [ ] [ ] [ ] [P]
        2 [ ] [ ] [N] [ ] [ ]
        3 [P] [ ] [ ] [ ] [P]
        4 [ ] [P] [ ] [P] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_knight, start)
        for pos in get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]):
            board.add_piece(w_pawn, pos)

        assert w_knight.is_in_stalemate(start, board) is True

    @pytest.mark.parametrize(
        'start,coords',
        [
            (Position(0, 0), [(2, 1), (1, 2)]),
            (Position(7, 0), [(5, 1), (6, 2)]),
            (Position(0, 7), [(1, 5), (2, 6)]),
            (Position(7, 7), [(6, 5), (5, 6)]),
        ],
    )
    def test_knight_is_stalemate_if_it_is_blocked_in_corners(self, w_knight, w_pawn, board, start, coords):
        """
           0   1   2   .   5   6   7
        0 [N] [ ] [ ] [ ] [ ] [ ] [N]
        1 [ ] [ ] [P] [ ] [P] [ ] [ ]
        2 [ ] [P] [ ] [ ] [ ] [P] [ ]
        . [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        5 [ ] [P] [ ] [ ] [ ] [P] [ ]
        6 [ ] [ ] [P] [ ] [P] [ ] [ ]
        7 [N] [ ] [ ] [ ] [ ] [ ] [N]
        """
        board.add_piece(w_knight, start)
        for coords_ in get_position_list(coords):
            board.add_piece(w_pawn, Position(*coords_))

        assert w_knight.is_in_stalemate(start, board) is True

    @pytest.mark.parametrize(
        'start,coords',
        [
            (Position(0, 2), [(1, 0), (2, 1), (2, 3), (1, 4)]),
            (Position(5, 0), [(3, 1), (4, 2), (6, 2), (7, 1)]),
            (Position(2, 7), [(0, 6), (1, 5), (3, 5), (4, 6)]),
            (Position(7, 5), [(6, 3), (5, 4), (5, 6), (6, 7)]),
        ],
    )
    def test_knight_is_stalemate_if_it_is_blocked_in_edges(self, w_knight, w_pawn, board, start, coords):
        """
           0   1   2       3   4   5   6   7       0   1   2   3   4       5   6   7
        0 [ ] [P] [ ]   0 [ ] [ ] [N] [ ] [ ]   5 [ ] [P] [ ] [P] [ ]   3 [ ] [P] [ ]
        1 [ ] [ ] [P]   1 [P] [ ] [ ] [ ] [P]   6 [P] [ ] [ ] [ ] [P]   4 [P] [ ] [ ]
        2 [N] [ ] [ ]   2 [ ] [P] [ ] [P] [ ]   7 [ ] [ ] [N] [ ] [ ]   5 [ ] [ ] [N]
        3 [ ] [ ] [P]                                                   6 [P] [ ] [ ]
        4 [ ] [P] [ ]                                                   7 [ ] [P] [ ]
        """
        board.add_piece(w_knight, start)
        for coords_ in get_position_list(coords):
            board.add_piece(w_pawn, Position(*coords_))

        assert w_knight.is_in_stalemate(start, board) is True

    @pytest.mark.parametrize(
        'start', get_position_list([(0, 0), (4, 0), (7, 0), (0, 3), (3, 4), (7, 4), (0, 7), (3, 7), (7, 7)])
    )
    def test_knight_isnt_stalemate_if_it_isnt_blocked(self, w_knight, w_pawn, board, start):
        """
           0   1   2   3   4   5   6   7
        0 [N] [ ] [ ] [ ] [N] [ ] [ ] [N]
        1 [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        2 [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        3 [N] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [N] [ ] [ ] [ ] [N]
        5 [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        6 [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
        7 [N] [ ] [ ] [N] [ ] [ ] [ ] [N]
        """
        board.add_piece(w_knight, start)

        assert w_knight.is_in_stalemate(start, board) is False

    @pytest.mark.parametrize(
        'empty_pos', get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)])
    )
    def test_knight_isnt_stalemate_if_there_is_at_least_one_not_blocked_position(
        self, w_knight, w_pawn, b_pawn, board, empty_pos
    ):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [P] [ ]
        1 [P] [ ] [ ] [ ] [P]
        2 [ ] [ ] [N] [ ] [ ]
        3 [P] [ ] [ ] [ ] [P]
        4 [ ] [P] [ ] [P] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_knight, start)
        for pos in get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]):
            if pos != empty_pos:
                board.add_piece(w_pawn, pos)

        assert w_knight.is_in_stalemate(start, board) is False

    @pytest.mark.parametrize(
        'enemy_pos', get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)])
    )
    def test_knight_isnt_stalemate_if_it_can_attack(self, w_knight, w_pawn, b_pawn, board, enemy_pos):
        """
           0   1   2   3   4
        0 [ ] [p] [ ] [P] [ ]
        1 [P] [ ] [ ] [ ] [P]
        2 [ ] [ ] [N] [ ] [ ]
        3 [P] [ ] [ ] [ ] [P]
        4 [ ] [P] [ ] [P] [ ]
        """
        start = Position(2, 2)
        board.add_piece(w_knight, start)
        for pos in get_position_list([(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]):
            if pos == enemy_pos:
                board.add_piece(b_pawn, pos)
            else:
                board.add_piece(w_pawn, pos)

        assert w_knight.is_in_stalemate(start, board) is False
