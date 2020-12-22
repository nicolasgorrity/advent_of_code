from itertools import chain, product
from typing import (Sequence, List, Tuple, Iterator,
                    Mapping, Union, Dict, Optional)


def parse_sub_rule_string(sub_rule: str) -> List[int]:
    sub_rule_list = sub_rule.split(' ')
    return list(map(int, sub_rule_list))


def parse_rule_string(rule: str) -> Tuple[int, Union[str, List[List[int]]]]:
    index, rule = rule.split(': ')
    index = int(index)

    if '"' in rule:
        rule = rule.split('"')[1]

    else:
        sub_rules = rule.split(' | ')
        rule = list(map(parse_sub_rule_string, sub_rules))

    return index, rule


def parse_rules(inputs: Sequence[str]
                ) -> Dict[int, Union[str, List[List[int]]]]:
    return dict(map(parse_rule_string, inputs))


def parse_messages(inputs: Sequence[str]) -> Iterator[str]:
    return filter(lambda s: len(s), inputs)


def parse_inputs(inputs: Sequence[str]
                 ) -> Tuple[Dict[int, Union[str, List[List[int]]]],
                            List[str]]:
    data_separation = inputs.index('')

    rules = parse_rules(inputs[:data_separation])
    messages = list(inputs[data_separation + 1:])

    return rules, messages


def build_matches(rules: Mapping[int, Union[str, List[List[int]]]],
                  rule_index: int,
                  matches: Optional[Mapping[int, List[str]]] = None
                  ) -> List[str]:
    if not matches:
        matches = dict()

    if rule_index in matches.keys():
        return matches[rule_index]

    rule = rules[rule_index]

    if type(rule) == str:
        matches[rule_index] = [rule]

    elif type(rule) != list:
        raise ValueError('Rule should be a list')

    else:
        possible_matches = map(lambda subrule:
                               map(lambda subrule_nb:
                                   build_matches(rules, subrule_nb, matches),
                                   subrule),
                               rule)
        possibilities = map(lambda subrule_matches:
                            map(lambda possible_tuple:
                                ''.join(possible_tuple),
                                product(*subrule_matches)),
                            possible_matches)
        matches[rule_index] = list(chain.from_iterable(possibilities))

    return matches[rule_index]


def ex_a(inputs: Sequence[str]) -> int:
    rules, messages = parse_inputs(inputs)
    matches = build_matches(rules, 0)
    nb_matching_messages = len(set(messages).intersection(set(matches)))

    return nb_matching_messages


def _message_matches_rule(message: str,
                          rules: Mapping[int, Union[str, List[List[int]]]],
                          rule_index: int
                          ) -> int:
    if len(message) == 0:
        return 0

    rule = rules[rule_index]

    if type(rule) == str:
        return 1 if message[0] == rule else 0

    for i, sub_rules in enumerate(rule):

        len_match = 0
        valid = True
        for j, sub_rule in enumerate(sub_rules):
            len_submatch = _message_matches_rule(message[len_match:],
                                                 rules,
                                                 sub_rule)

            if len_submatch == 0:
                valid = False
                break

            len_match += len_submatch

        if valid:
            return len_match

    return 0


def message_matches_rule(message: str,
                         rules: Mapping[int, Union[str, List[List[int]]]],
                         rule_index: int
                         ) -> bool:
    if len(message) == 0:
        return False

    len_match = _message_matches_rule(message, rules, rule_index)
    return len_match == len(message)


def ex_a_v2(inputs: Sequence[str]) -> int:
    rules, messages = parse_inputs(inputs)
    matches = map(lambda message:
                  message_matches_rule(message, rules, 0),
                  messages)
    nb_matching_messages = sum(matches)

    return nb_matching_messages


def ex_b(inputs: Sequence[str]) -> int:
    rules, messages = parse_inputs(inputs)

    input_patch = ['8: 42 | 42 8',
                   '11: 42 31 | 42 11 31',
                   '', 'ignored_message']
    new_rules, _ = parse_inputs(input_patch)

    rules.update(new_rules)

    raise NotImplementedError(f'Ex b computations not implemented')

    return 0


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
