import numpy as np
from typing import List, Sequence, Tuple, Union


def parse_inputs(
    inputs: Sequence[str],
    board_size: int = 5
) -> Tuple[List[int], np.array]:

    draws = list(map(int, inputs[0].split(',')))

    boards = list()
    nb_boards = int(len(inputs) / (board_size + 1))

    for i in range(nb_boards):
        lines = inputs[2 + i * (board_size + 1): 1 + (i + 1) * (board_size + 1)]
        lines = map(lambda s: s.split(' '), lines)
        lines = map(lambda line: filter(lambda s: len(s), line), lines)
        lines = list(map(lambda line: list(map(int, line)), lines))
        boards.append(lines)

    return draws, np.array(boards)


def check_winning_boards(
    boards: np.array
) -> List[int]:
    winning_indexes = set()

    for idx, board in enumerate(boards):
        for i in range(board.shape[0]):
            if all(nb == -1 for nb in board[i, :]):
                winning_indexes.add(idx)
                break
        if idx not in winning_indexes:
            for j in range(board.shape[1]):
                if all(nb == -1 for nb in board[:, j]):
                    winning_indexes.add(idx)
                    break

    return list(winning_indexes)


def ex(
    inputs: Sequence[str],
    pick_first: bool = True
) -> int:
    draws, boards = parse_inputs(inputs=inputs)

    winning_boards = None
    winning_draw = None
    nb_wins = 0

    for draw in draws:
        boards[boards == draw] = -1
        winning_boards_indices = check_winning_boards(boards)
        if winning_boards_indices:
            nb_wins += len(winning_boards_indices)
            winning_boards = boards[winning_boards_indices]
            winning_draw = draw
            boards = boards[list(set(range(len(boards))) - set(winning_boards_indices))]
            if pick_first:
                break
            elif len(boards) == 0:
                break

    if winning_boards is None or winning_draw is None:
        raise ValueError('No winning board found.')

    if len(winning_boards) > 1:
        raise ValueError(f'Found {len(winning_boards)} winning boards.')

    winning_board = winning_boards[0]

    # Sum non null elements of winning board
    winning_board[winning_board == -1] = 0
    winning_sum = winning_board.sum()

    return winning_sum * winning_draw


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data))
        print('result b is', ex(input_data, pick_first=False))
