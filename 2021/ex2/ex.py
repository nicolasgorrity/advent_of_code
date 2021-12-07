import sys
from typing import List, Sequence, Tuple


def parse_inputs(
    inputs: Sequence[str]
) -> Tuple[List[str], List[int]]:
    splitted_lines = map(lambda s: s.split(' '), inputs)
    directions, steps = zip(*splitted_lines)
    steps = list(map(int, steps))

    return directions, steps


def move_submarine(
    directions: Sequence[str],
    steps: Sequence[int],
    initial_depth: int,
    initial_horizontal_position: int,
    initial_aim: int = 0,
    enable_aim: bool = False
) -> Tuple[int, int, int]:

    if not directions or not steps:
        return initial_depth, initial_horizontal_position, initial_aim

    direction = next(iter(directions))
    step = next(iter(steps))

    if direction == 'forward':
        initial_horizontal_position += step
        if enable_aim:
            initial_depth += initial_aim * step

    elif direction == 'down':
        if enable_aim:
            initial_aim += step
        else:
            initial_depth += step

    elif direction == 'up':
        if enable_aim:
            initial_aim -= step
        else:
            initial_depth -= step

    if len(directions) == 1 or len(steps) == 1:
        return initial_depth, initial_horizontal_position, initial_aim

    return move_submarine(
        directions=directions[1:],
        steps=steps[1:],
        initial_depth=initial_depth,
        initial_horizontal_position=initial_horizontal_position,
        initial_aim=initial_aim,
        enable_aim=enable_aim
    )


def ex(
    inputs: Sequence[str],
    enable_aim: bool = False
) -> int:
    directions, steps = parse_inputs(inputs)

    sys.setrecursionlimit(2 * len(inputs))

    depth, horizontal_position, aim = move_submarine(
        directions=directions,
        steps=steps,
        initial_depth=0,
        initial_horizontal_position=0,
        initial_aim=0,
        enable_aim=enable_aim
    )

    return depth * horizontal_position


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data))
        print('result b is', ex(input_data, enable_aim=True))
