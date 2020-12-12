from itertools import product, starmap
from typing import Sequence, Callable

OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'


def occupied_seat_in_direction(x: int, y: int, dx: int, dy: int, floor_state: Sequence[str]) -> bool:
    if x < 0 or y < 0 or x >= len(floor_state[0]) or y >= len(floor_state):
        return False

    if floor_state[y][x] == OCCUPIED:
        return True

    if floor_state[y][x] == EMPTY:
        return False

    return occupied_seat_in_direction(x + dx, y + dy, dx, dy, floor_state)


def visible_occupied_seats(x: int, y: int, floor_state: Sequence[str]) -> int:
    all_directions = set(product(range(-1, 2), repeat=2)) - {(0, 0)}
    occupied_seats = starmap(lambda d_x, d_y:
                             occupied_seat_in_direction(x + d_x, y + d_y, d_x, d_y, floor_state),
                             all_directions)
    return sum(occupied_seats)


def adjacent_occupied_seats(x: int, y: int, floor_state: Sequence[str]) -> int:
    min_x = max(0, x-1)
    max_x = min(len(floor_state[0]), x + 2)
    min_y = max(0, y - 1)
    max_y = min(len(floor_state), y + 2)
    all_adjacent_poses = set(product(range(min_x, max_x), range(min_y, max_y))) - {(x, y)}
    adjacent_seats_count = sum(starmap(lambda x_coord, y_coord:
                                       floor_state[y_coord][x_coord] == OCCUPIED,
                                       all_adjacent_poses))
    return adjacent_seats_count


def update_cell(x: int, y: int,
                floor_state: Sequence[str],
                nb_occ_to_empty: int, occ_seats_method: Callable) -> str:
    cell_state = floor_state[y][x]

    if cell_state == FLOOR:
        return cell_state

    occupied_seats_cnt = occ_seats_method(x, y, floor_state)

    if cell_state == EMPTY and occupied_seats_cnt == 0:
        return OCCUPIED

    if cell_state == OCCUPIED and occupied_seats_cnt >= nb_occ_to_empty:
        return EMPTY

    return cell_state


def make_round(floor_state: Sequence[str], nb_occ_to_empty: int, occ_seats_method: Callable) -> Sequence[str]:
    y_range = range(len(floor_state))
    x_range = range(len(floor_state[0]))
    return list(map(lambda y:
                    ''.join(map(lambda x:
                                update_cell(x, y, floor_state, nb_occ_to_empty, occ_seats_method),
                                x_range)),
                    y_range))


def ex(floor_state: Sequence[str], nb_occ_to_empty: int, occ_seats_method: Callable) -> int:
    stop = False
    while not stop:
        new_state = make_round(floor_state, nb_occ_to_empty, occ_seats_method)
        stop = new_state == floor_state
        floor_state = new_state
    nb_occupied = sum(map(lambda row: row.count(OCCUPIED), floor_state))
    return nb_occupied


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data, nb_occ_to_empty=4, occ_seats_method=adjacent_occupied_seats))
        print('result b is', ex(input_data, nb_occ_to_empty=5, occ_seats_method=visible_occupied_seats))
