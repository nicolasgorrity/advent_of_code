import unittest
from ex import ex_a, ex_b, index_brackets, eval_expression


class Test(unittest.TestCase):

    def test_ex_a(self):
        inputs = [
            '2 * 3 + (4 * 5)',
            '5 + (8 * 3 + 9 + 3 * 4 * 3)',
            '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
            '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
        ]
        outputs = [
            26,
            437,
            12240,
            13632
        ]

        for input_data, output in zip(inputs, outputs):
            self.assertEqual(eval_expression(input_data), output)

        self.assertEqual(ex_a(inputs), sum(outputs))

    def test_index_brackets(self):
        self.assertEqual(index_brackets('()'), (0, 1))
        self.assertEqual(index_brackets('a(o)c'), (1, 3))

        self.assertEqual(index_brackets('aaa(aaa'), None)
        self.assertEqual(index_brackets('aze)rty'), None)
        self.assertEqual(index_brackets('(()'), None)

        self.assertEqual(index_brackets('b(k([{j]})(4)2)'), (1, 14))


if __name__ == '__main__':
    unittest.main()
