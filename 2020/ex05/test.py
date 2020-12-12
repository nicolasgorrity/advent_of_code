import unittest
from ex import ex_a


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 820)

    def test_examples(self):
        self.assertEqual(ex_a(['BFFFBBFRRR']), 567)
        self.assertEqual(ex_a(['FFFBBBFRRR']), 119)
        self.assertEqual(ex_a(['BBFFBBFRLL']), 820)


if __name__ == '__main__':
    unittest.main()
