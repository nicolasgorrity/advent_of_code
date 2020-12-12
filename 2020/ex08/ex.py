from itertools import starmap
from typing import Optional, Iterable, Tuple, List


functions = dict(
    nop=lambda arg: (0, 1),
    jmp=lambda arg: (0, arg),
    acc=lambda arg: (arg, 1)
)


def get_functions(inputs: Iterable[str]) -> Tuple[List[str], List[int]]:
    operations, arguments = zip(*map(lambda instruction: instruction.split(' '), inputs))
    arguments = list(map(int, arguments))

    return list(operations), arguments


def ex_a(inputs: Optional[Iterable[str]] = None,
         operations: Optional[List[str]] = None,
         arguments: Optional[List[int]] = None) -> Tuple[int, bool]:
    if not inputs and (not operations or not arguments):
        raise ValueError('Provide either inputs or both operations and arguments')

    if operations is None or arguments is None:
        operations, arguments = get_functions(inputs)

    marked = set()
    op_idx = 0
    acc = 0
    while op_idx not in marked and op_idx < len(operations):
        marked.add(op_idx)
        op_acc, op_jmp = functions[operations[op_idx]](arguments[op_idx])
        op_idx += op_jmp
        acc += op_acc

    return acc, op_idx == len(operations)


def test_operations(initial_operations: List[str],
                    arguments: List[int],
                    new_op_idx: int,
                    new_op: str) -> Tuple[int, int, bool]:
    test_operations = initial_operations.copy()
    test_operations[new_op_idx] = new_op
    acc_value, ended = ex_a(operations=test_operations, arguments=arguments)
    return new_op_idx, acc_value, ended


def ex_b(inputs: Iterable[str]) -> int:
    operations, arguments = get_functions(inputs)

    swap_op = dict(jmp='nop', nop='jmp', acc='acc')
    new_ops = starmap(lambda i, op: (i, swap_op[op]), enumerate(operations))
    new_ops = filter(lambda i_op: i_op[1] in {'jmp', 'nop'}, new_ops)

    results = starmap(lambda idx, op: test_operations(operations, arguments, idx, op), new_ops)
    results = filter(lambda result: result[2], results)
    op_idx_to_change, final_acc_value, ended = list(results)[0]

    return final_acc_value


if __name__ == '__main__':
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f.readlines()]
        print('result a is', ex_a(input_data)[0])
        print('result b is', ex_b(input_data))
