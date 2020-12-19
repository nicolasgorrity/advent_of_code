import unittest
from ex import ex_a, ex_b


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test_a.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 71)

    def test_ex_b(self):
        with open('test_b.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_b(inputs), 11 * 12 * 13)


if __name__ == '__main__':
    unittest.main()
