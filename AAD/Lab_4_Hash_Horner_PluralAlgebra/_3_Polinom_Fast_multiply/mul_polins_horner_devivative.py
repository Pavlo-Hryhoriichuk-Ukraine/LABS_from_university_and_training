import time
import random
import heapq
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).parent


def multiply_two_polins(
    poly1: tuple[int | float, ...],
    poly2: tuple[int | float, ...]
) -> tuple[int | float, ...]:
    len1, len2 = len(poly1), len(poly2)
    if len1 == 0 or len2 == 0:
        return ()

    result_array = [0.0] * (len1 + len2 - 1)
    for i in range(len1):
        for j in range(len2):
            result_array[i + j] += poly1[i] * poly2[j]

    cleaned = [int(x) if isinstance(x, float) and x.is_integer() else x for x in result_array]
    return tuple(cleaned)


def multiply_many(*polynomials: tuple[int | float, ...]) -> tuple[int | float, ...]:
    if not polynomials:
        return ()

    heap = [(len(p), p) for p in polynomials]
    heapq.heapify(heap)

    while len(heap) > 1:
        _, poly1 = heapq.heappop(heap)
        _, poly2 = heapq.heappop(heap)
        res = multiply_two_polins(poly1, poly2)
        heapq.heappush(heap, (len(res), res))

    return heap[0][1]


def eval_polynomial(polynom: tuple[int | float, ...], x0: int | float) -> int | float:
    if not polynom:
        return 0.0

    result = polynom[0]
    for i in range(1, len(polynom)):
        result = result * x0 + polynom[i]
    return result


def eval_polynomial_naive(polynom: tuple[int | float, ...], x0: int | float) -> int | float:
    if not polynom:
        return 0.0

    n = len(polynom) - 1
    result = 0.0
    for i, coeff in enumerate(polynom):
        # Naive power calculation for every term
        result += coeff * (x0 ** (n - i))
    return result


def get_derivative(polynom: tuple[int | float, ...]) -> tuple[int | float, ...]:
    n = len(polynom) - 1
    if n < 1:
        return (0,)

    derivative = tuple(polynom[i] * (n - i) for i in range(n))
    return derivative


def format_polynomial(polynom: tuple[int | float, ...]) -> str:
    if not polynom:
        return "0"

    n = len(polynom)
    terms: list[tuple[str, str]] = []

    for i, coeff in enumerate(polynom):
        if coeff == 0:
            continue

        degree = n - 1 - i
        sign = "-" if coeff < 0 else "+"
        abs_coeff = abs(coeff)
        coeff_str = str(int(abs_coeff)) if isinstance(abs_coeff, float) and abs_coeff.is_integer() else str(abs_coeff)

        if degree == 0:
            term_body = coeff_str
        elif degree == 1:
            term_body = "x" if abs_coeff == 1 else f"{coeff_str}x"
        else:
            term_body = f"x^{degree}" if abs_coeff == 1 else f"{coeff_str}x^{degree}"

        terms.append((sign, term_body))

    if not terms:
        return "0"

    first_sign, first_body = terms[0]
    result_parts = [f"-{first_body}" if first_sign == "-" else first_body]

    for sign, body in terms[1:]:
        result_parts.append(f" {sign} {body}")

    return "".join(result_parts)




def plot_function_and_derivative(poly: tuple[int | float, ...], x0: float, x_range: tuple[float, float] = (-5, 5)):
    """Plots P(x), its derivative P'(x), and marks the value at x0."""
    print("\n[*] Generating plot for P(x) and P'(x)...")

    derivative = get_derivative(poly)


    x_vals = np.linspace(x_range[0], x_range[1], 400)

    y_vals_p = [eval_polynomial(poly, x) for x in x_vals]
    y_vals_dp = [eval_polynomial(derivative, x) for x in x_vals]

    y0_p = eval_polynomial(poly, x0)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals_p, label=f'$P(x) = {format_polynomial(poly)}$', color='blue', linewidth=2)
    plt.plot(x_vals, y_vals_dp, label=f"$P'(x) = {format_polynomial(derivative)}$", color='red', linestyle='--')

    plt.scatter([x0], [y0_p], color='black', zorder=5)
    plt.annotate(f'P({x0}) = {y0_p}', (x0, y0_p), textcoords="offset points", xytext=(-15, 10), ha='center')

    plt.title('Polynomial and its Derivative Visualization')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ROOT_DIR / 'polynomial_derivative_plot.png')
    plt.show()


def benchmark_multiplication_time():
    """Plots multiplication time against degree n for n in [10, 1000]."""
    print("\n[*] Running Polynomial Multiplication Benchmark (n = 10 to 1000)...")

    degrees = [10, 50, 100, 250, 500, 750, 1000]
    times = []

    for d in degrees:
        p1 = tuple(random.uniform(-10, 10) for _ in range(d + 1))
        p2 = tuple(random.uniform(-10, 10) for _ in range(d + 1))

        start = time.perf_counter()
        _ = multiply_two_polins(p1, p2)
        end = time.perf_counter()

        times.append(end - start)
        print(f"Degree {d:4d} x {d:4d} | Exec Time: {times[-1]:.6f}s")

    plt.figure(figsize=(10, 5))
    plt.plot(degrees, times, marker='o', color='royalblue', label='Empirical Time')

    coef = times[-1] / (degrees[-1] ** 2)
    theoretical = [coef * (d ** 2) for d in degrees]

    plt.plot(degrees, theoretical, '--', color='red', label=r'Theoretical $O(n^2)$')
    plt.title('Multiplication Time vs Degree ($n$)')
    plt.xlabel('Polynomial Degree ($n$)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(ROOT_DIR / 'multiplication_benchmark.png')
    plt.show()


def benchmark_evaluation_time():
    """Plots evaluation time comparison between Horner's scheme and Naive method for N in [10, 10^5]."""
    print("\n[*] Running Evaluation Benchmark: Horner vs Naive (N = 10 to 10^5)...")

    degrees = [10, 100, 1000, 10000, 50000, 100000]
    horner_times = []
    naive_times = []
    x0 = 1.000001 # Small offset to avoid overflow during naive high power calculations

    for n in degrees:
        poly = tuple(random.uniform(-5, 5) for _ in range(n + 1))

        # Benchmark Horner
        start_h = time.perf_counter()
        _ = eval_polynomial(poly, x0)
        end_h = time.perf_counter()
        horner_times.append(end_h - start_h)

        # Benchmark Naive
        start_n = time.perf_counter()
        _ = eval_polynomial_naive(poly, x0)
        end_n = time.perf_counter()
        naive_times.append(end_n - start_n)

        print(f"Degree {n:6d} | Horner: {horner_times[-1]:.6f}s | Naive: {naive_times[-1]:.6f}s")

    plt.figure(figsize=(10, 5))
    plt.plot(degrees, horner_times, marker='o', color='green', label="Horner's Scheme $O(N)$")
    plt.plot(degrees, naive_times, marker='s', color='red', label='Naive Algorithm')

    plt.title('Evaluation Time: Horner vs Naive Algorithm')
    plt.xlabel('Polynomial Degree ($N$)')
    plt.ylabel('Time (seconds)')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('evaluation_benchmark.png')
    plt.show()


if __name__ == "__main__":
    sample_poly = (2, -3, -12, 5)
    plot_function_and_derivative(sample_poly, x0=2.0)

    benchmark_multiplication_time()

    benchmark_evaluation_time()