from typing import Iterable, Iterator


def binarize_row(row: str) -> str:
    return row.replace('B', '1').replace('F', '0')


def binarize_col(col: str) -> str:
    return col.replace('R', '1').replace('L', '0')


def binary_to_int(binary_str: str) -> int:
    return int(binary_str, 2)


def get_seat_ids(inputs: Iterable[str]) -> Iterator[int]:
    rows, cols = zip(*map(lambda boarding_pass: (boarding_pass[:7], boarding_pass[7:]), inputs))
    rows = map(binarize_row, rows)
    cols = map(binarize_col, cols)
    rows = map(binary_to_int, rows)
    cols = map(binary_to_int, cols)
    return map(lambda row, col: row * 8 + col, rows, cols)


def ex_a(inputs: Iterable[str]) -> int:
    seat_ids = get_seat_ids(inputs)
    return max(seat_ids)


def ex_b(inputs: Iterable[str]) -> int:
    seat_ids = set(get_seat_ids(inputs))
    min_id, max_id = min(seat_ids), max(seat_ids)
    possible_ids = range(min_id+1, max_id)
    valid_ids = filter(lambda id: id not in seat_ids and {id-1, id+1} < seat_ids, possible_ids)
    return list(valid_ids)[0]


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('max seat id is', ex_a(input_data))
        print('your boarding pass is', ex_b(input_data))
