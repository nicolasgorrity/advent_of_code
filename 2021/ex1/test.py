from ex import ex


def test_data_ex_a():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data, window_size=1)

    assert result == 7


def test_data_ex_b():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data, window_size=3)

    assert result == 5
