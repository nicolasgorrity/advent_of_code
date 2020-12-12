from itertools import combinations
import numpy as np
from typing import Iterable


def ex(inputs: Iterable[str], nb_entries: int = 2) -> int:
    valid_entries = filter(lambda entries: sum(entries) == 2020, combinations(map(int, inputs), nb_entries))
    return np.prod(list(valid_entries)[0])


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data, nb_entries=2))
        print('result b is', ex(input_data, nb_entries=3))
