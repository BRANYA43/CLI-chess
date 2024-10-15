from collections import ChainMap
from types import MappingProxyType
from unittest.mock import patch

from pytest import raises

from errors import BoardError
from objects.board import Board
from objects.enums import Color
from objects.position import Position


class TestBoard:
    def test_creating_board(self):
        board = Board()
        assert board.pieces_by_color == {Color.WHITE: {}, Color.BLACK: {}}
        assert board._limit_pos == Position(7, 7)

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

        with raises(BoardError, match=r'Cannot add the chess piece, position x:0, y:0 is occupied.'):
            board.add_piece(w_piece, w_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

        with raises(BoardError, match=r'Cannot add the chess piece, position x:1, y:0 is occupied.'):
            board.add_piece(b_piece, b_pos)

        assert w_pos in board.pieces_by_color[Color.WHITE]
        assert w_pos not in board.pieces_by_color[Color.BLACK]
        assert b_pos not in board.pieces_by_color[Color.WHITE]
        assert b_pos in board.pieces_by_color[Color.BLACK]

    def test_adding_piece_raises_error_if_position_out_range_of_board(self, board, w_piece):
        out_limit_pos = Position(8, 8)

        with raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.add_piece(w_piece, out_limit_pos)

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
        empty_pos = Position(0, 0)

        with raises(BoardError, match=r'Cannot remove the chess piece, position x:0, y:0 is empty.'):
            board.remove_piece(w_piece, empty_pos)

    def test_removing_piece_raises_error_if_position_has_another_piece(self, board, w_piece, b_piece):
        b_pos = Position(1, 0)

        board.add_piece(b_piece, b_pos)

        with raises(
            BoardError, match=r'Cannot remove the chess piece, there is a different chess piece at position x:1, y:0.'
        ):
            board.remove_piece(w_piece, b_pos)

    def test_removing_piece_raises_error_if_position_out_range_of_board(self, board, w_piece):
        out_limit_pos = Position(8, 8)

        with raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.remove_piece(w_piece, out_limit_pos)

    def test_getting_piece_by_position(self, board, w_piece, b_piece):
        w_pos = Position(0, 0)
        b_pos = Position(1, 0)

        board.add_piece(w_piece, w_pos)
        board.add_piece(b_piece, b_pos)

        assert board.get_piece(w_pos) is w_piece
        assert board.get_piece(b_pos) is b_piece

    def test_getting_piece_raises_error_if_position_is_empty(self, board):
        empty_pos = Position(0, 0)

        with raises(BoardError, match=r'Cannot get the chess piece, position x:0, y:0 is empty.'):
            board.get_piece(empty_pos)

    def test_getting_piece_raises_error_if_position_out_range_of_board(self, board):
        out_limit_pos = Position(8, 8)

        with raises(BoardError, match=r'x and y cannot be greate then 7.'):
            board.get_piece(out_limit_pos)

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
        start = Position(0, 0)
        end = Position(0, 0)

        with raises(
            BoardError, match=r'Cannot move chess piece, start position x:0, y:0 and end position x:0, y:0 match.'
        ):
            board.move_piece(start, end)

    def test_moving_piece_calls_check_method_of_piece(self, board, w_god_piece):
        start = Position(0, 0)
        end = Position(0, 1)
        board.add_piece(w_god_piece, start)

        with patch.object(w_god_piece, 'check') as mock_check:
            board.move_piece(start, end)

        assert mock_check.called