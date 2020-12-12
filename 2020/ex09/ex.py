from itertools import combinations, repeat, chain
from typing import Iterable, Tuple


def ex_a(inputs: Iterable[str], preamble: int = 25) -> Tuple[int, int]:
    numbers = list(map(int, inputs))
    previous_numbers = map(lambda idx: numbers[idx-preamble:idx], range(preamble, len(numbers)))
    possible_operands = map(lambda numbers_list: combinations(numbers_list, 2), previous_numbers)
    possible_sums = map(lambda operands_list: map(sum, operands_list), possible_operands)
    valid_numbers = map(lambda sums, target_number:
                        any(map(lambda sum_: sum_ == target_number, sums)),
                        possible_sums, numbers[preamble:])
    invalid_index = preamble + list(valid_numbers).index(False)

    return numbers[invalid_index], invalid_index


def ex_b(inputs: Iterable[str], preamble: int = 25) -> int:
    invalid_number, invalid_index = ex_a(inputs, preamble)
    numbers = list(map(int, inputs))

    start_ranges = range(invalid_index-1)
    end_ranges = map(lambda start_range: range(start_range + 2, invalid_index + 1), start_ranges)
    ranges = map(lambda start_index, end_indices:
                 zip(repeat(start_index, len(end_indices)), end_indices),
                 start_ranges, end_ranges)
    ranges = list(chain.from_iterable(ranges))
    valid_ranges = filter(lambda range_: sum(numbers[range_[0]: range_[1]]) == invalid_number, ranges)

    valid_start, valid_end = list(valid_ranges)[0]
    contiguous_range = numbers[valid_start: valid_end]

    return min(contiguous_range) + max(contiguous_range)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data, preamble=25)[0])
        print('result b is', ex_b(input_data, preamble=25))
