from ex import ex


def test_data_ex_a():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data)

    assert result == 4512


def test_data_ex_b():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data)

    assert False
    assert result == 4512
