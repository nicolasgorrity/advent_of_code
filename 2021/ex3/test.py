from ex import ex_a, ex_b


def test_data_ex_a():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex_a(inputs=input_data)

    assert result == 198


def test_data_ex_b():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex_b(inputs=input_data)

    assert result == 230
