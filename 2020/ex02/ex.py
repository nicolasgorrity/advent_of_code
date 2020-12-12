from typing import Iterable, Iterator, Tuple


def parse_policies(inputs: Iterable[str]) -> Tuple[Iterator[str], Iterator[str], Iterator[int], Iterator[int]]:
    whole_policies, passwords = zip(*map(lambda rule: rule.split(': '), inputs))
    policies_numbers, policies_letters = zip(*map(lambda whole_policy: whole_policy.split(' '), whole_policies))
    policies_min_nb, policies_max_nb = zip(*map(lambda policy_numbers:
                                                map(int, policy_numbers.split('-')),
                                                policies_numbers))
    return passwords, policies_letters, policies_min_nb, policies_max_nb


def ex_a(inputs: Iterable[str]) -> int:
    passwords, policies_letters, policies_min_nb, policies_max_nb = parse_policies(inputs)
    letter_counts = map(lambda password, policy_letter: password.count(policy_letter), passwords, policies_letters)
    valids = map(lambda count, nb_min, nb_max:
                 nb_min <= count <= nb_max,
                 letter_counts, policies_min_nb, policies_max_nb)
    return sum(valids)


def ex_b(inputs: Iterable[str]) -> int:
    passwords, policies_letters, policies_min_nb, policies_max_nb = parse_policies(inputs)
    correct_letters = map(lambda password, letter, min_nb, max_nb:
                          map(lambda index: password[index-1] == letter, (min_nb, max_nb)),
                          passwords, policies_letters, policies_min_nb, policies_max_nb)
    valid_rules = map(lambda valid_letters: sum(valid_letters) == 1, correct_letters)
    return sum(valid_rules)


if __name__ == '__main__':
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
