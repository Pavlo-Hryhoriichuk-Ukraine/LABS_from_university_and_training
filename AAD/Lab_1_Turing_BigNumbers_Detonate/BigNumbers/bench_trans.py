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


BASE_FROM  = 16
BASE_TO = 2
FILE_NAME = f"conversion_from_{BASE_FROM}_to_{BASE_TO}.png"



def generate_random_number_string(length: int, base: int = 10) -> str:
    """Generates a random number string of a given length for a specified base."""
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUV"[:base]
    first = random.choice(chars[1:])
    rest = ''.join(random.choice(chars) for _ in range(length - 1))
    return first + rest


def worker_single_conversion(n: int, base_from: int, base_to: int) -> tuple[int, int, float]:
    """
    Executes exactly ONE base conversion operation.
    Perfect for CPU load balancing.
    """
    num_str = generate_random_number_string(n, base_from)
    stats = OperationStats()
    big_num = BigInt.from_string(num_str, base_from, stats)

    # Reset stats so we ONLY measure the convert_to operation, not from_string
    stats.reset()

    start_time = time.perf_counter()
    _ = big_num.convert_to(base_to)
    end_time = time.perf_counter()

    return n, stats.get_total(), end_time - start_time

def run_optimized_conversion_experiment() -> None:
    lengths = [100, 250, 500, 1000, 1500, 2000, 3000, 4000]
    runs_per_length = 3

    raw_results: defaultdict[int, dict[str, list[Any]]] = defaultdict(lambda: {'ops': [], 'times': []})

    print("Submitting conversion tasks to the CPU pool... Please wait.")
    print(f"{'Length (N)':<12} | {'Base Transition':<17} | {'Ops C(N)':<15} | {'Time T(N) (s)':<15}")
    print("-" * 65)

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(worker_single_conversion, n, BASE_FROM, BASE_TO)
            for n in lengths
            for _ in range(runs_per_length)
        ]

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

        transition = f"{BASE_FROM} -> {BASE_TO}"
        print(f"{n:<12} | {transition:<17} | {median_ops:<15} | {median_time:<15.5f}")

    _ , (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(lengths, results_c, marker='o', color='b', label='Empirical C(n)')
    ax1.set_title('Operations vs Number Length (Base Conversion)')
    ax1.set_xlabel('Number of digits (n)')
    ax1.set_ylabel('Total Elementary Operations C(n)')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(lengths, results_t, marker='s', color='r', label='Empirical Time T(n)')
    ax2.set_title('Execution Time vs Number Length (Base Conversion)')
    ax2.set_xlabel('Number of digits (n)')
    ax2.set_ylabel('Execution Time T(n) (seconds)')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()

    os.makedirs("results", exist_ok=True)
    plt.savefig(ROOT_DIR / "results/" / FILE_NAME, dpi=300)
    plt.show()

if __name__ == "__main__":
    run_optimized_conversion_experiment()