from ex import ex


def test_data_ex_a():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data)

    assert result == 5


def test_data_ex_b():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data, include_diagonals=True)

    assert result == 12
