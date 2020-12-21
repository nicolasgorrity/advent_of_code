from collections import deque
from itertools import takewhile
from typing import Sequence, Tuple, Callable, Optional, Iterator, Iterable


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


def index_operator(expr: str,
                   operators: Optional[Iterator[str]] = None
                   ) -> Optional[Tuple[int, int]]:
    if not operators:
        operators = {'+', '-', '*', '/'}

    start_idx = sum(1 for _ in takewhile(
        lambda char:
        str.isspace(char) or char not in operators,
        expr))

    if start_idx == len(expr):
        return None

    if start_idx == len(expr) - 1:
        return start_idx, start_idx

    end_idx = start_idx + sum(1 for _ in takewhile(lambda char:
                                                   char in operators,
                                                   expr[start_idx + 1:]))

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


def eval_next_operand(expr: str,
                      priority_operators: Optional[Iterable[str]] = None,
                      ) -> Optional[Tuple[int, Tuple[int, int]]]:
    first_operand_idx = index_operand(expr, brackets='()')

    if not first_operand_idx:
        return None

    operand_start, operand_end = first_operand_idx
    operand = expr[operand_start: operand_end + 1]

    try:
        operand_value = int(operand)
    except ValueError:
        operand_value = eval_expression(expr[operand_start + 1: operand_end],
                                        priority_operators)

    return operand_value, (operand_start, operand_end)


def eval_expression(expr: str,
                    priority_operators: Optional[Iterable[str]] = None
                    ) -> int:
    # Parse first operand
    first_operand_eval = eval_next_operand(expr, priority_operators)
    if not first_operand_eval:
        raise ValueError(f'Invalid expression {expr}')
    first_operand_value, (first_operand_start, first_operand_end) \
        = first_operand_eval

    operators = deque()
    operands = deque([first_operand_value])

    # Parse following operators and operands until a priority operator is found
    while True:
        if first_operand_end + 1 == len(expr):
            break

        expr = expr[first_operand_end + 1:]

        # Parse next operator
        next_operator_idx = index_operator(expr)
        if not next_operator_idx:
            break

        operator_start, operator_end = next_operator_idx
        operator_str = expr[operator_start: operator_end + 1]

        if operator_end == len(expr) - 1:
            raise ValueError('Invalid expression: '
                             f'ends by operator {operator_str}')

        expr = expr[operator_end + 1:]

        # Parse next operand
        operand2_eval = eval_next_operand(expr, priority_operators)
        if not operand2_eval:
            raise ValueError('Invalid expression: '
                             f'ends by operator {operator_str}')
        operand2_value, (operand2_start, operand2_end) = operand2_eval

        # If operand has priority, execute operation
        if not priority_operators or operator_str in priority_operators:
            operand1_value = operands.pop()
            operator = eval_operator(operator_str)
            result = operator(operand1_value, operand2_value)
            operands.append(result)

        # Else execute any previous operation not impacted by this operation
        else:
            if len(operators) > 0:
                prev_operand2_value = operands.pop()
                prev_operand1_value = operands.pop()
                operator = eval_operator(operators.pop())
                result = operator(prev_operand1_value, prev_operand2_value)
                operands.append(result)

            # And store this operation
            operators.append(operator_str)
            operands.append(operand2_value)

        first_operand_end = operand2_end

    first_operand = operands.popleft()
    while len(operators) > 0:
        operator = eval_operator(operators.popleft())
        second_operand = operands.popleft()
        first_operand = operator(first_operand, second_operand)

    return first_operand


def ex_a(inputs: Sequence[str]) -> int:
    return sum(map(eval_expression, inputs))


def ex_b(inputs: Sequence[str]) -> int:
    return sum(map(lambda expr:
                   eval_expression(expr, priority_operators={'+', '-'}),
                   inputs))


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data))
        print('result b is', ex_b(input_data))
