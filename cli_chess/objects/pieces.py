from collections import deque
from typing import Optional, override

from errors import (
    AllyAttackError,
    InvalidMoveDirectionError,
    BlockedMoveError,
    InvalidMovePathError,
    InvalidMoveDistanceError,
    PieceError,
)
from objects.enums import Color, Direction
from objects.position import Position
from functools import partial

from objects.vector import Vector


class Piece:
    """Base class of all chess pieces"""

    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset()

    MAX_MOVE_COUNT = 0

    def __init__(self, color: int):
        self._color = Color(color)

    def __str__(self):
        return f'{self.color.name.title()} {self.name}'

    def __repr__(self):
        return f'{self.name}(id:{id(self)}, color:{self.color})'

    @property
    def color(self) -> Color:
        return self._color

    @property
    def name(self) -> str:
        return type(self).__name__

    def is_ally_for(self, piece: 'Piece') -> bool:
        return self.color == piece.color

    def check(
        self,
        start: Position,
        end: Position,
        board,
        attacked_piece: Optional['Piece'] = None,
        *,
        raise_exception=True,
        **kwargs,
    ) -> bool:
        """
        Checks whether the chess piece moves from the start position to the end position.
        :keyword diagonal_direction: if True then it considers diagonal directions (e.g. Bishop, Queen).
        """
        if (direction := kwargs.get('_direction')) is None:
            direction = start.get_direction(end)
        if (distance := kwargs.get('_distance')) is None:
            distance = start.get_distance(end)

        check_methods = deque(
            [
                partial(self.check_move_in_direction, direction, raise_exception=raise_exception, **kwargs),
                partial(self.check_move_distance, distance, raise_exception=raise_exception, **kwargs),
                partial(self.check_get_to_end_position, start, end, board, raise_exception=raise_exception, **kwargs),
            ]
        )
        if attacked_piece is not None:
            check_methods.appendleft(partial(self.check_attack, attacked_piece, raise_exception=raise_exception))

        for check in check_methods:
            if not check():
                return False
        return True

    def check_attack(self, attacked_piece: 'Piece', *, raise_exception=False) -> bool:
        """
        Checks whether the chess piece attack the ally chess piece.
        """
        if self.is_ally_for(attacked_piece):
            if raise_exception:
                raise AllyAttackError
            return False
        return True

    def check_move_in_direction(self, direction: Direction, *, raise_exception=False, **kwargs) -> bool:
        """
        Checks whether the chess piece can move in a direction.
        """
        result = direction in self.ALLOWED_MOVE_DIRECTIONS
        if raise_exception and not result:
            raise InvalidMoveDirectionError(name=self.name, direction=direction)
        return result

    def check_get_to_end_position(
        self, start: Position, end: Position, board, *, raise_exception=False, **kwargs
    ) -> bool:
        """
        Checks whether the chess piece can get from the start to the end position.
        """
        try:
            for next_pos in start.get_range_between(end):
                if board.has_piece_at_position(next_pos):
                    maybe_enemy_king = board.get_piece(next_pos)
                    if (
                        isinstance(maybe_enemy_king, King)
                        and maybe_enemy_king.color != self.color
                        and next_pos.get_distance(end) == 1
                        and maybe_enemy_king.is_in_check(next_pos, start, self, board)
                    ):
                        continue

                    if raise_exception:
                        raise BlockedMoveError(name=self.name)
                    return False
        except ValueError:
            if raise_exception:
                raise InvalidMovePathError(name=self.name, start=start, end=end)
            return False

        return True

    def check_move_distance(self, distance: int, *, raise_exception=False, **kwargs) -> bool:
        """
        Checks whether the chess piece can move the distance of squares.
        """
        result = 1 <= distance <= self.MAX_MOVE_COUNT
        if raise_exception and not result:
            raise InvalidMoveDistanceError(name=self.name, distance=distance, max_moves=self.MAX_MOVE_COUNT)
        return result

    def is_in_stalemate(self, start: Position, board) -> bool:
        """
        Returns True, if piece is in stalemate, else False.
        """
        excluded_directions: set[Direction] = set()
        possible_directions = board.get_possible_directions(start, self)
        for _ in range(self.MAX_MOVE_COUNT):
            if excluded_directions:
                possible_directions -= excluded_directions
                excluded_directions = set()

            for direction in possible_directions:
                try:
                    next_pos = start + direction.vector
                except ValueError:
                    excluded_directions.add(direction)
                    continue

                if next_pos > board.limit_pos:
                    excluded_directions.add(direction)
                    continue

                attacked_piece = board.get_piece(next_pos)

                try:
                    if self.check(start, next_pos, self, attacked_piece):
                        return False
                except BlockedMoveError:
                    excluded_directions.add(direction)
                except PieceError:
                    pass
        return True


class Pawn(Piece):
    MAX_MOVE_COUNT = 1

    def __init__(self, color: Color):
        super().__init__(color)
        self._moved = False

        if self.color == Color.WHITE:
            self.ALLOWED_MOVE_DIRECTIONS = frozenset([Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT])
        else:
            self.ALLOWED_MOVE_DIRECTIONS = frozenset([Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT])

    def is_moved(self) -> bool:
        return self._moved

    def do_first_move(self):
        self._moved = True

    @override
    def check_move_in_direction(
        self, direction: Direction, *, raise_exception=False, is_attack=False, **kwargs
    ) -> bool:
        result = super().check_move_in_direction(direction, raise_exception=raise_exception, **kwargs)
        if direction in Direction.get_diagonal_directions():
            result = is_attack and result
        else:
            result = not is_attack and result

        if not result and raise_exception:
            raise InvalidMoveDirectionError(name=self.name, direction=direction)
        return result

    @override
    def check_move_distance(self, distance: int, *, raise_exception=False, is_attack=False, **kwargs) -> bool:
        if not is_attack and not self._moved and distance <= 2:
            return True
        return super().check_move_distance(distance, raise_exception=raise_exception, **kwargs)

    @override
    def check(
        self,
        start: Position,
        end: Position,
        board,
        attacked_piece: Optional['Piece'] = None,
        *,
        raise_exception=True,
        **kwargs,
    ) -> bool:
        return super().check(
            start, end, board, attacked_piece, raise_exception=raise_exception, is_attack=bool(attacked_piece), **kwargs
        )


class Rook(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction.get_direct_directions())

    MAX_MOVE_COUNT = 8


class Knight(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction.get_diagonal_directions())

    MAX_MOVE_COUNT = 3

    @override
    def check_move_distance(self, distance: int, *, raise_exception=False, **kwargs) -> bool:
        result = distance == self.MAX_MOVE_COUNT
        if raise_exception and not result:
            raise InvalidMoveDistanceError(name=self.name, distance=distance, max_moves=self.MAX_MOVE_COUNT)
        return result

    def check_get_to_end_position(
        self, start: Position, end: Position, board, *, raise_exception=False, **kwargs
    ) -> bool:
        vector = kwargs['_direction'].vector
        l_vector = Vector(vector.x * 2, vector.y)
        r_vector = Vector(vector.x, vector.y * 2)
        l_expected_pos = start + l_vector
        r_expected_pos = start + r_vector
        result = end == l_expected_pos or end == r_expected_pos

        if raise_exception and not result:
            raise InvalidMovePathError(name=self.name, start=start, end=end)
        return result

    def check(
        self,
        start: Position,
        end: Position,
        board,
        attacked_piece: Optional['Piece'] = None,
        *,
        raise_exception=True,
        **kwargs,
    ) -> bool:
        kwargs['_direction'] = start.get_direction(end)
        kwargs['_distance'] = start.get_distance(end, is_difficult=True)

        return super().check(start, end, board, attacked_piece, raise_exception=raise_exception, **kwargs)

    def is_in_stalemate(self, start: Position, board) -> bool:
        possible_directions = board.get_possible_directions(start, self)
        possible_positions = self._get_possible_positions(start, possible_directions)

        for end in possible_positions:
            if board.has_piece_at_position(end):
                attacked_piece = board.get_piece(end)
            else:
                attacked_piece = None

            if self.check(start, end, board, attacked_piece, raise_exception=False):
                return False
        return True

    @staticmethod
    def _get_possible_positions(start: Position, possible_directions: set[Direction]):
        possible_positions = []
        for direction in possible_directions:
            vector = direction.vector
            l_vector = Vector(vector.x * 2, vector.y)
            r_vector = Vector(vector.x, vector.y * 2)
            for vector_ in (l_vector, r_vector):
                try:
                    possible_pos = start + vector_
                except ValueError:
                    pass
                else:
                    possible_positions.append(possible_pos)
        return possible_positions


class Bishop(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction.get_diagonal_directions())

    MAX_MOVE_COUNT = 8


class Queen(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction)

    MAX_MOVE_COUNT = 8


class King(Piece):
    ALLOWED_MOVE_DIRECTIONS: frozenset[Direction] = frozenset(Direction)

    MAX_MOVE_COUNT = 1

    def check_get_to_end_position(
        self, start: Position, end: Position, board, *, raise_exception=False, **kwargs
    ) -> bool:
        for pos, piece in board.pieces_by_color[self.color.opposite_color].items():
            if end == pos:
                continue
            elif piece.check(pos, end, board, self, raise_exception=False):
                if raise_exception:
                    raise InvalidMovePathError('King cannot move to the end position that is under attack of enemy.')
                return False

        return True

    def is_in_check(self, king_pos: Position, check_pos: Position, check_piece: Piece, board) -> bool:
        """
        Returns True if king is in check else False.
        """
        return check_piece.check(check_pos, king_pos, board, self, raise_exception=False)

    def is_in_checkmate(self, king_pos: Position, check_pos: Position, check_piece: Piece, board) -> bool:
        """
        Returns True if king is in checkmate else False.
        """
        if self._can_king_flee(king_pos, board):
            return False

        if self._has_allied_piece_to_stop_attack_to_king(king_pos, check_pos, check_piece, board):
            return False

        return True

    def _can_king_flee(self, king_pos: Position, board) -> bool:
        """
        Returns True if king can move to another square that isn't on attack line of enemy chess piece else False
        """
        king_possible_direction = board.get_possible_directions(king_pos, self)
        for direction in king_possible_direction:
            possible_pos = king_pos + direction.vector
            attacked_piece = board.get_piece(possible_pos) if board.has_piece_at_position(possible_pos) else None
            if self.check(king_pos, possible_pos, board, attacked_piece, raise_exception=False):
                return True
        return False

    def _has_allied_piece_to_stop_attack_to_king(
        self, king_pos: Position, check_pos: Position, check_piece: Piece, board
    ) -> bool:
        """
        Returns True if there has some allied chess piece to stop attack to king.
        """
        for allied_pos, allied_piece in board.pieces_by_color[self.color].items():
            if allied_piece.check(allied_pos, check_pos, board, check_piece, raise_exception=False):
                return True
            elif not isinstance(check_piece, Knight) and self._has_allied_piece_to_stand_on_attack_line_before_king(
                king_pos, check_pos, allied_pos, allied_piece, board
            ):
                return True
        return False

    @staticmethod
    def _has_allied_piece_to_stand_on_attack_line_before_king(
        king_pos: Position, check_pos: Position, allied_pos: Position, allied_piece: Piece, board
    ) -> bool:
        for pos in king_pos.get_range_between(check_pos):
            if allied_piece.check(allied_pos, pos, board, raise_exception=False):
                return True
        return False
