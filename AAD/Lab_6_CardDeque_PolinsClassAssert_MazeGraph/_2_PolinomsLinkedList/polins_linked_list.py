from __future__ import annotations

from collections.abc import Iterator
from typing import Any


class Mono:
    """
    Represents a single monomial (a node in our singly linked list).
    """

    def __init__(self, coefficient: int, degree: int) -> None:
        if coefficient == 0:
            self.coefficient = 0
            self.degree = 0
        else:
            self.coefficient = coefficient
            self.degree = degree

        self.next: Mono | None = None

    def clone(self) -> Mono:
        """Returns a disconnected deep copy of this Mono."""
        return Mono(self.coefficient, self.degree)

    def __str__(self) -> str:
        if self.coefficient == 0:
            return "Mono: 0"

        # Build the variable part
        var_part = ""
        if self.degree == 1:
            var_part = "x"
        elif self.degree > 1:
            var_part = f"x**{self.degree}"

        # Build the coefficient part
        if self.coefficient == 1 and self.degree != 0:
            coeff_part = ""
        elif self.coefficient == -1 and self.degree != 0:
            coeff_part = "-"
        else:
            coeff_part = str(self.coefficient)

        return f"Mono: {coeff_part}{var_part}"

    def __repr__(self) -> str:
        return f"Mono(coeff={self.coefficient}, degree={self.degree})"


class Polynomial:
    """
    Represents a polynomial using a singly linked list of Mono nodes.
    """

    def __init__(self, *args: Any) -> None:
        """
        Constructs a linked list of Mono objects.
        Accepts both Mono and Polynomial objects and flattens them,
        making sure to create copies of the nodes.
        """
        self.head: Mono | None = None
        current: Mono | None = None

        def add_node(mono_node: Mono) -> None:
            nonlocal current
            new_node = mono_node.clone()
            if self.head is None:
                self.head = new_node
                current = self.head
            else:
                current.next = new_node  # type: ignore
                current = new_node

        for item in args:
            if isinstance(item, Mono):
                add_node(item)
            elif isinstance(item, Polynomial):
                for mono in item:
                    add_node(mono)

    def __iter__(self) -> Iterator[Mono]:
        """Allows iterating through the linked list safely."""
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __str__(self) -> str:
        if not self.head:
            return "Polynomial: 0"

        terms = []
        for i, mono in enumerate(self):
            mono_str = str(mono).replace("Mono: ", "")
            if i > 0 and not mono_str.startswith("-"):
                terms.append("+" + mono_str)
            else:
                terms.append(mono_str)
        return "Polynomial: " + "".join(terms)

    def __repr__(self) -> str:
        nodes = [repr(mono) for mono in self]
        return f"Polynomial({nodes[0]}" + "".join(f" -> {n}" for n in nodes[1:]) + ")"

    def __eq__(self, other: object) -> bool:
        """Checks if two polynomials are mathematically identical in their current state."""
        if not isinstance(other, Polynomial):
            return False
        curr_self, curr_other = self.head, other.head
        while curr_self and curr_other:
            if (
                curr_self.coefficient != curr_other.coefficient
                or curr_self.degree != curr_other.degree
            ):
                return False
            curr_self = curr_self.next
            curr_other = curr_other.next
        return curr_self is None and curr_other is None

    def __hash__(self) -> int:
        """Required to store Polynomials in a set."""
        return hash(tuple((m.coefficient, m.degree) for m in self))

    @property
    def degree(self) -> int:
        """
        Returns the highest degree present in the polynomial.
        Operates non-destructively by traversing the linked list.
        """
        max_deg = 0
        for mono in self:
            max_deg = max(max_deg, mono.degree)
        return max_deg

    def copy(self) -> Polynomial:
        """
        Returns a complete deep copy of this Polynomial.
        """
        return Polynomial(self)

    @staticmethod
    def _is_greater(node_a: Mono, node_b: Mono) -> bool:
        """
        Helper comparison for sorting.
        Returns True if node_a should precede node_b in descending order.
        Zero monomials (coeff=0, degree=0) are shifted to the end.
        """
        is_a_zero = node_a.coefficient == 0 and node_a.degree == 0
        is_b_zero = node_b.coefficient == 0 and node_b.degree == 0

        if is_a_zero and not is_b_zero:
            return False
        if not is_a_zero and is_b_zero:
            return True
        if is_a_zero and is_b_zero:
            return False

        if node_a.degree == node_b.degree:
            return abs(node_a.coefficient) > abs(node_b.coefficient)

        return node_a.degree > node_b.degree

    def sort(self) -> None:
        """
        Sorts the linked list nodes in descending order by degree in-place using Insertion Sort.
        Nodes with coefficient 0 and degree 0 are moved to the end of the list.
        """
        if self.head is None or self.head.next is None:
            return

        dummy = Mono(0, 0)
        current = self.head

        while current is not None:
            next_node = current.next

            prev = dummy
            while prev.next is not None and self._is_greater(prev.next, current):
                prev = prev.next

            current.next = prev.next
            prev.next = current

            current = next_node  # type: ignore

        self.head = dummy.next

    def simplify(self) -> None:
        """
        Combines terms with the same degree and removes terms with coefficient 0.
        Mutates the current object.
        """
        if self.head is None:
            self.head = Mono(0, 0)
            return

        # Ensure canonical sorted order before combining like terms
        self.sort()

        # Phase 1: Combine adjacent terms having identical degrees
        current = self.head
        while current is not None and current.next is not None:
            if current.degree == current.next.degree:
                current.coefficient += current.next.coefficient
                current.next = current.next.next
            else:
                current = current.next

        # Phase 2: Remove all nodes with a zero coefficient
        dummy = Mono(0, 0)
        dummy.next = self.head
        prev = dummy

        while prev.next is not None:
            if prev.next.coefficient == 0:
                prev.next = prev.next.next
            else:
                prev = prev.next

        self.head = dummy.next

        # Edge case: if all terms were canceled out, represent as Mono(0, 0)
        if self.head is None:
            self.head = Mono(0, 0)

    def eval_at(self, x: float) -> float | int:
        """
        Evaluates the polynomial at a given value of x.
        """
        result = 0
        for mono in self:
            if mono.coefficient != 0:
                result += mono.coefficient * (x**mono.degree)  # type: ignore
        return result

    @property
    def derivative(self) -> Polynomial:
        """
        Returns a NEW Polynomial that is the derivative of the current one.
        The resulting polynomial is simplified and the original remains unchanged.
        """
        res = Polynomial()
        current_new: Mono | None = None

        for mono in self:
            if mono.degree > 0:
                new_coeff = mono.coefficient * mono.degree
                new_degree = mono.degree - 1
                new_node = Mono(new_coeff, new_degree)

                if res.head is None:
                    res.head = new_node
                    current_new = res.head
                else:
                    current_new.next = new_node  # type: ignore
                    current_new = new_node

        res.simplify()
        return res

    def __add__(self, other: Polynomial) -> Polynomial:
        """
        Adds two polynomials and returns a NEW Polynomial.
        """
        if not isinstance(other, Polynomial):
            return NotImplemented
        res = Polynomial(self, other)
        res.simplify()
        return res

    def __sub__(self, other: Polynomial) -> Polynomial:
        """
        Subtracts another polynomial from this one and returns a NEW Polynomial.
        """
        if not isinstance(other, Polynomial):
            return NotImplemented

        neg_other = Polynomial()
        curr: Mono | None = None
        for mono in other:
            inverted_node = Mono(-mono.coefficient, mono.degree)
            if neg_other.head is None:
                neg_other.head = inverted_node
                curr = neg_other.head
            else:
                curr.next = inverted_node  # type: ignore
                curr = inverted_node

        return self + neg_other

    def __mul__(self, other: Polynomial | int) -> Polynomial:
        """
        Multiplies this polynomial by another Polynomial or a scalar integer.
        Returns a NEW Polynomial.
        """
        res = Polynomial()
        curr_new: Mono | None = None

        def append_term(coeff: int, deg: int) -> None:
            nonlocal curr_new
            new_node = Mono(coeff, deg)
            if res.head is None:
                res.head = new_node
                curr_new = res.head
            else:
                curr_new.next = new_node  # type: ignore
                curr_new = new_node

        if isinstance(other, int):
            if other == 0:
                return Polynomial(Mono(0, 0))
            for mono in self:
                append_term(mono.coefficient * other, mono.degree)

        elif isinstance(other, Polynomial):
            for mono_self in self:
                for mono_other in other:
                    new_coeff = mono_self.coefficient * mono_other.coefficient
                    new_degree = mono_self.degree + mono_other.degree
                    append_term(new_coeff, new_degree)

        else:
            return NotImplemented

        res.simplify()
        return res

    def __rmul__(self, other: int) -> Polynomial:
        """
        Supports reflected scalar multiplication (e.g., 3 * p).
        """
        return self.__mul__(other)


def test_polynomial() -> None:
    # 1. Створення елементів Mono
    m1 = Mono(5, 2)
    m2 = Mono(1, 1)
    m3 = Mono(5, 0)
    m4 = Mono(0, 0)
    m5 = Mono(-2, 2)
    m6 = Mono(3, 1)
    m7 = Mono(-1, 0)
    m8 = Mono(0, 0)

    # 2. Створення об'єктів Polynomial
    p1 = Polynomial(m1, m2, m3, m4)
    p2 = Polynomial(m5, m6, m7, m8)
    p3 = Polynomial(m1, m2, m3, m4, m5, m6, m7, m8)

    # 3. Перевірка конструктора з іншим поліномом і копіювання
    p5 = Polynomial(m1, Polynomial(m2, m3))
    assert str(p5) == "Polynomial: 5x**2+x+5"
    p6 = p1.copy()
    assert str(p6) == "Polynomial: 5x**2+x+5+0"

    # 4. Перевірка властивості degree
    assert p1.degree == 2
    assert p2.degree == 2
    assert p3.degree == 2

    # 5. Перевірка рядкового представлення __str__
    assert str(p1) == "Polynomial: 5x**2+x+5+0"
    assert str(p2) == "Polynomial: -2x**2+3x-1+0"
    assert str(p3) == "Polynomial: 5x**2+x+5+0-2x**2+3x-1+0"

    # 6. Сортування та спрощення
    p8 = Polynomial(
        Mono(-1, 0),
        Mono(1, 1),
        Mono(-3, 1),
        Mono(0, 0),
        Mono(-3, 2),
        Mono(2, 1),
        Mono(1, 0),
        Mono(-5, 2),
    )
    p8.sort()
    print(p8)
    assert str(p8) == "Polynomial: -5x**2-3x**2+2x-3x+x+1-1+0"
    p8.simplify()
    assert str(p8) == "Polynomial: -8x**2"

    p3.sort()
    print(str(p3))
    assert str(p3) == "Polynomial: 5x**2-2x**2+3x+x+5-1+0+0"
    p3.simplify()
    assert str(p3) == "Polynomial: 3x**2+4x+4"

    # 7. Обчислення значення в точці eval_at
    assert p1.eval_at(0) == 5
    assert p1.eval_at(2) == 27
    assert p2.eval_at(0) == -1  # (p2: -2*(0)^2 + 3*(0) - 1 = -1)
    assert p2.eval_at(2) == -3  # (p2: -2*(4) + 6 - 1 = -3)

    # 8. Похідна (derivative)
    p4 = p3.derivative
    assert str(p4) == "Polynomial: 6x+4"
    assert str(p3) == "Polynomial: 3x**2+4x+4"  # p3 не змінився

    # 9. Додавання та віднімання
    p9 = Polynomial(Mono(-2, 1), Mono(-3, 0))
    p10 = Polynomial(Mono(5, 2), Mono(1, 0))

    assert str(p9 + p10) == "Polynomial: 5x**2-2x-2"
    assert str(p9 - p10) == "Polynomial: -5x**2-2x-4"

    # 10. Множення на число та на поліном
    assert str(p9 * 3) == "Polynomial: -6x-9"
    assert str(3 * p9) == "Polynomial: -6x-9"
    assert str(p9 * 0) == "Polynomial: 0"

    p11 = p1 * p9
    assert str(p11) == "Polynomial: -10x**3-17x**2-13x-15"

    print("Всі тести для Завдання 2 пройдено успішно!")


if __name__ == "__main__":
    test_polynomial()
