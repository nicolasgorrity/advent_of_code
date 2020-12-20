from itertools import starmap, compress, chain, product, repeat
from typing import Sequence, List, Tuple, Iterator, Set, Callable, Any


def get_active_indices(input_line: str) -> Iterator[int]:
    return starmap(lambda i, state:
                   i,
                   filter(lambda i_state:
                          i_state[1] == '#',
                          enumerate(input_line)))


def parse_inputs(inputs: Sequence[str],
                 nb_dimensions: int) -> List[Tuple[int, ...]]:
    assert nb_dimensions >= 2
    return list(chain.from_iterable(
        starmap(lambda y, input_line:
                zip(get_active_indices(input_line),
                    repeat(y),
                    *repeat(repeat(0), nb_dimensions - 2)),
                enumerate(inputs))))


def element_wise_op(op: Callable,
                    *arrays: Tuple[Any, ...]) -> Tuple[Any, ...]:
    return type(arrays[0])(starmap(op, zip(*arrays)))


def inc_range(start: int, stop: int, step: int = 1) -> range:
    return range(start, stop + step, step)


def neighborhood(index: Tuple[int, ...]) -> Set[Tuple[int, ...]]:
    dimension = len(index)
    relative_indices = set(product(inc_range(-1, 1), repeat=dimension)) \
                       - {(0,) * dimension}
    return set(map(lambda di:
                   element_wise_op(lambda i1, i2: i1 + i2, index, di),
                   relative_indices))


def inactive_indices_with_active_neighbors(active_indices: Set[Tuple[int, ...]],
                                           nb_active: int
                                           ) -> Set[Tuple[int, ...]]:
    active_indices_neighbors = map(neighborhood, active_indices)
    inactive_neighbors_of_active_indices = map(lambda neighbors:
                                               neighbors - active_indices,
                                               active_indices_neighbors)

    inactive_candidates = set(chain.from_iterable(
        inactive_neighbors_of_active_indices))

    inactive_candidates_neighborhoods = map(neighborhood, inactive_candidates)

    inactive_candidates_toggle_condition = map(
        lambda neighbors:
        len(active_indices - neighbors) == len(active_indices) - nb_active,
        inactive_candidates_neighborhoods)

    inactive_indices_toggling = compress(inactive_candidates,
                                         inactive_candidates_toggle_condition)

    return set(inactive_indices_toggling)


def active_indices_with_active_neighbors(active_indices: Set[Tuple[int, ...]],
                                         nb_active: Set[int]
                                         ) -> Set[Tuple[int, ...]]:
    active_indices_neighborhoods = map(neighborhood, active_indices)

    nb_active_neighbors = map(lambda neighbors:
                              len(neighbors) - len(neighbors - active_indices),
                              active_indices_neighborhoods)

    validity = map(lambda nb: nb in nb_active, nb_active_neighbors)
    valid_indices = compress(active_indices, validity)

    return set(valid_indices)


def cycle(active_indices: Set[Tuple[int, ...]]) -> Set[Tuple[int, ...]]:
    indices_to_keep_active = active_indices_with_active_neighbors(
        active_indices, nb_active={2, 3})
    indices_to_deactivate = active_indices - indices_to_keep_active

    indices_to_activate = inactive_indices_with_active_neighbors(
        active_indices, nb_active=3)

    return active_indices.union(indices_to_activate) - indices_to_deactivate


def ex(inputs: Sequence[str], nb_dimensions: int, nb_cycles: int) -> int:
    active_indices = set(parse_inputs(inputs, nb_dimensions))

    for _ in range(nb_cycles):
        active_indices = cycle(active_indices)

    return len(active_indices)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex(input_data, nb_dimensions=3, nb_cycles=6))
        print('result b is', ex(input_data, nb_dimensions=4, nb_cycles=6))
