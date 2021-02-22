from functools import reduce
from itertools import compress, chain
import numpy as np
from typing import Sequence, Dict, Tuple, Mapping, Union


def parse_tile_data(inputs: Sequence[str]) -> Tuple[int, np.ndarray]:
    title = inputs[0]
    tile_id = int(title.split(':')[0].split(' ')[1])

    tile = np.array(list(map(list, map(chain, inputs[1:]))))
    tile = (tile == '#').astype(int)

    return tile_id, tile


def parse_inputs(inputs: Sequence[str]) -> Dict[int, np.ndarray]:
    separations = map(lambda input_line: input_line == '', inputs)
    separations_idx = list(compress(range(len(inputs)), separations))

    tiles = map(lambda start, end:
                parse_tile_data(inputs[start + 1: end]),
                [-1] + separations_idx, separations_idx + [len(inputs)])

    return dict(tiles)


def get_matrix_slice(side: int,
                     matrix_shape: Tuple[int, int]
                     ) -> Union[Tuple[int, slice], Tuple[slice, int]]:
    if side == 0:  # left
        return slice(0, matrix_shape[0]), 0
    if side == 1:  # right
        return slice(0, matrix_shape[0]), matrix_shape[1] - 1
    if side == 2:  # top
        return 0, slice(0, matrix_shape[1])
    if side == 3:  # bottom
        return matrix_shape[0] - 1, slice(0, matrix_shape[1])


def tiles_sides_match(tile_side_1: np.ndarray,
                      tile_side_2: np.ndarray) -> bool:
    return np.all(tile_side_1 == tile_side_2) \
           or np.all(tile_side_1 == tile_side_2[::-1])


def tile_match_on_side(tiles: Mapping[int, np.ndarray],
                       tile_idx: int,
                       side: int,
                       other_tile_idx: int
                       ) -> bool:
    other_tile = tiles[other_tile_idx]
    this_tile = tiles[tile_idx]
    this_tile_side = this_tile[get_matrix_slice(side, this_tile.shape)]

    for other_side in range(4):
        other_tile_side = other_tile[get_matrix_slice(other_side,
                                                      other_tile.shape)]
        if tiles_sides_match(this_tile_side, other_tile_side):
            return True

    return False


def nb_matches(tiles: Mapping[int, np.ndarray],
               tile_idx: int
               ) -> Tuple[int, int, int, int]:
    other_tiles_idx = set(tiles.keys()) - {tile_idx}
    sides = range(4)

    matching_tiles = map(lambda side:
                         sum(map(lambda other_idx:
                                 tile_match_on_side(tiles, tile_idx,
                                                    side, other_idx),
                                 other_tiles_idx)),
                         sides)

    left_match, right_match, top_match, bottom_match = matching_tiles
    return left_match, right_match, top_match, bottom_match


def ex_a(inputs: Sequence[str]) -> int:
    tiles = parse_inputs(inputs)

    matches_per_tile = list(map(lambda tile_idx:
                           nb_matches(tiles, tile_idx),
                           tiles.keys()))
    [print(nb) for nb in matches_per_tile]
    corners_condition = map(lambda idx, nb_matches:
                            nb_matches.count(0) == 2,
                            tiles.keys(), matches_per_tile)
    corners_indices = compress(tiles.keys(), corners_condition)

    return reduce(lambda i1, i2: i1 * i2, corners_indices)


def ex_b(inputs: Sequence[str]) -> int:
    return 0


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
