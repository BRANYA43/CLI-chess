from pytest import raises

from objects.enums import Direction
from objects.position import Position
from objects.vector import Vector


class TestPosition:
    def test_creating_position(self):
        pos = Position(1, 0)
        assert pos.x == 1
        assert pos.y == 0

    def test_creating_position_raises_error_if_x_or_y_dont_have_int_type(self):
        # invalid "x" type
        with raises(TypeError, match='x and y must be integer.'):
            Position('1', 0)

        # invalid "y: type
        with raises(TypeError, match='x and y must be integer.'):
            Position(0, '2')

    def test_position_is_hashed(self):
        pos = Position(20, 30)
        assert hash(pos) == hash((pos.x, pos.y))

    def test_position_is_iterable(self):
        x, y = Position(20, 30)
        assert x == 20
        assert y == 30

    def test_adding_position_with_vector_new_position(self):
        pos = Position(1, 2)
        vector = Vector(-1, 3)

        new_pos = pos + vector
        assert new_pos is not pos
        assert new_pos.x == (pos.x + vector.x)
        assert new_pos.y == (pos.y + vector.y)

    def test_adding_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 2)
        invalid_operand = (1, 2)

        with raises(TypeError, match=r'Expected Vector, but got tuple.'):
            pos + invalid_operand

    def test_subtracting_two_positions_returns_vector(self):
        pos_1 = Position(1, 2)
        pos_2 = Position(3, 1)

        new_vector = pos_1 - pos_2
        assert new_vector.x == (pos_1.x - pos_2.x)
        assert new_vector.y == (pos_1.y - pos_2.y)

    def test_subtracting_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 2)
        invalid_operand = (1, 2)

        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos - invalid_operand

    def test_equal_comparing(self):
        main = Position(0, 1)
        equal = Position(0, 1)
        not_equal = Position(1, 0)

        assert (main == equal) is True
        assert (main == not_equal) is False

    def test_equal_comparing_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 2)
        invalid_operand = (1, 2)

        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos == invalid_operand

    def test_not_equal_comparing(self):
        main = Position(0, 1)
        equal = Position(0, 1)
        not_equal_by_x = Position(1, 1)
        not_equal_by_y = Position(0, 2)

        assert (main != equal) is False
        assert (main != not_equal_by_x) is True
        assert (main != not_equal_by_y) is True

    def test_not_equal_comparing_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 2)
        invalid_operand = (1, 2)

        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos != invalid_operand

    def test_greate_than_comparing(self):
        main = Position(1, 3)

        # main greate than (True)
        x_equal_y_less = Position(1, 2)
        x_greate_y_less = Position(2, 2)
        x_y_less = Position(0, 2)
        x_less_y_equal = Position(0, 3)

        for pos in (x_equal_y_less, x_greate_y_less, x_y_less, x_less_y_equal):
            assert (main > pos) is True

        # main less than (False)
        x_y_equal = main
        x_equal_y_greate = Position(1, 4)
        x_y_greate = Position(2, 4)
        x_greate_y_equal = Position(2, 3)
        x_less_y_greate = Position(0, 4)

        for pos in (x_y_equal, x_equal_y_greate, x_y_greate, x_greate_y_equal, x_less_y_greate):
            assert (main > pos) is False

    def test_greate_than_comparing_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 3)
        invalid_operand = (1, 2)
        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos > invalid_operand

    def test_greate_than_or_equal_comparing(self):
        main = Position(1, 3)

        # main greate than or equal (True)
        x_y_equal = main
        x_equal_y_less = Position(1, 2)
        x_greate_y_less = Position(2, 2)
        x_y_less = Position(0, 2)
        x_less_y_equal = Position(0, 3)

        for pos in (x_y_equal, x_equal_y_less, x_greate_y_less, x_y_less, x_less_y_equal):
            assert (main >= pos) is True

        # main less than (False)
        x_equal_y_greate = Position(1, 4)
        x_y_greate = Position(2, 4)
        x_greate_y_equal = Position(2, 3)
        x_less_y_greate = Position(0, 4)

        for pos in (x_equal_y_greate, x_y_greate, x_greate_y_equal, x_less_y_greate):
            assert (main >= pos) is False

    def test_greate_than_or_equal_comparing_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 3)
        invalid_operand = (1, 2)
        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos >= invalid_operand

    def test_less_than_comparing(self):
        main = Position(1, 3)

        # main less than (True)
        x_equal_y_greate = Position(1, 4)
        x_y_greate = Position(2, 4)
        x_greate_y_equal = Position(2, 3)
        x_less_y_greate = Position(0, 4)

        for pos in (x_equal_y_greate, x_y_greate, x_greate_y_equal, x_less_y_greate):
            assert (main < pos) is True

        # main greate than (False)
        x_y_equal = main
        x_equal_y_less = Position(1, 2)
        x_greate_y_less = Position(2, 2)
        x_y_less = Position(0, 2)
        x_less_y_equal = Position(0, 3)

        for pos in (x_y_equal, x_equal_y_less, x_greate_y_less, x_y_less, x_less_y_equal):
            assert (main < pos) is False

    def test_less_than_comparing_raises_error_if_second_operand_isnt_position(self):
        pos = Position(1, 3)
        invalid_operand = (1, 2)
        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos < invalid_operand

    def test_less_than_ot_equal_comparing(self):
        main = Position(1, 3)

        # main less than (True)
        x_y_equal = main
        x_equal_y_greate = Position(1, 4)
        x_y_greate = Position(2, 4)
        x_greate_y_equal = Position(2, 3)
        x_less_y_greate = Position(0, 4)

        for pos in (x_y_equal, x_equal_y_greate, x_y_greate, x_greate_y_equal, x_less_y_greate):
            assert (main <= pos) is True

        # main greate than (False)
        x_equal_y_less = Position(1, 2)
        x_greate_y_less = Position(2, 2)
        x_y_less = Position(0, 2)
        x_less_y_equal = Position(0, 3)

        for pos in (x_equal_y_less, x_greate_y_less, x_y_less, x_less_y_equal):
            assert (main <= pos) is False

    def test_less_than_ot_equal_comparing_if_second_operand_isnt_position(self):
        pos = Position(1, 3)
        invalid_operand = (1, 2)
        with raises(TypeError, match=r'Expected Position, but got tuple.'):
            pos <= invalid_operand

    def test_position_gets_correct_direction(self):
        """
           0    1    2   3    4
        0 [UL] [UL] [U] [UR] [UR]
        1 [UL] [UL] [U] [UR] [UR]
        2 [L ] [L ] [#] [R ] [R ]
        3 [DL] [DL] [D] [DR] [DR]
        4 [DL] [DL] [D] [DR] [DR]
        """
        start = Position(2, 2)
        directions_coords = {
            Direction.UP: [(2, 0), (2, 1)],
            Direction.DOWN: [(2, 3), (2, 4)],
            Direction.LEFT: [(1, 2), (0, 2)],
            Direction.RIGHT: [(3, 2), (4, 2)],
            Direction.UP_LEFT: [(0, 0), (1, 0), (0, 1), (1, 1)],
            Direction.UP_RIGHT: [(3, 0), (4, 0), (3, 1), (4, 1)],
            Direction.DOWN_LEFT: [(0, 3), (1, 3), (0, 4), (1, 4)],
            Direction.DOWN_RIGHT: [(3, 3), (4, 3), (3, 4), (4, 4)],
        }
        for direction, coords in directions_coords.items():
            for x, y in coords:
                end = Position(x, y)
                assert start.get_direction(end) == direction

    def test_getting_distance_with_considering_diagonal_directions(self):
        """
           0   1   2   3   4
        0 [2] [ ] [2] [ ] [2]
        1 [ ] [1] [1] [1] [ ]
        2 [2] [1] [#] [1] [2]
        3 [ ] [1] [1] [1] [ ]
        4 [2] [ ] [2] [ ] [2]
        """
        start = Position(2, 2)
        # x, y, distance
        coords_distances = [
            (2, 1, 1),
            (2, 0, 2),  # UP
            (2, 3, 1),
            (2, 4, 2),  # DOWN
            (1, 2, 1),
            (0, 2, 2),  # LEFT
            (3, 2, 1),
            (4, 2, 2),  # RIGHT
            (1, 1, 1),
            (0, 0, 2),  # UP_LEFT
            (3, 1, 1),
            (4, 0, 2),  # UP_RIGHT
            (1, 3, 1),
            (0, 4, 2),  # DOWN_LEFT
            (3, 3, 1),
            (4, 4, 2),  # DOWN_RIGHT
        ]  # noqa

        for x, y, distance in coords_distances:
            end = Position(x, y)
            assert start.get_distance(end) == distance

    def test_getting_distance_without_considering_diagonal_directions(self):
        """
           0   1   2   3   4
        0 [4] [3] [2] [3] [4]
        1 [3] [2] [1] [2] [3]
        2 [2] [1] [#] [1] [2]
        3 [3] [2] [1] [2] [3]
        4 [4] [3] [2] [3] [4]
        """
        start = Position(2, 2)
        # x, y, distance
        coords_distances = [
            (2, 1, 1),
            (2, 0, 2),  # UP
            (2, 3, 1),
            (2, 4, 2),  # DOWN
            (1, 2, 1),
            (0, 2, 2),  # LEFT
            (3, 2, 1),
            (4, 2, 2),  # RIGHT
            (1, 1, 2),
            (1, 0, 3),
            (0, 1, 3),
            (0, 0, 4),  # UP_LEFT
            (3, 1, 2),
            (3, 0, 3),
            (4, 1, 3),
            (4, 0, 4),  # UP_RIGHT
            (1, 3, 2),
            (0, 3, 3),
            (1, 4, 3),
            (0, 4, 4),  # DOWN_LEFT
            (3, 3, 2),
            (4, 3, 3),
            (3, 4, 3),
            (4, 4, 4),  # DOWN_RIGHT
        ]  # noqa
        for x, y, distance in coords_distances:
            end = Position(x, y)
            assert start.get_distance(end, is_difficult=True) == distance

    def test_getting_range_between_two_positions(self):
        """
           0   1   2   3   4
        0 [S] [x] [x] [x] [E]
        1 [x] [x] [ ] [ ] [ ]
        2 [x] [ ] [x] [ ] [ ]
        3 [x] [ ] [ ] [x] [ ]
        4 [E] [ ] [ ] [ ] [E]
           0   1   2   3   4
        0 [E] [x] [x] [x] [S]
        1 [ ] [ ] [ ] [x] [x]
        2 [ ] [ ] [x] [ ] [x]
        3 [ ] [x] [ ] [ ] [x]
        4 [E] [ ] [ ] [ ] [E]
           0   1   2   3   4
        0 [E] [ ] [ ] [ ] [E]
        1 [x] [ ] [ ] [x] [ ]
        2 [x] [ ] [x] [ ] [ ]
        3 [x] [x] [ ] [ ] [ ]
        4 [S] [x] [x] [x] [E]
           0   1   2   3   4
        0 [E] [ ] [ ] [ ] [E]
        1 [ ] [x] [ ] [ ] [x]
        2 [ ] [ ] [x] [ ] [x]
        3 [ ] [ ] [ ] [x] [x]
        4 [E] [x] [x] [x] [S]
        """
        starts = [(0, 0), (4, 0), (0, 4), (4, 4)]
        ends = [
            [(4, 0), (0, 4), (4, 4)],  # start(0, 0)
            [(0, 0), (0, 4), (4, 4)],  # start(4, 0)
            [(0, 0), (4, 0), (4, 4)],  # start(0, 4)
            [(0, 0), (4, 0), (0, 4)],  # start(4, 4)
        ]
        ranges = [
            [
                [(1, 0), (2, 0), (3, 0)],  # start(0, 0) -> end(4, 0)
                [(0, 1), (0, 2), (0, 3)],  # start(0, 0) -> end(0, 4)
                [(1, 1), (2, 2), (3, 3)],
            ],  # start(0, 0) -> end(4, 4)
            [
                [(3, 0), (2, 0), (1, 0)],  # start(4, 0) -> end(0, 0)
                [(3, 1), (2, 2), (1, 3)],  # start(4, 0) -> end(0, 4)
                [(4, 1), (4, 2), (4, 3)],  # start(4, 0) -> end(4, 4)
            ],
            [
                [(0, 3), (0, 2), (0, 1)],  # start(0, 4) -> end(0, 0)
                [(1, 3), (2, 2), (3, 1)],  # start(0, 4) -> end(4, 0)
                [(1, 4), (2, 4), (3, 4)],  # start(0, 4) -> end(4, 4)
            ],
            [
                [(3, 3), (2, 2), (1, 1)],  # start(4, 4) -> end(0, 0)
                [(4, 3), (4, 2), (4, 1)],  # start(4, 4) -> end(4, 0)
                [(3, 4), (2, 4), (1, 4)],  # start(4, 4) -> end(0, 4)
            ],
        ]  # noqa

        for start_coords, ends_, ranges_ in zip(starts, ends, ranges):
            start = Position(*start_coords)
            for end_coords, range_coords in zip(ends_, ranges_):
                end = Position(*end_coords)
                range_ = [Position(*coords) for coords in range_coords]
                assert list(start.get_range_between(end)) == range_

    def test_getting_range_between_two_positions_raises_error_for_invalid_position(self):
        """
           0   1   2   3   4
        0 [ ] [E] [ ] [E] [ ]
        1 [E] [ ] [ ] [ ] [E]
        2 [ ] [ ] [S] [ ] [ ]
        3 [E] [ ] [ ] [ ] [E]
        4 [ ] [E] [ ] [E] [ ]
        """
        start = Position(2, 2)
        error_positions = [(1, 0), (3, 0), (0, 1), (4, 1), (0, 3), (4, 3), (1, 4), (3, 4)]
        for coords in error_positions:
            end = Position(*coords)
            with raises(
                ValueError,
                match='The angle between the vector of two positions and the x or y axis must be one of the following: 0°, 45°, 90°, 135°, or 180°.',
            ):
                list(start.get_range_between(end))

    def test_getting_range_between_two_positions_returns_no_positions_if_end_position_is_neighbor_of_start(self):
        """
           0   1   2   3   4
        0 [ ] [ ] [ ] [ ] [ ]
        1 [ ] [E] [E] [E] [ ]
        2 [ ] [E] [S] [E] [ ]
        3 [ ] [E] [E] [E] [ ]
        4 [ ] [ ] [ ] [ ] [ ]
        """
        start = Position(2, 2)
        ends = [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]

        for coords in ends:
            end = Position(*coords)
            assert list(start.get_range_between(end)) == []
