from typing import Iterable, Iterator, Tuple, Mapping

NORTH = 'N'
EAST = 'E'
WEST = 'W'
SOUTH = 'S'

LEFT = 'L'
RIGHT = 'R'
FORWARD = 'F'
BACK = 'B'

direction_to_orientation = {
    RIGHT: {
        NORTH: EAST,
        EAST: SOUTH,
        SOUTH: WEST,
        WEST: NORTH
    },
    LEFT: {
        NORTH: WEST,
        WEST: SOUTH,
        SOUTH: EAST,
        EAST: NORTH
    },
    BACK: {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }
}


def parse_input(line: str) -> Tuple[str, int]:
    return line[0], int(line[1:])


def parse_inputs(inputs: Iterable[str]) -> Iterator[Tuple[str, int]]:
    return map(parse_input, inputs)


def direction_from_angle(initial_direction: str, angle: int) -> str:
    if initial_direction not in {RIGHT, LEFT}:
        return initial_direction

    if angle == 90:
        return initial_direction
    elif angle == 180:
        return BACK
    elif angle == 270:
        return LEFT if initial_direction == RIGHT else RIGHT


def count_moves_in_each_orientation(actions: Iterator[Tuple[str, int]],
                                    initial_direction: str = EAST) -> Mapping[str, int]:
    current_direction = initial_direction
    counts = {NORTH: 0, EAST: 0, WEST: 0, SOUTH: 0}

    for i, (action, parameter) in enumerate(actions):
        if action == FORWARD:
            counts[current_direction] += parameter

        elif action in {LEFT, RIGHT}:
            action_90deg = direction_from_angle(action, parameter)
            current_direction = direction_to_orientation[action_90deg][current_direction]

        else:
            counts[action] += parameter

    return counts


def manhattan_distance(moves_count: Mapping[str, int]) -> int:
    return abs(moves_count[NORTH] - moves_count[SOUTH]) + abs(moves_count[EAST] - moves_count[WEST])


def ex_a(inputs: Iterable[str]) -> int:
    initial_direction = EAST
    actions = parse_inputs(inputs)
    counts = count_moves_in_each_orientation(actions, initial_direction)

    return manhattan_distance(counts)


def count_moves_around_waypoint(actions: Iterator[Tuple[str, int]],
                                waypoint: Mapping[str, int]) -> Mapping[str, int]:
    counts = {NORTH: 0, EAST: 0, WEST: 0, SOUTH: 0}

    for i, (action, parameter) in enumerate(actions):
        if action == FORWARD:
            for orientation in counts.keys():
                counts[orientation] += waypoint[orientation] * parameter

        elif action in {LEFT, RIGHT}:
            action_90deg = direction_from_angle(action, parameter)
            waypoint = {direction_to_orientation[action_90deg][orientation]: waypoint[orientation]
                        for orientation in waypoint.keys()}

        else:
            waypoint[action] += parameter

    return counts


def ex_b(inputs: Iterable[str]) -> int:
    actions = parse_inputs(inputs)
    waypoint = {EAST: 10, NORTH: 1, SOUTH: 0, WEST: 0}
    counts = count_moves_around_waypoint(actions, waypoint)
    return manhattan_distance(counts)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
