import operator
import re
from typing import ClassVar


class StringCalculator:
    PRECEDENCE: ClassVar = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    RIGHT_ASSOC: ClassVar = {"^"}
    OPERATIONS: ClassVar = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "^": operator.pow,
    }

    class Node:
        def __init__(self, value, left=None, right=None):
            self.value, self.left, self.right = value, left, right

    def __init__(self, expression):
        self.expression = expression
        self.tokens = re.findall(r"\d+(?:\.\d+)?|[+\-*/^()]", self.expression)
        self.root = None

    @classmethod
    def _apply_op(cls, op: str, b: float, a: float) -> float:
        return cls.OPERATIONS[op](a, b)

    # а) дерево виразу
    def build_tree(self) -> None:
        postfix_tokens = self.infix_to_postfix(self.expression).split()
        stack: list[StringCalculator.Node] = []

        for elem in postfix_tokens:
            if elem in self.PRECEDENCE:
                right = stack.pop()
                left = stack.pop()
                node = self.Node(elem, left=left, right=right)
                stack.append(node)
            else:
                stack.append(self.Node(elem))

        if stack:
            self.root = stack.pop()

    # б), в) обходи дерева
    def prefix(self) -> str:
        res: list[str] = []

        def _pre_order(node: StringCalculator.Node | None) -> None:
            if node is not None:
                res.append(node.value)
                _pre_order(node.left)
                _pre_order(node.right)

        _pre_order(self.root)
        return " ".join(res)

    def postfix(self) -> str:
        res: list[str] = []

        def _post_order(node: StringCalculator.Node | None) -> None:
            if node is not None:
                _post_order(node.left)
                _post_order(node.right)
                res.append(node.value)

        _post_order(self.root)
        return " ".join(res)

    # г), д) обчислення префіксного та постфіксного виразів
    @staticmethod
    def eval_postfix(expr: str) -> float:
        stack: list[float] = []
        tokens = expr.split()

        for token in tokens:
            if token in StringCalculator.PRECEDENCE:
                b = stack.pop()
                a = stack.pop()
                stack.append(StringCalculator._apply_op(token, b, a))
            else:
                stack.append(float(token))

        return stack[0]

    @staticmethod
    def eval_prefix(expr: str) -> float:
        stack: list[float] = []
        tokens = expr.split()

        for token in reversed(tokens):
            if token in StringCalculator.PRECEDENCE:
                a = stack.pop()
                b = stack.pop()
                stack.append(StringCalculator._apply_op(token, b, a))
            else:
                stack.append(float(token))

        return stack[0]

    @classmethod
    def infix_to_postfix(cls, expr: str) -> str:
        operators: list[str] = []
        output: list[str] = []
        tokens = re.findall(r"\d+(?:\.\d+)?|[+\-*/^()]", expr)

        for elem in tokens:
            if elem == "(":
                operators.append("(")
            elif elem == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                if operators and operators[-1] == "(":
                    operators.pop()
            elif elem in cls.PRECEDENCE:
                while (
                    operators
                    and operators[-1] in cls.PRECEDENCE
                    and (
                        cls.PRECEDENCE[operators[-1]] > cls.PRECEDENCE[elem]
                        or (
                            cls.PRECEDENCE[operators[-1]] == cls.PRECEDENCE[elem]
                            and elem not in cls.RIGHT_ASSOC
                        )
                    )
                ):
                    output.append(operators.pop())
                operators.append(elem)
            else:
                output.append(elem)

        while operators:
            output.append(operators.pop())

        return " ".join(output)

    # є) обчислення інфіксного виразу двома стеками
    @classmethod
    def eval_infix(cls, expr: str) -> float | int:
        values: list[float] = []
        ops: list[str] = []
        tokens = re.findall(r"\d+(?:\.\d+)?|[+\-*/^()]", expr)

        for elem in tokens:
            if elem == "(":
                ops.append("(")
            elif elem == ")":
                while ops and ops[-1] != "(":
                    op = ops.pop()
                    b = values.pop()
                    a = values.pop()
                    values.append(cls._apply_op(op, b, a))
                if ops and ops[-1] == "(":
                    ops.pop()
            elif elem in cls.PRECEDENCE:
                while ops and ops[-1] in cls.PRECEDENCE:
                    top_prec = cls.PRECEDENCE[ops[-1]]
                    curr_prec = cls.PRECEDENCE[elem]
                    is_left_assoc = elem not in cls.RIGHT_ASSOC

                    if top_prec > curr_prec or (
                        top_prec == curr_prec and is_left_assoc
                    ):
                        op = ops.pop()
                        b = values.pop()
                        a = values.pop()
                        values.append(cls._apply_op(op, b, a))
                    else:
                        break
                ops.append(elem)
            else:
                values.append(float(elem))

        while ops:
            op = ops.pop()
            b = values.pop()
            a = values.pop()
            values.append(cls._apply_op(op, b, a))

        result = values[0]
        return int(result) if result.is_integer() else result


if __name__ == "__main__":
    calc = StringCalculator("3 + 4 * 2 / (1 - 5) ^ 2 ^ 3")
    calc.build_tree()
    assert calc.postfix() == "3 4 2 * 1 5 - 2 3 ^ ^ / +"
    assert calc.prefix() == "+ 3 / * 4 2 ^ - 1 5 ^ 2 3"
    assert (
        abs(StringCalculator.eval_postfix("3 4 2 * 1 5 - 2 3 ^ ^ / +") - 3.000122)
        < 1e-4
    )
    assert (
        abs(StringCalculator.eval_prefix("+ 3 / * 4 2 ^ - 1 5 ^ 2 3") - 3.000122) < 1e-4
    )

    assert StringCalculator.infix_to_postfix("56 * (4 + 5)") == "56 4 5 + *"
    assert StringCalculator.infix_to_postfix("2 ^ 3 ^ 2") == "2 3 2 ^ ^"
    assert StringCalculator.infix_to_postfix("10 - 4 - 3") == "10 4 - 3 -"

    assert StringCalculator.eval_infix("56 * (4 + 5)") == 504
    assert StringCalculator.eval_infix("2 ^ 3 ^ 2") == 512
    assert StringCalculator.eval_infix("10 - 4 - 3") == 3

    print("Завдання 4: базові тести пройдено")
