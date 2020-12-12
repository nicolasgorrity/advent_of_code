import unittest
from ex import ex_a, ex_b


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 2)

    def test_ex_b(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_b(inputs), 1)


if __name__ == '__main__':
    unittest.main()
