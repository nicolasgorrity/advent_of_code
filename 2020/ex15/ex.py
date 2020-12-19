from typing import Iterator, MutableMapping, List


def parse_inputs(inputs: str) -> Iterator[int]:
    return map(int, inputs.split(','))


def put_to_queue_in_dict(dictionary: MutableMapping[int, List],
                         key: int,
                         value: int) -> None:
    if key not in dictionary:
        dictionary[key] = [value]

    elif len(dictionary[key]) == 1:
        dictionary[key].append(dictionary[key][0])
        dictionary[key][0] = value

    else:
        dictionary[key][1] = dictionary[key][0]
        dictionary[key][0] = value


def ex(inputs: str, spoken_number_idx: int) -> int:
    starting_numbers = list(parse_inputs(inputs))
    spoken_numbers = dict()

    spoken_number = 0
    for i in range(spoken_number_idx):

        if i < len(starting_numbers):
            spoken_number = starting_numbers[i]

        elif spoken_number not in spoken_numbers.keys() \
                or len(spoken_numbers[spoken_number]) < 2:
            spoken_number = 0

        else:
            spoken_number = spoken_numbers[spoken_number][0] \
                            - spoken_numbers[spoken_number][1]

        put_to_queue_in_dict(spoken_numbers, spoken_number, i)

    return spoken_number


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = f.readlines()[0].strip()
        print('result a is', ex(input_data, spoken_number_idx=2020))
        print('result b is', ex(input_data, spoken_number_idx=30000000))
