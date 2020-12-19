from functools import reduce
from itertools import chain, filterfalse
from typing import Sequence, List, Tuple, Mapping, Iterator, Set, Dict


def parse_rule(rule: str) -> Tuple[str, List[Tuple[int, int]]]:
    field, ranges = rule.strip().split(': ')
    ranges = ranges.split(' or ')
    ranges = list(map(lambda range_str:
                      tuple(map(int, range_str.split('-'))),
                      ranges))
    return field, ranges


def parse_ticket(ticket: str) -> List[int]:
    return list(map(int, ticket.strip().split(',')))


def parse_inputs(inputs: Sequence[str]
                 ) -> Tuple[Mapping[str, List[Tuple[int, int]]],
                            List[int],
                            List[List[int]]]:
    your_ticket_idx = inputs.index('your ticket:')
    nearby_tickets_idx = inputs.index('nearby tickets:')

    rules = inputs[: your_ticket_idx - 1]
    my_ticket = inputs[your_ticket_idx + 1]
    nearby_tickets = inputs[nearby_tickets_idx + 1:]

    rules = dict(map(parse_rule, rules))
    my_ticket = parse_ticket(my_ticket)
    nearby_tickets = list(map(parse_ticket, nearby_tickets))

    return rules, my_ticket, nearby_tickets


def number_in_range(x: int, start: int, end: int) -> bool:
    return start <= x <= end


def field_matches_rule(number: int, rule: List[Tuple[int, int]]) -> bool:
    return any(map(lambda range_rule:
                   number_in_range(number, *range_rule),
                   rule))


def ticket_invalid_numbers(ticket: List[int],
                           rules: Mapping[str, List[Tuple[int, int]]]
                           ) -> List[int]:
    invalid = filterfalse(lambda x:
                          any(map(lambda rule:
                                  field_matches_rule(x, rule),
                                  rules.values())),
                          ticket)
    return list(invalid)


def ex_a(inputs: Sequence[str]) -> int:
    rules, _, nearby_tickets = parse_inputs(inputs)
    invalid_tickets_numbers = map(lambda ticket:
                                  ticket_invalid_numbers(ticket, rules),
                                  nearby_tickets)
    return sum(chain.from_iterable(invalid_tickets_numbers))


def field_matches_any_rule(field: int,
                           rules: Mapping[str, List[Tuple[int, int]]]
                           ) -> bool:
    return any(map(lambda rule:
                   field_matches_rule(field, rule),
                   rules.values()))


def field_possible_classes(field: int,
                           rules: Mapping[str, List[Tuple[int, int]]]
                           ) -> List[str]:
    return [class_name
            for class_name, rule in rules.items()
            if field_matches_rule(field, rule)]


def ticket_possible_classes(ticket: List[int],
                            rules: Mapping[str, List[Tuple[int, int]]]
                            ) -> List[List[str]]:
    return list(map(lambda field:
                    field_possible_classes(field, rules),
                    ticket))


def reduce_index_possible_classes(index_possible_classes: Iterator[List[str]]
                                  ) -> Set[str]:
    return reduce(lambda classes1, classes2:
                  classes1.intersection(classes2),
                  map(set, index_possible_classes))


def fields_indices(tickets: List[List[int]],
                   rules: Mapping[str, List[Tuple[int, int]]],
                   ) -> Dict[str, int]:
    tickets_possible_classes = list(map(lambda ticket:
                                        ticket_possible_classes(ticket, rules),
                                        tickets))
    possible_fields_transpose = map(lambda class_idx:
                                    [fields[class_idx]
                                     for fields in tickets_possible_classes],
                                    range(len(rules)))
    index_possible_fields = list(enumerate(
        map(lambda index_fields:
            reduce_index_possible_classes(index_fields),
            possible_fields_transpose)))

    fields_indices_dict = dict()
    while len(fields_indices_dict) < len(rules):
        sure_fields = filter(lambda i_fields:
                             len(i_fields[1]) == 1,
                             index_possible_fields)

        new_indices, new_fields = zip(*sure_fields)
        new_fields = list(map(lambda field_set:
                              next(iter(field_set)),
                              new_fields))

        fields_indices_dict.update(dict(zip(new_fields, new_indices)))

        index_possible_fields = [(i, possible_fields - set(new_fields))
                                 for i, possible_fields in index_possible_fields
                                 if i not in new_indices]

    return fields_indices_dict


def ex_b(inputs: Sequence[str], prefix: str = None) -> int:
    rules, my_ticket, nearby_tickets = parse_inputs(inputs)

    valid_tickets = list(filter(lambda ticket:
                                all(map(lambda field:
                                        field_matches_any_rule(field, rules),
                                        ticket)),
                                nearby_tickets))

    fields_indices_dict = fields_indices(valid_tickets, rules)

    relevant_fields = filter(lambda field:
                             not prefix or field.startswith(prefix),
                             fields_indices_dict.keys())
    relevant_indices = map(lambda field:
                           fields_indices_dict[field],
                           relevant_fields)
    relevant_values = map(lambda index: my_ticket[index], relevant_indices)

    return reduce(lambda x1, x2: x1 * x2, relevant_values)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data, prefix='departure'))
