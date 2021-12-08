from collections import Counter
import numpy as np
from typing import Any, Sequence


def parse_inputs(
    inputs: Sequence[str]
) -> np.array:
    return np.array(list(map(list, inputs)))


def extrem_frequency(
    array: Sequence[Any],
    frequency_mode: str
) -> Any:
    if frequency_mode not in {'most_common', 'least_common'}:
        raise ValueError(f'Unsupported frequency_mode `{frequency_mode}`')

    most_common_index = {'most_common': 0, 'least_common': -1}[frequency_mode]

    most_common_values = sorted(Counter(array).most_common(), key=lambda t: (t[1], t[0]), reverse=True)
    return most_common_values[most_common_index][0]


def ex_a(
    inputs: Sequence[str],
) -> int:
    bits_grid = parse_inputs(inputs)

    most_frequent_bits = map(
        lambda i:
        extrem_frequency(bits_grid[:, i], 'most_common'),
        range(bits_grid.shape[1])
    )

    gamma_rate = int(''.join(most_frequent_bits), 2)
    epsilon_rate = gamma_rate ^ int('1' * bits_grid.shape[1], 2)

    return gamma_rate * epsilon_rate


def filter_with_bit_frequency(
    bits_grid: np.array,
    frequency_mode: str
) -> str:

    extrem_frequency_bit_in_col0 = extrem_frequency(
        array=bits_grid[:, 0],
        frequency_mode=frequency_mode
    )

    filtered_bits_grid = bits_grid[bits_grid[:, 0] == extrem_frequency_bit_in_col0]

    if filtered_bits_grid.shape[0] == 1:
        return ''.join(filtered_bits_grid[0])

    return extrem_frequency_bit_in_col0 + filter_with_bit_frequency(
        bits_grid=filtered_bits_grid[:, 1:],
        frequency_mode=frequency_mode
    )


def ex_b(
    inputs: Sequence[str],
) -> int:
    bits_grid = parse_inputs(inputs)

    oxygen_generator_rating_str = filter_with_bit_frequency(
        bits_grid=bits_grid,
        frequency_mode='most_common'
    )
    oxygen_generator_rating = int(oxygen_generator_rating_str, 2)

    co2_scrubber_rating_str = filter_with_bit_frequency(
        bits_grid=bits_grid,
        frequency_mode='least_common'
    )
    co2_scrubber_rating = int(co2_scrubber_rating_str, 2)

    return oxygen_generator_rating * co2_scrubber_rating


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
