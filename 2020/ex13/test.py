import unittest
from ex import ex_a, ex_b, min_timestep_matching_requirements


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_a(inputs), 295)

    def test_ex_b(self):
        with open('test.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex_b(inputs), 1068781)

    def test_ex_b_some_examples(self):
        inputs = [
            [17,-1,13,19],
            [67,7,59,61],
            [67,-1,7,59,61],
            [67,7,-1,59,61],
            [1789,37,47,1889]
        ]
        outputs = [3417, 754018, 779210, 1261476, 1202161486]

        for buses, output in zip(inputs, outputs):
            self.assertEqual(min_timestep_matching_requirements(buses), output)


if __name__ == '__main__':
    unittest.main()
