from unittest.mock import patch

from pytest import raises

from errors import PieceError
from objects.enums import Color, Direction
from objects.pieces import Piece
from objects.position import Position


class TestPiece:
    def test_creating_piece(self):
        piece = Piece(Color.WHITE)

        assert piece.color == Color.WHITE

    def test_creating_piece_raises_error_for_invalid_color(self):
        with raises(ValueError, match=r'2 is not a valid Color'):
            Piece(2)

    def test_name_property_return_name_of_class(self, w_piece):
        class NewPiece(Piece):
            pass

        assert w_piece.name == Piece.__name__
        assert NewPiece(Color.WHITE).name == NewPiece.__name__

    def test_class_constants(self):
        assert Piece.ALLOWED_MOVE_DIRECTIONS == frozenset()
        assert Piece.MAX_MOVE_COUNT == 0
        assert Piece.CAN_MOVE_OR_ATTACK_THROUGH is False

    def test_piece_is_ally_for_another_piece(self, w_piece):
        assert w_piece.is_ally_for(w_piece) is True

    def test_piece_isnt_ally_for_another_piece(self, w_piece, b_piece):
        assert w_piece.is_ally_for(b_piece) is False

    def test_piece_check_move_in_anything_directions(self, w_god_piece):
        for direction in Direction:
            assert w_god_piece.check_move_in_direction(direction) is True

    def test_piece_cant_move_in_anything_directions(self, w_piece):
        for direction in Direction:
            assert w_piece.check_move_in_direction(direction) is False

    def test_check_move_in_direction_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with raises(PieceError, match=r'Piece cannot move in the UP direction.'):
            w_piece.check_move_in_direction(Direction.UP, raise_exception=True)

    def test_piece_check_move_from_1_to_8_squares(self, w_god_piece):
        for d in range(1, 9):
            assert w_god_piece.check_move_distance(d) is True

    def test_piece_cant_move_less_1_square(self, w_piece):
        assert w_piece.check_move_distance(0) is False

    def test_piece_cant_move_greate_than_8_squares(self, w_god_piece):
        assert w_god_piece.check_move_distance(9) is False

    def test_check_move_distance_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with raises(PieceError, match=r'Piece cannot move 0 squares.'):
            w_piece.check_move_distance(0, raise_exception=True)

    def test_piece_check_get_to_at_end_position(self, w_god_piece, board):
        """
           0   1   2   3   4
        0 [x] [ ] [x] [ ] [x]
        1 [ ] [x] [x] [x] [ ]
        2 [x] [x] [#] [x] [x]
        3 [ ] [x] [x] [x] [ ]
        4 [x] [ ] [x] [ ] [x]
        """
        w_god_piece.CAN_MOVE_OR_ATTACK_THROUGH = False
        coords = [
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
        start = Position(2, 2)
        board.add_piece(w_god_piece, start)
        for x, y in coords:
            end = Position(x, y)
            assert w_god_piece.check_get_to_end_position(start, end, board) is True

    def test_piece_check_get_to_end_position_if_there_is_another_piece_on_way_and_it_check_move_through_another_piece(
        self, board, w_piece, w_god_piece
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

        blocking_piece_coords = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        for x, y in blocking_piece_coords:
            pos = Position(x, y)
            board.add_piece(w_piece, pos)

        coords = [(0, 0), (2, 0), (4, 0), (0, 2), (4, 2), (0, 4), (2, 4), (4, 4)]
        for x, y in coords:
            end = Position(x, y)
            assert w_god_piece.check_get_to_end_position(start, end, board) is True

    def test_piece_cant_get_to_end_position_if_there_is_another_piece_on_way(self, board, w_piece, w_god_piece):
        """
           0   1   2   3   4
        0 [x] [ ] [x] [ ] [x]
        1 [ ] [p] [p] [p] [ ]
        2 [x] [p] [#] [p] [x]
        3 [ ] [p] [p] [p] [ ]
        4 [x] [ ] [x] [ ] [x]
        """
        w_god_piece.CAN_MOVE_OR_ATTACK_THROUGH = False

        start = Position(2, 2)
        board.add_piece(w_god_piece, start)

        blocking_piece_coords = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        for x, y in blocking_piece_coords:
            pos = Position(x, y)
            board.add_piece(w_piece, pos)

        coords = [(0, 0), (2, 0), (4, 0), (0, 2), (4, 2), (0, 4), (2, 4), (4, 4)]
        for x, y in coords:
            end = Position(x, y)
            assert w_god_piece.check_get_to_end_position(start, end, board) is False
            with raises(PieceError, match=r'Piece cannot move through another chess piece.'):
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
        w_god_piece.CAN_MOVE_OR_ATTACK_THROUGH = False
        start = Position(0, 0)
        end = Position(4, 1)
        assert w_god_piece.check_get_to_end_position(start, end, board) is False
        with raises(PieceError, match=r'Piece cannot get from start\(x:0, y:0\) to end\(x:4, y:1\) position.'):
            w_god_piece.check_get_to_end_position(start, end, board, raise_exception=True)

    def test_check_method_returns_true_without_attacked_piece(self, w_god_piece, board):
        start = Position(0, 0)
        end = Position(7, 7)
        assert (
            w_god_piece.check(
                start,
                end,
                board,
            )
            is True
        )

    def test_check_method_returns_true_with_attacked_piece(self, w_god_piece, b_piece, board):
        start = Position(0, 0)
        end = Position(7, 7)
        assert w_god_piece.check(start, end, board, attacked_piece=b_piece) is True

    def test_check_method_check_raise_all_error_if_raise_exception_is_true(self, w_piece, board):
        start = Position(0, 0)
        end = Position(7, 7)
        board.add_piece(w_piece, Position(1, 1))

        # if attacked piece is the ally
        with raises(PieceError, match=r'Ally pieces cannot attacked each other.'):
            w_piece.check(start, end, board, w_piece)

        # if piece cannot move in the direction
        with raises(PieceError, match=r'Piece cannot move in the DOWN RIGHT direction.'):
            w_piece.check(start, end, board)
        w_piece.ALLOWED_MOVE_DIRECTIONS = frozenset([Direction.DOWN_RIGHT])

        # if piece cannot move distance
        with raises(PieceError, match=r'Piece cannot move 7 squares.'):
            w_piece.check(start, end, board)
        w_piece.MAX_MOVE_COUNT = 8

        # if piece cannot move through another piece
        with raises(PieceError, match=r'Piece cannot move through another chess piece.'):
            w_piece.check(start, end, board)

    @patch.object(Piece, 'check_get_to_end_position')
    @patch.object(Piece, 'check_move_distance')
    @patch.object(Piece, 'check_move_in_direction')
    def test_check_method_doesnt_continue_call_other_method_if_attacked_piece_is_ally(
        self, mock_direction, mock_distance, mock_get, w_piece, board
    ):
        """
        Piece.check_move_in_direction - wasn't called.
        Piece.check_move_distance - wasn't called.
        Piece.check_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end, board, w_piece, raise_exception=False) is False

        mock_direction.assert_not_called()
        mock_distance.assert_not_called()
        mock_get.assert_not_called()

    @patch.object(Piece, 'check_get_to_end_position')
    @patch.object(Piece, 'check_move_distance')
    @patch.object(Piece, 'check_move_in_direction', return_value=False)
    def test_check_method_doesnt_continue_call_other_method_if_first_returns_false(
        self, mock_direction, mock_distance, mock_got, w_piece, board
    ):
        """
        Piece.check_move_in_direction - returned False.
        Piece.check_move_distance - wasn't called.
        Piece.check_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end, board) is False

        mock_direction.assert_called()
        mock_distance.assert_not_called()
        mock_got.assert_not_called()

    @patch.object(Piece, 'check_get_to_end_position')
    @patch.object(Piece, 'check_move_distance', return_value=False)
    @patch.object(Piece, 'check_move_in_direction', return_value=True)
    def test_check_method_doesnt_continue_call_other_method_if_second_returns_false(
        self, mock_direction, mock_distance, mock_got, w_piece, board
    ):
        """
        Piece.check_move_in_direction - returned True.
        Piece.check_move_distance - returned False.
        Piece.check_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end, board) is False

        mock_direction.assert_called()
        mock_distance.assert_called()
        mock_got.assert_not_called()

    @patch.object(Piece, 'check_get_to_end_position', return_value=False)
    @patch.object(Piece, 'check_move_distance', return_value=True)
    @patch.object(Piece, 'check_move_in_direction', return_value=True)
    def test_check_method_doesnt_continue_call_other_method_if_the_last_returns_false(
        self, mock_direction, mock_distance, mock_got, w_piece, board
    ):
        """
        Piece.check_move_in_direction - returned True.
        Piece.check_move_distance - returned True.
        Piece.check_move_through_another_piece - returned False.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end, board) is False

        mock_direction.assert_called()
        mock_distance.assert_called()
        mock_got.assert_called()
