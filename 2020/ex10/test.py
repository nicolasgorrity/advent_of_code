import unittest
from ex import ex_a, ex_b


class Test(unittest.TestCase):

    def test_ex_a1(self):
        with open('test_1.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 35)

    def test_ex_a2(self):
        with open('test_2.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 220)

    def test_ex_b1(self):
        with open('test_1.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_b(inputs), 8)

    def test_ex_b2(self):
        with open('test_2.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_b(inputs), 19208)


if __name__ == '__main__':
    unittest.main()
