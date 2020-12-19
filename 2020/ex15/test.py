import unittest
from ex import ex


class Test(unittest.TestCase):

    def test_ex_a(self):
        inputs = ['0,3,6',
                  '1,3,2',
                  '2,1,3',
                  '1,2,3',
                  '2,3,1',
                  '3,2,1',
                  '3,1,2']
        outputs = [0, 1, 10, 27, 78, 438, 1836]
        spoken_number_ids = [10, 2020, 2020, 2020, 2020, 2020, 2020]
        for data, output, spoken_idx in zip(inputs, outputs, spoken_number_ids):
            self.assertEqual(output, ex(data, spoken_idx))

    def test_ex_b(self):
        inputs = ['0,3,6',
                  '1,3,2',
                  '2,1,3',
                  '1,2,3',
                  '2,3,1',
                  '3,2,1',
                  '3,1,2']
        outputs = [175594, 2578, 3544142, 261214, 6895259, 18, 362]
        for data, output in zip(inputs, outputs):
            self.assertEqual(output, ex(data, 30000000))
            print('ok')


if __name__ == '__main__':
    unittest.main()
