import time
import random
import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
import matplotlib.pyplot as plt

from BigInt_2_0_ import BigInt


# Assuming BigInt is in a file named big_int.py
# from big_int import BigInt

@dataclass
class BenchmarkTask:
    """Represents a single multiplication task for a worker process."""
    n_digits: int
    algo_name: str
    str_a: str
    str_b: str

@dataclass
class BenchmarkResult:
    """Stores the execution time and verification status of a task."""
    n_digits: int
    algo_name: str
    execution_time: float
    is_correct: bool


def execute_multiplication_task(task: BenchmarkTask) -> BenchmarkResult:
    a = BigInt.from_string(task.str_a, 10)
    b = BigInt.from_string(task.str_b, 10)

    start_time = time.perf_counter()
    if task.algo_name == "Schoolbook (O(n^2))":
        res = a * b
    elif task.algo_name == "Karatsuba (O(n^1.585))":
        res = a.mul_karatsuba_recursively(b)
    elif task.algo_name == "Toom-Cook 3 (O(n^1.465))":
        res = a.mul_toom_cook_3_recursively(b)
    else:
        raise ValueError(f"Unknown algorithm: {task.algo_name}")
    end_time = time.perf_counter()

    return BenchmarkResult(
        n_digits=task.n_digits,
        algo_name=task.algo_name,
        execution_time=end_time - start_time,
        is_correct=True
    )

class ParallelMultiplicationBenchmark:
    """
    Orchestrates the parallel execution of BigInt multiplication algorithms.
    """

    def __init__(self, digit_sizes: list[int], num_trials: int = 2):
        self.digit_sizes = digit_sizes
        self.num_trials = num_trials
        self.algorithms = [
            "Schoolbook (O(n^2))",
            "Karatsuba (O(n^1.585))",
            "Toom-Cook 3 (O(n^1.465))"
        ]
        self.results_map: dict[str, dict[int, list[float]]] = {
            algo: {n: [] for n in digit_sizes} for algo in self.algorithms
        }

    @staticmethod
    def _generate_n_digit_number(n: int) -> str:
        """Generates a random n-digit string representation of an integer."""
        first_digit = str(random.randint(1, 9))
        rest_digits = ''.join(str(random.randint(0, 9)) for _ in range(n - 1))
        return first_digit + rest_digits

    def run(self) -> None:
        """Generates tasks and processes them concurrently."""
        tasks: list[BenchmarkTask] = []

        print("Generating large random numbers for tasks...")
        for n in self.digit_sizes:
            for _ in range(self.num_trials):
                str_a = self._generate_n_digit_number(n)
                str_b = self._generate_n_digit_number(n)

                for algo in self.algorithms:
                    tasks.append(BenchmarkTask(n, algo, str_a, str_b))

        optimal_workers = max(1, os.cpu_count() or 0 - 1)
        print(f"Distributing {len(tasks)} heavy tasks across {optimal_workers} CPU cores...")

        # Execute tasks in parallel
        with ProcessPoolExecutor(max_workers=optimal_workers) as executor:
            futures = [executor.submit(execute_multiplication_task, task) for task in tasks]

            for future in as_completed(futures):
                res: BenchmarkResult = future.result()

                if not res.is_correct:
                    print(f"CRITICAL: {res.algo_name} failed at {res.n_digits} digits!")

                self.results_map[res.algo_name][res.n_digits].append(res.execution_time)
                print(f"Completed: {res.algo_name} | {res.n_digits} digits | {res.execution_time:.4f}s")

        self._print_summary()

    def _print_summary(self) -> None:
        """Prints the aggregated average times in a formatted table."""
        print(f"\n{'n digits':<10} | {'Schoolbook (s)':<18} | {'Karatsuba (s)':<18} | {'Toom-Cook (s)':<18}")
        print("-" * 73)

        for n in self.digit_sizes:
            avg_school = sum(self.results_map["Schoolbook (O(n^2))"][n]) / self.num_trials
            avg_karat = sum(self.results_map["Karatsuba (O(n^1.585))"][n]) / self.num_trials
            avg_toom = sum(self.results_map["Toom-Cook 3 (O(n^1.465))"][n]) / self.num_trials

            print(f"{n:<10} | {avg_school:<18.4f} | {avg_karat:<18.4f} | {avg_toom:<18.4f}")

    def plot(self) -> None:
        """Renders the Matplotlib chart."""
        plt.figure(figsize=(12, 7))

        for algo, marker in zip(self.algorithms, ['o', 's', '^']):
            averages = [sum(self.results_map[algo][n]) / self.num_trials for n in self.digit_sizes]
            plt.plot(self.digit_sizes, averages, label=algo, marker=marker, linewidth=2.5)

        plt.title('WITH THREADHOLE Parallel Performance Analysis of BigInt Multiplication', fontsize=15, fontweight='bold')
        plt.xlabel('Number of Digits (n)', fontsize=13)
        plt.ylabel('Average Execution Time (seconds)', fontsize=13)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Required for Windows multiprocessing compatibility
    multiprocessing.freeze_support()

    # Ready for massive numbers
    sizes_to_test = [1000, 3000, 5000, 7000, 10000, 14000, 17000, 20000, 22000, 27000, 31000]

    benchmark = ParallelMultiplicationBenchmark(digit_sizes=sizes_to_test, num_trials=3)
    benchmark.run()
    benchmark.plot()