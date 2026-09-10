import time
import random
import statistics
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from typing import Any
from pathlib import Path
from operations import OperationStats, BigInt

ROOT_DIR = Path(__file__).parent
BASE = 2
FILE_NAME = f"add_base_{BASE}.png"


def generate_random_number_string(length: int, base: int = 10) -> str:
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUV"[:base]
    first = random.choice(chars[1:])
    rest = ''.join(random.choice(chars) for _ in range(length - 1))
    return first + rest


def worker_single_addition(n: int, base: int) -> tuple[int, int, float]:
    str_a = generate_random_number_string(n, base)
    str_b = generate_random_number_string(n, base)

    stats = OperationStats()
    big_a = BigInt.from_string(str_a, base, stats)
    big_b = BigInt.from_string(str_b, base, stats)

    # Reset stats to ignore parsing operations
    stats.reset()

    start_time = time.perf_counter()
    _ = big_a + big_b
    end_time = time.perf_counter()

    return n, stats.get_total(), end_time - start_time

def run_optimized_addition_experiment() -> None:
    lengths = [10_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    runs_per_length = 5

    raw_results: defaultdict[int, dict[str, list[Any]]] = defaultdict(lambda: {'ops': [], 'times': []})

    print("Submitting tasks to the CPU pool... Please wait.")
    print(f"{'Length (N)':<12} | {'Ops C(N)':<15} | {'Time T(N) (s)':<15}")
    print("-" * 45)

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(worker_single_addition, n, BASE)
            for n in lengths
            for _ in range(runs_per_length)
        ]

        # as_completed yields tasks exactly as they finish, keeping the UI responsive
        for future in as_completed(futures):
            n, ops, t = future.result()
            raw_results[n]['ops'].append(ops)
            raw_results[n]['times'].append(t)


    results_c: list[int] = []
    results_t: list[float] = []

    for n in sorted(lengths):
        median_ops = int(statistics.median(raw_results[n]['ops']))
        median_time = statistics.median(raw_results[n]['times'])

        results_c.append(median_ops)
        results_t.append(median_time)

        print(f"{n:<12} | {median_ops:<15} | {median_time:<15.5f}")


    _ , (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(lengths, results_c, marker='o', color='b', label='Empirical C(n)')
    ax1.set_title('Operations vs Number Length (Addition)')
    ax1.set_xlabel('Number of digits (n)')
    ax1.set_ylabel('Total Elementary Operations C(n)')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(lengths, results_t, marker='s', color='r', label='Empirical Time T(n)')
    ax2.set_title('Execution Time vs Number Length (Addition)')
    ax2.set_xlabel('Number of digits (n)')
    ax2.set_ylabel('Execution Time T(n) (seconds)')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(ROOT_DIR / "results" / FILE_NAME, dpi=300)
    plt.show()

if __name__ == "__main__":
    run_optimized_addition_experiment()