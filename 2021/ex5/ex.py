from collections import Counter
from itertools import chain
from typing import List, Sequence, Tuple


def parse_inputs(
    inputs: Sequence[str],
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:

    starts, ends = zip(*map(lambda s: s.split(' -> '), inputs))
    starts = list(map(lambda s: tuple(map(int, s.split(','))), starts))
    ends = list(map(lambda s: tuple(map(int, s.split(','))), ends))

    return list(zip(starts, ends))


def custom_range(
    start: int,
    end: int
) -> List[int]:

    if start < end:
        return list(range(start, end + 1))

    if start > end:
        return list(range(end, start + 1))[::-1]

    return [start]


def is_wind_horizontal_or_vertical(
    wind_start: Tuple[int, int],
    wind_end: Tuple[int, int],
) -> bool:

    return any(wind_start[i] == wind_end[i] for i in range(2))


def get_trajectory(
    wind: Tuple[Tuple[int, int], Tuple[int, int]],
    include_diagonals: bool = False
) -> List[Tuple[int, int]]:

    wind_start, wind_end = wind

    if not include_diagonals and not is_wind_horizontal_or_vertical(wind_start, wind_end):
        return list()

    trajectory_x = custom_range(wind_start[0], wind_end[0])
    trajectory_y = custom_range(wind_start[1], wind_end[1])

    trajectory_y += [trajectory_y[-1]] * (len(trajectory_x) - len(trajectory_y))
    trajectory_x += [trajectory_x[-1]] * (len(trajectory_y) - len(trajectory_x))

    return list(zip(trajectory_x, trajectory_y))


def ex(
    inputs: Sequence[str],
    include_diagonals: bool = False
) -> int:
    winds = parse_inputs(inputs=inputs)

    all_trajectories = chain.from_iterable(
        map(lambda wind: get_trajectory(wind, include_diagonals), winds)
    )

    counter = Counter(all_trajectories)
    points_passed_more_than_twice = map(lambda cnt: cnt >= 2, counter.values())

    return sum(points_passed_more_than_twice)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data))
        print('result b is', ex(input_data, include_diagonals=True))
