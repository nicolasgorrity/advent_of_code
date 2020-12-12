from collections import Counter
import numpy as np
from typing import Sequence, Iterable


def split_line_groups(inputs: Sequence[str]) -> Iterable[Sequence[str]]:
    groups_splits = np.hstack([[-1], np.where(np.isin(inputs, ''))[0], len(inputs)])
    return [inputs[groups_splits[i] + 1: groups_splits[i + 1]] for i in range(len(groups_splits) - 1)]


def ex_a(inputs: Sequence[str]) -> int:
    groups = split_line_groups(inputs)
    groups_answers_sets = map(lambda group_lines: set(''.join(group_lines)), groups)
    nb_yes = map(len, groups_answers_sets)

    return sum(nb_yes)


def count_valid_letters(group_answers: Sequence[str]) -> int:
    group_size = len(group_answers)
    answers_concat = ''.join(group_answers)
    letters_count = Counter(answers_concat)
    valid_letters = map(lambda cnt: cnt == group_size, letters_count.values())
    return sum(valid_letters)


def ex_b(inputs: Sequence[str]) -> int:
    groups = split_line_groups(inputs)
    valid_letters_per_group = map(count_valid_letters, groups)

    return sum(valid_letters_per_group)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result of ex_a is', ex_a(input_data))
        print('result of ex_b is', ex_b(input_data))
