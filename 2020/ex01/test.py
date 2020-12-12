import unittest
from ex import ex


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_entries=2), 514579)

    def test_ex_b(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_entries=3), 241861950)


if __name__ == '__main__':
    unittest.main()
