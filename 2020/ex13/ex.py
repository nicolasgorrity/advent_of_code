from itertools import compress, count
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


def min_timestep_matching_requirements(buses: Sequence[int]) -> int:
    valid_buses = list(map(lambda bus_id: bus_id != -1, buses))
    working_buses = list(compress(buses, valid_buses))
    departure_delays = list(compress(range(len(buses)), valid_buses))

    counts = list(map(lambda bus_id: count(start=1, step=1), working_buses))
    coeffs = list(map(next, counts))

    while True:
        potential_t0_list = list(map(lambda coeff, bus_id, delay:
                                     coeff * bus_id - delay, coeffs,
                                     working_buses, departure_delays))
        max_t0 = max(potential_t0_list)
        do_updates = list(map(lambda potential_t0: potential_t0 != max_t0, potential_t0_list))

        if not any(do_updates):
            break

        coeffs = list(map(lambda coeff, potential_t0, bus_id, do_update:
                          coeff + int(np.ceil((max_t0 - potential_t0) / bus_id))
                          if do_update
                          else coeff,
                          coeffs, potential_t0_list, working_buses, do_updates))

    departure_timestep = working_buses[0] * coeffs[0]
    return departure_timestep


def ex_b(inputs: Sequence[str]) -> int:
    _, all_buses = parse_inputs(inputs, ignore_x=False)
    return min_timestep_matching_requirements(all_buses)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
