from typing import Sequence, List


def parse_inputs(
    inputs: Sequence[str]
) -> List[int]:
    return list(map(int, inputs))


def ex(
    inputs: Sequence[str],
    window_size: int = 1
) -> int:
    depths = parse_inputs(inputs)

    increases_in_windows = map(
        lambda previous, next_:
        next_ > previous,
        depths[:-window_size], depths[window_size:]
    )

    return sum(increases_in_windows)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data, window_size=1))
        print('result b is', ex(input_data, window_size=3))
