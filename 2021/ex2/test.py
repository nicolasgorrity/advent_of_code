from ex import ex


def test_data_ex_a():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data)

    assert result == 150


def test_data_ex_b():
    test_file = 'test.txt'

    with open(test_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]

        result = ex(inputs=input_data, enable_aim=True)

    assert result == 900
