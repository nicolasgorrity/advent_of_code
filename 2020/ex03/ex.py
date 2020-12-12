from functools import reduce
from itertools import count
from typing import Tuple, Sequence


def nb_encountered_trees(inputs: Sequence[str], slope: Tuple[int, int]) -> int:
    x, y = 0, 0
    dx, dy = slope
    sy = len(inputs)
    sx = len(inputs[0])

    range_y = range(y, sy, dy)
    range_x = map(lambda x_pos: x_pos % sx, count(start=x, step=dx))
    return sum(map(lambda x_pos, y_pos: inputs[y_pos][x_pos] == '#', range_x, range_y))


def ex_a(inputs: Sequence[str]) -> int:
    slope = (3, 1)
    return nb_encountered_trees(inputs, slope)


def ex_b(inputs: Sequence[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    nb_trees_per_slope = map(lambda slope: nb_encountered_trees(inputs, slope), slopes)
    return reduce(lambda nb1, nb2: nb1 * nb2, nb_trees_per_slope)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
