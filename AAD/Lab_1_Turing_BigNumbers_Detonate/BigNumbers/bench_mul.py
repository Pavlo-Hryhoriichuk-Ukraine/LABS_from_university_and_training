import time
import random
import statistics
import os
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from typing import Any

from operations import OperationStats, BigInt
from bench_add import ROOT_DIR

FILE_PATH = "multiplication_base10_experiment.png"


def generate_decimal(length: int) -> str:
    """Generates a random decimal string of a given length."""
    chars = "0123456789"
    first = random.choice(chars[1:])  # Ensure it doesn't start with 0
    rest = ''.join(random.choice(chars) for _ in range(length - 1))
    return first + rest


def worker_single_mul_strategy(n: int, strategy_base: int) -> tuple[int, int, int, float]:
    """
    Executes exactly ONE multiplication test.
    Baseline is Base 10.
    """
    str_a = generate_decimal(n)
    str_b = generate_decimal(n)

    stats = OperationStats()

    if strategy_base == 10:
        a10 = BigInt.from_string(str_a, 10, stats)
        b10 = BigInt.from_string(str_b, 10, stats)

        # Reset stats to count ONLY the multiplication operations
        stats.reset()
        t0 = time.perf_counter()
        _ = a10 * b10
        t1 = time.perf_counter()

    else:
        a_init = BigInt.from_string(str_a, 10, stats)
        b_init = BigInt.from_string(str_b, 10, stats)

        # Reset stats to count the ENTIRE pipeline: Conversions + Multiplication + Final Conversion
        stats.reset()
        t0 = time.perf_counter()

        a_conv = a_init.convert_to(strategy_base)
        b_conv = b_init.convert_to(strategy_base)

        c_conv = a_conv * b_conv
        _ = c_conv.convert_to(10)

        t1 = time.perf_counter()

    return n, strategy_base, stats.get_total(), t1 - t0


def run_optimized_multiplication_experiment() -> None:
    lengths = [100, 250, 500, 1000]
    strategies = [10, 2, 8, 16, 32]
    runs_per_length = 3

    raw_results: defaultdict[int, defaultdict[int, dict[str, list[Any]]]] = defaultdict(
        lambda: defaultdict(lambda: {'ops': [], 'times': []})
    )

    print("Submitting Base 10 multiplication tasks to the CPU pool... Please wait.")
    print(f"{'N (digits)':<12} | {'Base 10 Ops':<12} | {'Base 2 Ops':<12} | {'Base 10 (s)':<12} | {'Base 2 (s)':<12}")
    print("-" * 75)

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(worker_single_mul_strategy, n, base)
            for n in lengths
            for base in strategies
            for _ in range(runs_per_length)
        ]

        for future in as_completed(futures):
            n, base, ops, t = future.result()
            raw_results[n][base]['ops'].append(ops)
            raw_results[n][base]['times'].append(t)


    data_ops: dict[int, list[int]] = {10: [], 2: [], 8: [], 16: [], 32: []}
    data_time: dict[int, list[float]] = {10: [], 2: [], 8: [], 16: [], 32: []}
    sorted_lengths = sorted(lengths)

    for n in sorted_lengths:
        for b in strategies:
            median_ops = int(statistics.median(raw_results[n][b]['ops']))
            median_time = statistics.median(raw_results[n][b]['times'])

            data_ops[b].append(median_ops)
            data_time[b].append(median_time)

        print(f"{n:<12} | {data_ops[10][-1]:<12} | {data_ops[2][-1]:<12} | {data_time[10][-1]:<12.5f} | {data_time[2][-1]:<12.5f}")


    _ , (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    colors = {10: 'red', 2: 'purple', 8: 'orange', 16: 'blue', 32: 'green'}

    for b in strategies:
        label = 'Direct Base 10' if b == 10 else f'Convert -> Mul -> Back (Base {b})'
        ax1.plot(sorted_lengths, data_ops[b], marker='o', color=colors[b], label=label)
        ax2.plot(sorted_lengths, data_time[b], marker='s', color=colors[b], label=label)

    ax1.set_title('Operations C(n): Direct Base 10 vs Conversion')
    ax1.set_xlabel('Length of decimal string (N digits)')
    ax1.set_ylabel('Total Operations C(n)')
    ax1.grid(True)
    ax1.legend()

    ax2.set_title('Time T(n): Direct Base 10 vs Conversion')
    ax2.set_xlabel('Length of decimal string (N digits)')
    ax2.set_ylabel('Time T(n) (seconds)')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig(ROOT_DIR / "results" / FILE_PATH, dpi=300)
    plt.show()

if __name__ == "__main__":
    run_optimized_multiplication_experiment()