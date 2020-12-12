from collections import Counter
from itertools import filterfalse
from functools import reduce
from typing import Mapping, Any, Union, Dict, Tuple


def remove_none_and_return_dict(dictionary: Dict[Union[None, Any], Any]) -> Dict[Any, Any]:
    dictionary.pop(None, None)
    return dictionary


def parse_container_bag_string(bag: str) -> str:
    return ' '.join(bag.strip().split(' ')[:-1])


def parse_contained_bag_string(bag: str) -> Union[Tuple[str, int], Tuple[None, None]]:
    if bag == 'no other bags':
        return None, None

    bag_words = bag.split(' ')
    return ' '.join(bag_words[1:-1]), int(bag_words[0])


def parse_contained_list_string(contained_bags: str) -> Mapping[str, int]:
    contained_dict = dict(map(parse_contained_bag_string, contained_bags.strip().replace('.', '').split(', ')))
    return remove_none_and_return_dict(contained_dict)


def compute_rules_dict(inputs):
    container, contained = zip(*map(lambda rule: rule.split(' contain '), inputs))
    contained = map(parse_contained_list_string, contained)
    container = map(parse_container_bag_string, container)
    rules = dict(zip(container, contained))
    return rules


def indirect_possible_contained(bag: str, rules: dict, marked=None):
    if marked is None:
        marked = set()

    contained_direct_set = set(rules[bag].keys())
    marked.add(bag)
    contained_indirect_set = list(map(lambda child_bag:
                                      set() if child_bag in marked
                                      else indirect_possible_contained(child_bag, rules, marked),
                                      rules[bag]))
    if len(contained_indirect_set) > 0:
        contained_indirect_set = reduce(lambda s1, s2: s1.union(s2), contained_indirect_set)

    return contained_direct_set.union(contained_indirect_set)


def ex_a(inputs, color_contained='shiny gold'):
    rules = compute_rules_dict(inputs)
    possible_contained = map(lambda bag: indirect_possible_contained(bag, rules), rules)
    nb_possible_containers = sum(map(lambda possibly_contained:
                                     color_contained in possibly_contained,
                                     possible_contained))

    return nb_possible_containers


def compute_nb_contained_bags(rules: dict, counts=None):
    if len(rules) == 0:
        return

    if counts is None:
        counts = {bag: 0 for bag in rules.keys()}

    end_leaves = list(filterfalse(lambda bag: len(rules[bag]) > 0, rules))

    for end_leaf in end_leaves:
        rules.pop(end_leaf, None)

    nb_end_leaves = map(lambda container:
                        sum(map(lambda contained_bag:
                            rules[container].pop(contained_bag, 0) * (1 + counts[contained_bag]),
                            end_leaves)),
                        rules.keys())
    new_counts = dict(zip(rules.keys(), nb_end_leaves))
    counts.update(Counter(counts) + Counter(new_counts))

    compute_nb_contained_bags(rules, counts)

    return counts


def ex_b(inputs, container_color='shiny gold'):
    rules = compute_rules_dict(inputs)
    nb_contained_per_bag = compute_nb_contained_bags(rules)
    return nb_contained_per_bag[container_color]


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
