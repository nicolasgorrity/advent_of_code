from itertools import starmap
from typing import Sequence, Iterator, List

import numpy as np
import re


optional_fields = {'cid'}
fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
mandatory_fields = fields - optional_fields


rules = dict(
    byr=lambda byr: re.match(r'^\d{4}$', byr) and 1920 <= int(byr) <= 2002,
    iyr=lambda iyr: re.match(r'^\d{4}$', iyr) and 2010 <= int(iyr) <= 2020,
    eyr=lambda eyr: re.match(r'^\d{4}$', eyr) and 2020 <= int(eyr) <= 2030,
    hgt=lambda hgt: bool(re.match(r'^(1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in)$', hgt)),
    hcl=lambda hcl: bool(re.match(r'^#[\da-f]{6}$', hcl)),
    ecl=lambda ecl: bool(re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', ecl)),
    pid=lambda pid: bool(re.match(r'^\d{9}$', pid)),
    cid=lambda cid: True
)


def parse_passports(inputs: Sequence[str]) -> Iterator[List[str]]:
    passport_splits = np.hstack([[-1], np.where(np.isin(inputs, ''))[0], len(inputs)])
    passports = [inputs[passport_splits[i] + 1: passport_splits[i + 1]] for i in range(len(passport_splits) - 1)]
    passports = map(lambda passport_lines: ' '.join(passport_lines).split(' '), passports)
    return passports


def check_mandatory_fields(passport: List[str]) -> bool:
    passport_fields = map(lambda entry: entry.split(':')[0], passport)
    missing_fields = mandatory_fields - set(passport_fields)
    valid = len(missing_fields) == 0
    return valid


def ex_a(inputs: Sequence[str]):
    passports = parse_passports(inputs)
    valid_passports = map(check_mandatory_fields, passports)
    return sum(valid_passports)


def check_validity_of_fields(passport: List[str]) -> bool:
    fields_data = map(lambda entry: entry.split(':'), passport)
    valid_fields = starmap(lambda field, data: rules[field](data), fields_data)
    return all(valid_fields)


def ex_b(inputs: Sequence[str]):
    passports = parse_passports(inputs)

    # Filter invalid passports
    passports = filter(check_mandatory_fields, passports)

    # Check consistency of fields
    valid_passports = map(check_validity_of_fields, passports)

    return sum(valid_passports)


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
