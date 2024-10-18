from unittest.mock import patch

import pytest

from errors import PieceError
from objects.enums import Color, Direction
from objects.pieces import Piece
from objects.position import Position
from tests.conftest import get_position_list


class TestPiece:
    def test_creating_piece(self):
        piece = Piece(Color.WHITE)

        assert piece.color == Color.WHITE

    def test_creating_piece_raises_error_for_invalid_color(self):
        with pytest.raises(ValueError, match=r'2 is not a valid Color'):
            Piece(2)

    def test_name_property_return_name_of_class(self, w_piece):
        class NewPiece(Piece):
            pass

        assert w_piece.name == Piece.__name__
        assert NewPiece(Color.WHITE).name == NewPiece.__name__

    def test_class_constants(self):
        assert Piece.ALLOWED_MOVE_DIRECTIONS == frozenset()
        assert Piece.MAX_MOVE_COUNT == 0

    def test_piece_is_ally_for_another_piece(self, w_piece):
        assert w_piece.is_ally_for(w_piece) is True

    def test_piece_isnt_ally_for_another_piece(self, w_piece, b_piece):
        assert w_piece.is_ally_for(b_piece) is False

    @pytest.mark.parametrize('direction', list(Direction))
    def test_piece_check_move_in_anything_directions(self, direction, w_god_piece):
        assert w_god_piece.check_move_in_direction(direction) is True

    @pytest.mark.parametrize('direction', list(Direction))
    def test_piece_cant_move_in_anything_directions(self, direction, w_piece):
        assert w_piece.check_move_in_direction(direction) is False

    def test_check_move_in_direction_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with pytest.raises(PieceError, match=r'Piece cannot move in the UP direction.'):
            w_piece.check_move_in_direction(Direction.UP, raise_exception=True)

    @pytest.mark.parametrize('distance', range(1, 9))
    def test_piece_check_move_from_1_to_8_squares(self, distance, w_god_piece):
        assert w_god_piece.check_move_distance(distance) is True

    def test_piece_cant_move_less_1_square(self, w_piece):
        assert w_piece.check_move_distance(0) is False

    def test_piece_cant_move_greate_than_8_squares(self, w_god_piece):
        assert w_god_piece.check_move_distance(9) is False

    def test_check_move_distance_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with pytest.raises(PieceError, match=r'Piece cannot move 0 squares.'):
            w_piece.check_move_distance(0, raise_exception=True)

    def test_checking_attack_returns_true_if_piece_attack_no_ally_pieces(self, w_piece, b_piece):
        assert w_piece.check_attack(b_piece) is True

    def test_checking_attack_returns_false_if_piece_attacks_ally_piece(self, w_piece):
        assert w_piece.check_attack(w_piece) is False
        with pytest.raises(PieceError, match=r'Ally pieces cannot attacked each other.'):
            w_piece.check_attack(w_piece, raise_exception=True)

    @pytest.mark.parametrize(
        'end',
        get_position_list(
            [
                (0, 0),
                (2, 0),
                (4, 0),
                (1, 1),
                (2, 1),
                (3, 1),
                (0, 2),
                (1, 2),
                (3, 2),
                (4, 2),
                (1, 3),
                (2, 3),
                (3, 3),
                (0, 4),
                (2, 4),
                (4, 4),
            ]
        ),
    )
    def test_piece_check_get_to_at_end_position(self, w_god_piece, board, end):
        """
           0   1   2   3   4
        0 [x] [ ] [x] [ ] [x]
        1 [ ] [x] [x] [x] [ ]
        2 [x] [x] [#] [x] [x]
        3 [ ] [x] [x] [x] [ ]
        4 [x] [ ] [x] [ ] [x]
        """
        start = Position(2, 2)
        board.add_piece(w_god_piece, start)
        assert w_god_piece.check_get_to_end_position(start, end, board) is True

    @pytest.mark.parametrize(
        'end, blocking_piece_pos',
        list(
            zip(
                get_position_list([(0, 0), (2, 0), (4, 0), (0, 2), (4, 2), (0, 4), (2, 4), (4, 4)]),  # ends
                get_position_list([(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]),  # blocking
            )
        ),
    )
    def test_piece_cant_get_to_end_position_if_there_is_another_piece_on_way(
        self, board, w_piece, w_god_piece, end, blocking_piece_pos
    ):
        """
           0   1   2   3   4
        0 [x] [ ] [x] [ ] [x]
        1 [ ] [p] [p] [p] [ ]
        2 [x] [p] [#] [p] [x]
        3 [ ] [p] [p] [p] [ ]
        4 [x] [ ] [x] [ ] [x]
        """

        start = Position(2, 2)
        board.add_piece(w_god_piece, start)
        board.add_piece(w_piece, blocking_piece_pos)

        assert w_god_piece.check_get_to_end_position(start, end, board) is False
        with pytest.raises(PieceError, match=r'Piece cannot move through another chess piece.'):
            w_god_piece.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_piece_cant_get_to_end_position_if_start_and_end_arent_on_the_same_straight_line(self, board, w_god_piece):
        """
           0   1   2   3   4
        0 [#] [ ] [ ] [ ] [ ]
        1 [ ] [ ] [ ] [ ] [x]
        2 [ ] [ ] [ ] [ ] [ ]
        3 [ ] [ ] [ ] [ ] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(0, 0)
        end = Position(4, 1)
        assert w_god_piece.check_get_to_end_position(start, end, board) is False
        with pytest.raises(PieceError, match=r'Piece cannot get from start\(x:0, y:0\) to end\(x:4, y:1\) position.'):
            w_god_piece.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_check_method_returns_true_without_attacked_piece(self, w_god_piece, board):
        assert w_god_piece.check(Position(0, 0), Position(7, 7), board) is True

    @patch.object(Position, 'get_distance')
    @patch.object(Position, 'get_direction')
    def test_check_method_doesnt_calculate_direction_and_distance_if_they_are_in_kwargs(
        self, mock_direction, mock_distance, w_god_piece, board
    ):
        w_god_piece.check(Position(0, 0), Position(7, 7), board, _direction=Direction.UP, _distance=1)

        mock_direction.assert_not_called()
        mock_distance.assert_not_called()

    def test_check_method_returns_true_with_attacked_piece(self, w_god_piece, b_piece, board):
        assert w_god_piece.check(Position(0, 0), Position(7, 7), board, attacked_piece=b_piece) is True

    def test_check_method_check_raise_all_error_if_raise_exception_is_true(self, w_piece, board):
        start = Position(0, 0)
        end = Position(7, 7)
        board.add_piece(w_piece, Position(1, 1))

        # if attacked piece is the ally
        with pytest.raises(PieceError, match=r'Ally pieces cannot attacked each other.'):
            w_piece.check(start, end, board, w_piece)

        # if piece cannot move in the direction
        with pytest.raises(PieceError, match=r'Piece cannot move in the DOWN RIGHT direction.'):
            w_piece.check(start, end, board)
        w_piece.ALLOWED_MOVE_DIRECTIONS = frozenset([Direction.DOWN_RIGHT])

        # if piece cannot move distance
        with pytest.raises(PieceError, match=r'Piece cannot move 7 squares.'):
            w_piece.check(start, end, board)
        w_piece.MAX_MOVE_COUNT = 8

        # if piece cannot move through another piece
        with pytest.raises(PieceError, match=r'Piece cannot move through another chess piece.'):
            w_piece.check(start, end, board)

    @pytest.mark.parametrize(
        'mock_values, expected_calls',
        [
            (
                {'attack': False, 'direction': None, 'distance': None, 'get': None},
                {'attack': True, 'direction': False, 'distance': False, 'get': False},
            ),  # Test for attack check
            (
                {'attack': None, 'direction': False, 'distance': None, 'get': None},
                {'attack': False, 'direction': True, 'distance': False, 'get': False},
            ),  # Test for direction check
            (
                {'attack': None, 'direction': True, 'distance': False, 'get': None},
                {'attack': False, 'direction': True, 'distance': True, 'get': False},
            ),  # Test for distance check
            (
                {'attack': None, 'direction': True, 'distance': True, 'get': False},
                {'attack': False, 'direction': True, 'distance': True, 'get': True},
            ),  # Test for get-to-end-position check
        ],
    )
    @patch.object(Piece, 'check_get_to_end_position')
    @patch.object(Piece, 'check_move_distance')
    @patch.object(Piece, 'check_move_in_direction')
    @patch.object(Piece, 'check_attack')
    def test_check_method(
        self, mock_attack, mock_direction, mock_distance, mock_get, w_piece, board, mock_values, expected_calls
    ):
        mock_attack.return_value = mock_values['attack']
        mock_direction.return_value = mock_values['direction']
        mock_distance.return_value = mock_values['distance']
        mock_get.return_value = mock_values['get']

        attacked_piece = w_piece if expected_calls['attack'] else None

        assert w_piece.check(Position(0, 0), Position(7, 7), board, attacked_piece) is False

        assert mock_attack.called is expected_calls['attack']
        assert mock_direction.called is expected_calls['direction']
        assert mock_distance.called is expected_calls['distance']
        assert mock_get.called is expected_calls['get']
