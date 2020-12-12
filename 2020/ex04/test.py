import unittest
from ex import ex_a, ex_b, rules


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 2)

    def test_rules(self):
        self.assertTrue(rules['byr']('2002'))
        self.assertFalse(rules['byr']('2003'))

        self.assertTrue(rules['hgt']('60in'))
        self.assertTrue(rules['hgt']('190cm'))
        self.assertFalse(rules['hgt']('190in'))
        self.assertFalse(rules['hgt']('190'))

        self.assertTrue(rules['hcl']('#123abc'))
        self.assertFalse(rules['hcl']('#123abz'))
        self.assertFalse(rules['hcl']('123abc'))

        self.assertTrue(rules['ecl']('brn'))
        self.assertFalse(rules['ecl']('wat'))

        self.assertTrue(rules['pid']('000000001'))
        self.assertFalse(rules['pid']('0123456789'))

    def test_rules_on_invalid_passports(self):
        invalid_passports = [
            'eyr:1972 cid:100',
            'hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
            '',
            'iyr:2019',
            'hcl:#602927 eyr:1967 hgt:170cm',
            'ecl:grn pid:012533040 byr:1946',
            '',
            'hcl:dab227 iyr:2012',
            'ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
            '',
            'hgt:59cm ecl:zzz',
            'eyr:2038 hcl:74454a iyr:2023',
            'pid:3556412378 byr:2007']
        self.assertEqual(ex_b(invalid_passports), 0)

    def test_rules_on_valid_passports(self):
        valid_passports = [
            'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980',
            'hcl:#623a2f',
            '',
            'eyr:2029 ecl:blu cid:129 byr:1989',
            'iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
            '',
            'hcl:#888785',
            'hgt:164cm byr:2001 iyr:2015 cid:88',
            'pid:545766238 ecl:hzl',
            'eyr:2022',
            '',
            'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719']
        self.assertEqual(ex_b(valid_passports), 4)


if __name__ == '__main__':
    unittest.main()
