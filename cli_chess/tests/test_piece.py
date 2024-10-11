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

    def test_piece_can_move_in_anything_directions(self, w_god_piece):
        for direction in Direction:
            assert w_god_piece.can_move_in_direction(direction) is True

    def test_piece_cant_move_in_anything_directions(self, w_piece):
        for direction in Direction:
            assert w_piece.can_move_in_direction(direction) is False

    def test_can_move_in_direction_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with raises(PieceError, match=r'Piece cannot move in the UP direction.'):
            w_piece.can_move_in_direction(Direction.UP, raise_exception=True)

    def test_piece_can_move_from_1_to_8_squares(self, w_god_piece):
        for d in range(1, 9):
            assert w_god_piece.can_move_distance(d) is True

    def test_piece_cant_move_less_1_square(self, w_piece):
        assert w_piece.can_move_distance(0) is False

    def test_piece_cant_move_greate_than_8_squares(self, w_god_piece):
        assert w_god_piece.can_move_distance(9) is False

    def test_can_move_distance_method_raises_error_if_raise_exception_is_true(self, w_piece):
        with raises(PieceError, match=r'Piece cannot move 0 squares.'):
            w_piece.can_move_distance(0, raise_exception=True)

    def test_piece_can_move_through_another_piece(self, w_god_piece):
        assert w_god_piece.can_move_through_another_piece() is True

    def test_piece_cant_move_through_another_piece(self, w_piece):
        assert w_piece.can_move_through_another_piece() is False

    def test_can_move_through_another_piece(self, w_piece):
        with raises(PieceError, match=r'Piece cannot move through another chess piece.'):
            w_piece.can_move_through_another_piece(raise_exception=True)

    def test_check_method_returns_true_without_attacked_piece(self, w_god_piece):
        start = Position(0, 0)
        end = Position(7, 7)
        assert w_god_piece.check(start, end) is True

    def test_check_method_returns_true_with_attacked_piece(self, w_god_piece, b_piece):
        start = Position(0, 0)
        end = Position(7, 7)
        assert w_god_piece.check(start, end, attacked_piece=b_piece) is True

    def test_check_method_can_raise_all_error_if_raise_exception_is_true(self, w_piece):
        start = Position(0, 0)
        end = Position(7, 7)

        # if attacked piece is the ally
        with raises(PieceError, match=r'Ally pieces cannot attacked each other.'):
            w_piece.check(start, end, w_piece)

        # if piece cannot move in the direction
        with raises(PieceError, match=r'Piece cannot move in the DOWN RIGHT direction.'):
            w_piece.check(start, end)
        w_piece.ALLOWED_MOVE_DIRECTIONS = frozenset([Direction.DOWN_RIGHT])

        # if piece cannot move distance
        with raises(PieceError, match=r'Piece cannot move 7 squares.'):
            w_piece.check(start, end)
        w_piece.MAX_MOVE_COUNT = 8

        # if piece cannot move through another piece
        with raises(PieceError, match=r'Piece cannot move through another chess piece.'):
            w_piece.check(start, end)
        w_piece.CAN_MOVE_OR_ATTACK_THROUGH = True

    @patch.object(Piece, 'can_move_through_another_piece')
    @patch.object(Piece, 'can_move_distance')
    @patch.object(Piece, 'can_move_in_direction')
    def test_check_method_doesnt_continue_call_other_method_if_attacked_piece_is_ally(
        self, mock_direction, mock_distance, mock_through, w_piece
    ):
        """
        Piece.can_move_in_direction - wasn't called.
        Piece.can_move_distance - wasn't called.
        Piece.can_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end, w_piece, raise_exception=False) is False

        mock_direction.assert_not_called()
        mock_distance.assert_not_called()
        mock_through.assert_not_called()

    @patch.object(Piece, 'can_move_through_another_piece')
    @patch.object(Piece, 'can_move_distance')
    @patch.object(Piece, 'can_move_in_direction', return_value=False)
    def test_check_method_doesnt_continue_call_other_method_if_first_returns_false(
        self, mock_direction, mock_distance, mock_through, w_piece
    ):
        """
        Piece.can_move_in_direction - returned False.
        Piece.can_move_distance - wasn't called.
        Piece.can_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end) is False

        mock_direction.assert_called()
        mock_distance.assert_not_called()
        mock_through.assert_not_called()

    @patch.object(Piece, 'can_move_through_another_piece')
    @patch.object(Piece, 'can_move_distance', return_value=False)
    @patch.object(Piece, 'can_move_in_direction', return_value=True)
    def test_check_method_doesnt_continue_call_other_method_if_second_returns_false(
        self, mock_direction, mock_distance, mock_through, w_piece
    ):
        """
        Piece.can_move_in_direction - returned True.
        Piece.can_move_distance - returned False.
        Piece.can_move_through_another_piece - wasn't called.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end) is False

        mock_direction.assert_called()
        mock_distance.assert_called()
        mock_through.assert_not_called()

    @patch.object(Piece, 'can_move_through_another_piece', return_value=False)
    @patch.object(Piece, 'can_move_distance', return_value=True)
    @patch.object(Piece, 'can_move_in_direction', return_value=True)
    def test_check_method_doesnt_continue_call_other_method_if_the_last_returns_false(
        self, mock_direction, mock_distance, mock_through, w_piece
    ):
        """
        Piece.can_move_in_direction - returned True.
        Piece.can_move_distance - returned True.
        Piece.can_move_through_another_piece - returned False.
        """
        start = Position(0, 0)
        end = Position(7, 7)

        assert w_piece.check(start, end) is False

        mock_direction.assert_called()
        mock_distance.assert_called()
        mock_through.assert_called()
