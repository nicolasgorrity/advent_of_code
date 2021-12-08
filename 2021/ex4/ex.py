import numpy as np
from typing import List, Sequence, Tuple


def parse_inputs(
    inputs: Sequence[str]
) -> Tuple[List[int], np.array]:
    raise NotImplementedError


def ex(
    inputs: Sequence[str],
    enable_aim: bool = False
) -> int:
    _ = parse_inputs(inputs=inputs)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data))
        # print('result b is', ex(input_data))
