from functools import reduce
from itertools import compress
import numpy as np
from typing import Tuple, Sequence


def parse_buses(buses: str, ignore_x: bool = True) -> Sequence[int]:
    bus_list = buses.strip().split(',')
    if ignore_x:
        bus_list = filter(lambda bus: bus != 'x', bus_list)
    else:
        bus_list = map(lambda bus: '-1' if bus == 'x' else bus, bus_list)
    return list(map(int, bus_list))


def parse_inputs(inputs: Sequence[str], ignore_x: bool = True) -> Tuple[int, Sequence[int]]:
    earliest_departure = int(inputs[0])
    working_buses = parse_buses(inputs[1], ignore_x)
    return earliest_departure, working_buses


def next_departure(earliest_departure: int, bus_id: int):
    return int(np.ceil(earliest_departure / bus_id) * bus_id)


def waiting_time(earliest_departure: int, bus_id: int):
    return next_departure(earliest_departure, bus_id) - earliest_departure


def ex_a(inputs: Sequence[str]) -> int:
    earliest_departure, working_buses = parse_inputs(inputs, ignore_x=True)
    waiting_times = list(map(lambda bus_id: waiting_time(earliest_departure, bus_id), working_buses))
    best_bus_id, min_waiting_time = min(zip(working_buses, waiting_times), key=lambda id_time: id_time[1])

    return best_bus_id * min_waiting_time


def find_synchronized_bus_coef(bus_id: int, delay: int, other_id: int, other_delay: int) -> int:
    k = 0
    while (other_id * k - other_delay + delay) % bus_id != 0:
        k += 1

    return int((other_id * k - other_delay + delay) / bus_id)


def compute_equivalent_synchronized_bus(bus1: Tuple[int, int], bus2: Tuple[int, int]) -> Tuple[int, int]:
    bus_id_1, delay_1 = bus1
    bus_id_2, delay_2 = bus2

    new_bus_id = np.lcm(bus_id_1, bus_id_2)

    bus_coeff_2 = find_synchronized_bus_coef(bus_id_2, delay_2, bus_id_1, delay_1)
    synchronized_timestamp = bus_id_2 * bus_coeff_2 - delay_2

    return new_bus_id, -synchronized_timestamp


def min_timestep_matching_requirements(buses: Sequence[int]) -> int:
    valid_buses = list(map(lambda bus_id: bus_id != -1, buses))
    working_buses = list(compress(buses, valid_buses))
    departure_delays = list(compress(range(len(buses)), valid_buses))

    synchronized_bus = reduce(compute_equivalent_synchronized_bus, zip(working_buses, departure_delays))

    return -synchronized_bus[1]


def ex_b(inputs: Sequence[str]) -> int:
    _, all_buses = parse_inputs(inputs, ignore_x=False)
    return min_timestep_matching_requirements(all_buses)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
