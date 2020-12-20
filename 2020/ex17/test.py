import random
import unittest
from ex import ex, common_neighborhoods


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_dimensions=3, nb_cycles=6), 112)

    def test_common_neighbors(self):
        x, y = [random.randint(0, 50) for _ in range(2)]
        indices = [(x - 1, y), (x, y), (x + 1, y)]
        common_neighborhood = [(x, y - 1), (x, y + 1)]
        self.assertEqual(set(common_neighborhoods(indices)),
                         set(common_neighborhood))

    def test_ex_b(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_dimensions=4, nb_cycles=6), 848)


if __name__ == '__main__':
    unittest.main()
