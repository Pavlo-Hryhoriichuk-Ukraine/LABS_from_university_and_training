import itertools
import time
import matplotlib.pyplot as plt
import numpy as np


class Set:
    def __init__(self, characteristic_tuple: tuple[int, ...]) -> None:
        self.characteristic_tuple = characteristic_tuple

    def __add__(self, other: 'Set') -> 'Set':
        # Union (A | B)
        result_vector = tuple(a | b for a, b in zip(self.characteristic_tuple, other.characteristic_tuple))
        return Set(characteristic_tuple=result_vector)

    def __mul__(self, other: 'Set') -> 'Set':
        # Intersection (A & B)
        result_vector = tuple(a & b for a, b in zip(self.characteristic_tuple, other.characteristic_tuple))
        return Set(characteristic_tuple=result_vector)

    def __truediv__(self, other: 'Set') -> 'Set':
        # Set difference (A \ B): a AND (NOT b)
        result_vector = tuple(a & (1 - b) for a, b in zip(self.characteristic_tuple, other.characteristic_tuple))
        return Set(characteristic_tuple=result_vector)

    def __sub__(self, other: 'Set') -> 'Set':
        # Alternative alias for difference (A - B)
        return self.__truediv__(other)

    def __floordiv__(self, other: 'Set') -> 'Set':
        # Symmetric difference (A Delta B): a XOR b
        result_vector = tuple(a ^ b for a, b in zip(self.characteristic_tuple, other.characteristic_tuple))
        return Set(characteristic_tuple=result_vector)

    def __neg__(self) -> 'Set':
        # Complement (-A): 1 - a (inverts 0 to 1 and 1 to 0)
        result_vector = tuple(1 - a for a in self.characteristic_tuple)
        return Set(characteristic_tuple=result_vector)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Set):
            return False

        if len(self.characteristic_tuple) != len(value.characteristic_tuple):
            return False

        return self.characteristic_tuple == value.characteristic_tuple

    def __repr__(self) -> str:
        return f"Set{self.characteristic_tuple}"

    @staticmethod
    def identity_check(string: str) -> bool:
        # Standardize equality symbol
        normalized_str = string.replace("==", "=")
        if "=" not in normalized_str:
            raise ValueError("Identity string must contain an equality sign ('=' or '==').")

        left_expr, right_expr = normalized_str.split("=", 1)

        # Identify unique set variable names (single uppercase letters, excluding constants)
        name_set = set()
        for char in string:
            if 'A' <= char <= 'Z' and char not in ('U', 'E'):
                name_set.add(char)

        variables = sorted(list(name_set))
        n = len(variables)

        if n > 10:
            raise ValueError("The number of sets must not exceed 10.")

        total_rows = 2 ** n

        # Build truth table combinations [0, 1]^n
        if n == 0:
            context = {}
        else:
            table = list(itertools.product([0, 1], repeat=n))
            columns = list(zip(*table))
            context = {var_name: Set(col_data) for var_name, col_data in zip(variables, columns)}

        # Add predefined constant sets
        context['U'] = Set((1,) * total_rows)
        context['E'] = Set((0,) * total_rows)
        context['Empty'] = context['E']

        # Evaluate both sides within the prepared context
        left_val = eval(left_expr.strip(), {"__builtins__": None}, context)
        right_val = eval(right_expr.strip(), {"__builtins__": None}, context)

        return left_val == right_val


# --- Verification and Demonstration ---

def run_set_algebra_demonstration():
    print("========== 1. VERIFYING 9 BASIC LAWS OF SET ALGEBRA ==========\n")
    laws = [
        ("Idempotent Law (Union)", "A + A == A"),
        ("Idempotent Law (Intersection)", "A * A == A"),
        ("Commutative Law (Union)", "A + B == B + A"),
        ("Commutative Law (Intersection)", "A * B == B * A"),
        ("Associative Law", "(A + B) + C == A + (B + C)"),
        ("Distributive Law", "A * (B + C) == (A * B) + (A * C)"),
        ("Absorption Law", "A + (A * B) == A"),
        ("De Morgan's Law (Union)", "-(A + B) == (-A) * (-B)"),
        ("De Morgan's Law (Intersection)", "-(A * B) == (-A) + (-B)"),
        ("Double Complement Law", "-(-A) == A"),
        ("Identity with Empty Set", "A + E == A"),
        ("Identity with Universe", "A * U == A"),
        ("Complement Law (Union)", "A + (-A) == U"),
        ("Complement Law (Intersection)", "A * (-A) == E"),
        ("Symmetric Difference Definition", "A // B == (A / B) + (B / A)"),
    ]

    for name, expr in laws:
        is_valid = Set.identity_check(expr)
        print(f"[{'PASS' if is_valid else 'FAIL'}] {name:<35} | {expr}")

    print("\n========== 2. TESTING COUNTEREXAMPLES (FALSE IDENTITIES) ==========\n")
    false_statements = [
        ("False Distributivity", "A + (B * C) == (A + B) * C"),
        ("False Complement", "A + B == -A"),
        ("False Absorption", "A * (A + B) == B"),
        ("False Difference", "A / B == B / A")
    ]

    for name, expr in false_statements:
        is_valid = Set.identity_check(expr)
        print(f"[{'CORRECT DETECTED FALSE' if not is_valid else 'ERROR'}] {name:<25} | {expr} -> Result: {is_valid}")


# --- Complexity Benchmark & Plotting ---

def benchmark_identity_check():
    print("\n========== 3. BENCHMARKING TRUTH TABLE COMPLEXITY (O(2^n)) ==========\n")

    variable_pool = [chr(ord('A') + i) for i in range(10)]
    n_values = list(range(1, 11))
    measured_times = []

    for n in n_values:
        active_vars = variable_pool[:n]
        expr = f"{' + '.join(active_vars)} == {' + '.join(reversed(active_vars))}"

        start_time = time.perf_counter()
        _ = Set.identity_check(expr)
        end_time = time.perf_counter()

        elapsed = end_time - start_time
        measured_times.append(elapsed)
        print(f"Variables: {n:2d} (Rows: {2**n:4d}) | Time: {elapsed:.6f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, measured_times, marker='o', color='darkblue', label='Empirical Verification Time')

    scale_factor = measured_times[-1] / (2 ** n_values[-1])
    theoretical_curve = [scale_factor * (2 ** n) for n in n_values]
    plt.plot(n_values, theoretical_curve, '--', color='crimson', label=r'Theoretical $O(2^n)$ Curve')

    plt.title('Truth Table Verification Complexity vs Number of Sets ($n$)')
    plt.xlabel('Number of Unique Sets ($n$)')
    plt.ylabel('Execution Time (seconds)')
    plt.yscale('log')
    plt.xticks(n_values)
    plt.grid(True, which="both", linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig('set_identity_benchmark.png')
    plt.show()


if __name__ == "__main__":
    run_set_algebra_demonstration()
    benchmark_identity_check()