from collections import ChainMap
from types import MappingProxyType
from unittest.mock import patch

import pytest
from pytest_lazy_fixtures import lf

from errors import BoardError
from objects.board import Board
from objects.enums import Color, Direction
from objects.position import Position


class TestBoard:
    def test_creating_board(self):
        board = Board()
        assert board.pieces_by_color == {Color.WHITE: {}, Color.BLACK: {}}
        assert board.limit_pos == Position(7, 7)
        assert board.moving_pieces_color == Color.WHITE

    def test_pieces_by_color_property_returns_mappingproxytype(self, board, w_piece, b_piece):
        assert isinstance(board.pieces_by_color, MappingProxyType)
        assert isinstance(board.pieces_by_color[Color.WHITE], MappingProxyType)
        assert isinstance(board.pieces_by_color[Color.BLACK], MappingProxyType)

    def test_pieces_property_returns_chain_map(self, board):
        assert isinstance(board.pieces, ChainMap)

    def test_pieces_property_references_to_dictionaries_from_pieces_by_color_variable(self, board, w_piece, b_piece):
        board._pieces_by_color[Color.WHITE][Position(0, 0)] = w_piece
        board._pieces_by_color[Color.BLACK][Position(0, 0)] = b_piece
        assert board.pieces.maps[Color.WHITE] == board._pieces_by_color[Color.WHITE]
        assert board.pieces.maps[Color.BLACK] == board._pieces_by_color[Color.BLACK]

    def test_passing_move_to_other_pieces_of_different_color(self, board):
        assert board.moving_pieces_color == Color.WHITE
        board.pass_move()
        assert board.moving_pieces_color == Color.BLACK
        board.pass_move()
        assert board.moving_pieces_color == Color.WHITE

    def test_having_piece_at_position(self, board, w_piece, b_piece):
        pos_has_w_piece = Position(0, 0)
        pos_has_b_piece = Position(1, 0)
        pos_not_have_piece = Position(2, 0)
        board._pieces_by_color[Color.WHITE][pos_has_w_piece] = w_piece
        board._pieces_by_color[Color.WHITE][pos_has_b_piece] = b_piece
        assert board.has_piece_at_position(pos_has_w_piece) is True
        assert board.has_piece_at_position(pos_has_b_piece) is True
        assert board.has_piece_at_position(pos_not_have_piece) is False

    def test_adding_piece_at_position(self, board, w_piece, b_piece):
        w_pos = Position(0, 0)
        b_pos = Position(1, 0)

        assert w_pos not in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos not in board.pieces_by_color[Color.BLACK]

        board.add_piece(w_piece, w_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos not in board.pieces_by_color[Color.BLACK]

        board.add_piece(b_piece, b_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

    def test_adding_piece_raises_error_if_position_is_occupied_another_piece(self, board, w_piece, b_piece):
        w_pos = Position(0, 0)
        b_pos = Position(1, 0)

        board.add_piece(w_piece, w_pos)
        board.add_piece(b_piece, b_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

        with pytest.raises(BoardError, match=r'Cannot add the chess piece, position x:0, y:0 is occupied.'):
            board.add_piece(w_piece, w_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

        with pytest.raises(BoardError, match=r'Cannot add the chess piece, position x:1, y:0 is occupied.'):
            board.add_piece(b_piece, b_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

    def test_adding_piece_raises_error_if_position_out_range_of_board(self, board, w_piece):
        with pytest.raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.add_piece(w_piece, Position(8, 8))

    def test_removing_piece_at_position(self, board, w_piece, b_piece):
        w_pos = Position(0, 0)
        b_pos = Position(1, 0)

        board.add_piece(w_piece, w_pos)
        board.add_piece(b_piece, b_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

        board.remove_piece(w_piece, w_pos)

        assert w_pos not in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

        board.remove_piece(b_piece, b_pos)

        assert w_pos not in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos not in board.pieces_by_color[Color.BLACK]

    def test_removing_piece_raises_error_if_position_is_empty(self, board, w_piece):
        with pytest.raises(BoardError, match=r'Cannot remove the chess piece, position x:0, y:0 is empty.'):
            board.remove_piece(w_piece, Position(0, 0))

    def test_removing_piece_raises_error_if_position_has_another_piece(self, board, w_piece, b_piece):
        pos = Position(1, 0)
        board.add_piece(b_piece, pos)

        with pytest.raises(
            BoardError, match=r'Cannot remove the chess piece, there is a different chess piece at position x:1, y:0.'
        ):
            board.remove_piece(w_piece, pos)

    def test_removing_piece_raises_error_if_position_out_range_of_board(self, board, w_piece):
        with pytest.raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.remove_piece(w_piece, Position(8, 8))

    def test_getting_piece_by_position(self, board, w_piece, b_piece):
        w_pos = Position(0, 0)
        b_pos = Position(1, 0)

        board.add_piece(w_piece, w_pos)
        board.add_piece(b_piece, b_pos)

        assert board.get_piece(w_pos) is w_piece
        assert board.get_piece(b_pos) is b_piece

    def test_getting_piece_returns_none(self, board):
        assert board.get_piece(Position(0, 0)) is None

    def test_getting_piece_raises_error_if_position_out_range_of_board(self, board):
        with pytest.raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.get_piece(Position(8, 8))

    def test_moving_piece_from_start_to_end_positions(self, board, w_god_piece, b_god_piece):
        w_start = Position(0, 0)
        b_start = Position(1, 0)
        w_end = Position(0, 1)

        board.add_piece(w_god_piece, w_start)
        board.add_piece(b_god_piece, b_start)

        assert w_start in board.pieces_by_color[Color.WHITE]
        assert w_end not in board.pieces_by_color[Color.WHITE]
        assert w_start not in board.pieces_by_color[Color.BLACK]
        assert w_end not in board.pieces_by_color[Color.BLACK]

        assert b_start in board.pieces_by_color[Color.BLACK]
        assert b_start not in board.pieces_by_color[Color.WHITE]

        board.move_piece(w_start, w_end)

        assert w_start not in board.pieces_by_color[Color.WHITE]
        assert w_end in board.pieces_by_color[Color.WHITE]
        assert w_start not in board.pieces_by_color[Color.BLACK]
        assert w_end not in board.pieces_by_color[Color.BLACK]

        assert b_start in board.pieces_by_color[Color.BLACK]
        assert b_start not in board.pieces_by_color[Color.WHITE]

    def test_moving_piece_from_start_position_to_end_positions_if_end_position_has_enemy_piece(
        self, board, w_god_piece, b_piece
    ):
        start = Position(0, 0)
        end = Position(1, 0)

        board.add_piece(w_god_piece, start)
        board.add_piece(b_piece, end)

        assert start in board.pieces_by_color[Color.WHITE]
        assert end not in board.pieces_by_color[Color.WHITE]
        assert start not in board.pieces_by_color[Color.BLACK]
        assert end in board.pieces_by_color[Color.BLACK]

        board.move_piece(start, end)

        assert start not in board.pieces_by_color[Color.WHITE]
        assert end in board.pieces_by_color[Color.WHITE]
        assert start not in board.pieces_by_color[Color.BLACK]
        assert end not in board.pieces_by_color[Color.BLACK]

        assert board._pieces_by_color[Color.BLACK] == {}

    def test_moving_piece_raises_error_if_start_and_end_positions_is_match(self, board):
        pos = Position(0, 0)
        with pytest.raises(
            BoardError, match=r'Cannot move chess piece, start position x:0, y:0 and end position x:0, y:0 match.'
        ):
            board.move_piece(pos, pos)

    def test_moving_piece_calls_check_method_of_piece(self, board, w_god_piece):
        start = Position(0, 0)
        end = Position(0, 1)
        board.add_piece(w_god_piece, start)

        with patch.object(w_god_piece, 'check') as mock_check:
            board.move_piece(start, end)

        assert mock_check.called

    @pytest.mark.parametrize(
        'pos',
        [Position(x, y) for y in range(2) for x in range(8)] + [Position(x, y) for x in range(2) for y in range(8)],
    )
    @pytest.mark.parametrize(
        'piece', (lf(piece) for piece in ('w_pawn', 'b_pawn', 'w_rook', 'w_knight', 'w_bishop', 'w_queen'))
    )
    def test_getting_possible_directions_returns_expected_directions(self, pos, board, piece):
        possible_directions = board.get_possible_directions(pos, piece)
        allowed_directions = piece.ALLOWED_MOVE_DIRECTIONS
        expected = set(Direction)
        match pos:
            case Position(0, 0):
                expected = {Direction.DOWN, Direction.RIGHT, Direction.DOWN_RIGHT}
            case Position(7, 0):
                expected = {Direction.DOWN, Direction.LEFT, Direction.DOWN_LEFT}
            case Position(0, 7):
                expected = {Direction.UP, Direction.RIGHT, Direction.UP_RIGHT}
            case Position(7, 7):
                expected = {Direction.UP, Direction.LEFT, Direction.UP_LEFT}
            case Position(0, _):
                expected = {Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.UP_RIGHT, Direction.DOWN_RIGHT}
            case Position(7, _):
                expected = {Direction.UP, Direction.DOWN, Direction.LEFT, Direction.UP_LEFT, Direction.DOWN_LEFT}
            case Position(_, 0):
                expected = {Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT}
            case Position(_, 7):
                expected = {Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.UP_LEFT, Direction.UP_RIGHT}
            case Position(_, _):
                pass

        assert possible_directions == expected & allowed_directions

    def test_white_pieces_is_in_stalemate_and_black_not(self, w_piece, b_queen, board):
        """
           0   1   2
        0 [P] [ ] [ ]
        1 [q] [ ] [ ]
        2 [ ] [ ] [ ]
        """
        board.add_piece(w_piece, Position(0, 0))
        board.add_piece(b_queen, Position(0, 1))

        assert board.moving_pieces_color == Color.WHITE
        assert board.check_stalemate() is True
        board.pass_move()
        assert board.moving_pieces_color == Color.BLACK
        assert board.check_stalemate() is False
