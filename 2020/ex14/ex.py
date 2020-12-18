from itertools import chain, starmap, product, repeat
from typing import Sequence, List, Tuple, Optional, Iterator


def parse_inputs(inputs: Sequence[str]) -> List[Tuple[str, List[Tuple[int, int]]]]:
    instructions = list()
    for input_line in inputs:
        if input_line.startswith('mask = '):
            instructions.append((input_line.split('mask = ')[1].strip(), list()))

        else:
            key, value = input_line.strip().split(' = ')
            value = int(value)
            key = int(key.split('[')[1].split(']')[0])
            instructions[-1][1].append((key, value))

    return instructions


def int_to_binary_string(value: int, length: Optional[int] = 0) -> str:
    return f'{value:0{length}b}'


def masked_value(value: int, mask: str) -> int:
    value = int_to_binary_string(value, len(mask))
    value = map(lambda val_chr, mask_chr:
                val_chr if mask_chr == 'X'
                else mask_chr,
                value, mask)
    return int(''.join(value), 2)


def mask_memory_output(mask: str, operations: Iterator[Tuple[int, int]]) -> Iterator[Tuple[int, int]]:
    return starmap(lambda address, value: (address, masked_value(value, mask)), operations)


def ex_a(inputs: Sequence[str]) -> int:
    instructions = parse_inputs(inputs)
    masks_memory = starmap(mask_memory_output, instructions)
    memory = dict(chain.from_iterable(masks_memory))
    return sum(memory.values())


def masked_addresses(address: int, mask: str) -> Iterator[int]:
    address_binary = int_to_binary_string(address, len(mask))
    address_masked = ''.join(map(lambda address_chr, mask_chr:
                                 address_chr if mask_chr == '0'
                                 else mask_chr,
                                 address_binary, mask))
    address_splits = address_masked.split('X')
    nb_x = len(address_splits) - 1
    possible_x_values = product(*repeat((0, 1), nb_x))
    addresses = map(lambda x_values:
                    ''.join([address_splits[0]] + [str(x_val) + split
                                                   for x_val, split in zip(x_values, address_splits[1:])]),
                    possible_x_values)

    return map(lambda address_str: int(address_str, 2), addresses)


def decoder_operation_memory(mask: str, address: int, value: int) -> Iterator[Tuple[int, int]]:
    return zip(masked_addresses(address, mask), repeat(value))


def decoder_mask_memory(mask: str, operations: Iterator[Tuple[int, int]]) -> List[Tuple[int, int]]:
    return list(chain.from_iterable(starmap(lambda address, value:
                                            decoder_operation_memory(mask, address, value),
                                            operations)))


def ex_b(inputs: Sequence[str]) -> int:
    instructions = parse_inputs(inputs)
    masks_memory = starmap(decoder_mask_memory, instructions)
    memory = dict(chain.from_iterable(masks_memory))
    return sum(memory.values())


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
