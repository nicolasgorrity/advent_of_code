from collections import Counter
import numpy as np
from typing import Sequence


def parse_inputs(
    inputs: Sequence[str]
) -> np.array:
    return np.array(list(map(list, inputs)))


def ex_a(
    inputs: Sequence[str],
) -> int:
    bits_grid = parse_inputs(inputs)

    most_frequent_bits = map(lambda i: Counter(bits_grid[:, i]).most_common(1)[0][0], range(bits_grid.shape[1]))

    gamma_rate = int(''.join(most_frequent_bits), 2)
    epsilon_rate = gamma_rate ^ int('1' * bits_grid.shape[1], 2)

    return gamma_rate * epsilon_rate


def ex_b(
    inputs: Sequence[str],
) -> int:
    bits_grid = parse_inputs(inputs)

    print('TODO')


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
