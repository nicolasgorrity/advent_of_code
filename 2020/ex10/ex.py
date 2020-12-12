from collections import Counter
from itertools import dropwhile, takewhile
import numpy as np
from typing import Iterable


def ex_a(inputs: Iterable[str]) -> int:
    adapters = [0] + sorted(map(int, inputs))
    successive_differences = np.diff(adapters)
    counts = Counter(successive_differences)
    return counts[1] * (counts[3] + 1)


def ex_b(inputs: Iterable[str]) -> int:
    adapters = [0] + sorted(map(int, inputs))
    adapters = adapters + [adapters[-1] + 3]
    possible_nexts = dict(map(lambda adapter:
                              (adapter,
                               list(takewhile(lambda val:
                                              val <= adapter + 3,
                                              dropwhile(lambda val: val <= adapter, adapters)))),
                              adapters))

    possible_combinations = dict({adapters[-1]: 1})
    for adapter in reversed(adapters[:-1]):
        possible_combinations[adapter] = sum(map(lambda possible_next: possible_combinations[possible_next],
                                                 possible_nexts[adapter]))

    nb_possible_combinations = possible_combinations[adapters[0]]

    return nb_possible_combinations


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
