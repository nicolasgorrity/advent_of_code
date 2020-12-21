from itertools import takewhile
from typing import Sequence, Tuple, Callable, Optional


def index_brackets(string: str,
                   brackets: str = '()'
                   ) -> Optional[Tuple[int, int]]:
    opened, closed = brackets

    try:
        opened_idx = string.index(opened)
    except ValueError:
        return None

    bracket_counter = 1
    closed_idx = opened_idx

    for i, char in enumerate(string[opened_idx + 1:]):
        if char == opened:
            bracket_counter += 1

        elif char == closed:
            bracket_counter -= 1

        if bracket_counter == 0:
            closed_idx += i + 1
            break

    if closed_idx == opened_idx:
        return None

    return opened_idx, closed_idx


def index_operand(expr: str,
                  brackets: str = '()'
                  ) -> Optional[Tuple[int, int]]:
    nb_leading_spaces = sum(1 for _ in takewhile(str.isspace, expr))

    if nb_leading_spaces == len(expr):
        return None

    if expr[nb_leading_spaces] == brackets[0]:
        start_idx, end_idx = index_brackets(expr[nb_leading_spaces:], brackets)
        return start_idx + nb_leading_spaces, end_idx + nb_leading_spaces

    else:
        start_idx = nb_leading_spaces
        try:
            end_idx = nb_leading_spaces + expr[nb_leading_spaces:].index(' ') - 1
        except ValueError:
            end_idx = len(expr) - 1
        return start_idx, end_idx


def index_operator(expr: str) -> Optional[Tuple[int, int]]:
    nb_leading_spaces = sum(1 for _ in takewhile(str.isspace, expr))

    if nb_leading_spaces == len(expr):
        return None

    start_idx = nb_leading_spaces
    try:
        end_idx = nb_leading_spaces + expr[nb_leading_spaces:].index(' ') - 1
    except ValueError:
        end_idx = len(expr) - 1
    return start_idx, end_idx


def eval_operator(expr: str) -> Callable:
    if expr == '*':
        return lambda a, b: a * b
    if expr == '/':
        return lambda a, b: a / b
    if expr == '//':
        return lambda a, b: a // b
    if expr == '+':
        return lambda a, b: a + b
    if expr == '-':
        return lambda a, b: a - b

    raise ValueError(f'Operator {expr} not supported')


def eval_next_operand(expr: str) -> Optional[Tuple[int, int]]:
    first_operand_idx = index_operand(expr, brackets='()')

    if not first_operand_idx:
        return None

    operand_start, operand_end = first_operand_idx
    operand = expr[operand_start: operand_end + 1]

    try:
        operand_value = int(operand)
    except ValueError:
        operand_value = eval_expression(expr[operand_start + 1: operand_end])

    return operand_value, operand_end


def eval_next_operator(expr: str) -> Optional[Tuple[Callable, int]]:
    first_operator_idx = index_operator(expr)

    if not first_operator_idx:
        return None

    operator_start, operator_end = first_operator_idx
    operator_str = expr[operator_start: operator_end + 1]
    operator = eval_operator(operator_str)

    return operator, operator_end


def eval_expression(expr: str) -> int:
    # Parse first operand
    first_operand_eval = eval_next_operand(expr)
    if not first_operand_eval:
        raise ValueError(f'Invalid expression {expr}')
    first_operand_value, first_operand_end = first_operand_eval

    if first_operand_end + 1 == len(expr):
        return first_operand_value

    expr = expr[first_operand_end + 1:]

    # Parse first operator
    operator_eval = eval_next_operator(expr)
    if not operator_eval:
        return first_operand_value
    operator, operator_end = operator_eval

    if operator_end + 1 == len(expr):
        raise ValueError(f'Invalid expression {expr}')

    expr = expr[operator_end + 1:]

    # Parse second operand
    second_operand_eval = eval_next_operand(expr)
    if not second_operand_eval:
        raise ValueError(f'Invalid expression {expr}')
    second_operand_value, second_operand_end = second_operand_eval

    # Compute operator result
    operator_result = operator(first_operand_value, second_operand_value)

    if second_operand_end + 1 == len(expr):
        return operator_result

    # Reduce expression with new result
    reduced_expr = f'{operator_result}{expr[second_operand_end + 1:]}'

    return eval_expression(reduced_expr)


def ex_a(inputs: Sequence[str]) -> int:
    return sum(map(eval_expression, inputs))


def ex_b(inputs: Sequence[str]) -> int:
    return 0


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
