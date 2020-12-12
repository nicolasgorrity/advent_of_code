import unittest
from ex import ex, make_round, adjacent_occupied_seats, visible_occupied_seats


class Test(unittest.TestCase):

    def test_ex_a(self):
        with open('test_a/test0_a.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_occ_to_empty=4, occ_seats_method=adjacent_occupied_seats), 37)

    def test_ex_a_first_steps(self):
        next_state = None
        for i in range(6):
            with open(f'test_a/test{i}_a.txt', 'r') as f:
                floor_state = [line.strip() for line in f.readlines()]
            if i > 0:
                self.assertEqual(floor_state, next_state)
            next_state = make_round(floor_state, nb_occ_to_empty=4, occ_seats_method=adjacent_occupied_seats)

    def test_ex_b(self):
        with open('test_b/test0_b.txt', 'r') as f:
            inputs = [line.strip() for line in f.readlines()]
            self.assertEqual(ex(inputs, nb_occ_to_empty=5, occ_seats_method=visible_occupied_seats), 26)

    def test_ex_b_first_steps(self):
        next_state = None
        for i in range(7):
            with open(f'test_b/test{i}_b.txt', 'r') as f:
                floor_state = [line.strip() for line in f.readlines()]
            if i > 0:
                self.assertEqual(floor_state, next_state)
            next_state = make_round(floor_state, nb_occ_to_empty=5, occ_seats_method=visible_occupied_seats)


if __name__ == '__main__':
    unittest.main()
