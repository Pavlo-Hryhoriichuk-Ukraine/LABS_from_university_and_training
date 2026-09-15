import time
import matplotlib.pyplot as plt

def fibon_search(array: list[int], goal_num: int) -> int:

    n = len(array)
    if n == 0:
        return -1

    F_k2 = 0
    F_k1 = 1
    F_k = F_k2 + F_k1

    while F_k < n:
        F_k2 = F_k1
        F_k1 = F_k
        F_k = F_k2 + F_k1

    offset = -1

    while F_k > 1:
        index = offset + F_k2
        if index >= n:
            index = n - 1

        elem = array[index]

        if elem < goal_num:
            offset = index
            F_k = F_k1
            F_k1 = F_k2
            F_k2 = F_k - F_k1

        elif elem > goal_num:
            F_k = F_k2
            F_k1 = F_k1 - F_k2
            F_k2 = F_k - F_k1

        else:
            return index

    # if element IS
    if F_k1 == 1 and (offset + 1 < n) and array[offset + 1] == goal_num:
        return offset + 1

    return -1


def binary_search(array: list[int], goal_num: int) -> int:

    low = 0
    high = len(array) - 1

    while low <= high:
        mid = (low + high) // 2
        elem = array[mid]

        if elem < goal_num:
            low = mid + 1
        elif elem > goal_num:
            high = mid - 1
        else:
            return mid

    return -1


def run_benchmark() -> None:

    sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
    num_trials = 1000

    results_fib = []
    results_bin = []

    print(f"{'Array Size (N)':<15} | {'Binary Search (s)':<20} | {'Fibonacci Search (s)':<20}")
    print("-" * 60)

    for n in sizes:
        arr = list(range(n))

        # 2. Choose a number guaranteed NOT to be in the array (worst-case scenario)
        target = n + 10


        start_bin = time.perf_counter()
        for _ in range(num_trials):
            binary_search(arr, target)
        bin_avg_time = (time.perf_counter() - start_bin) / num_trials
        results_bin.append(bin_avg_time)


        start_fib = time.perf_counter()
        for _ in range(num_trials):
            fibon_search(arr, target)
        fib_avg_time = (time.perf_counter() - start_fib) / num_trials
        results_fib.append(fib_avg_time)


        print(f"{n:<15} | {bin_avg_time:<20.8f} | {fib_avg_time:<20.8f}")

    plot_results(sizes, results_bin, results_fib)


def plot_results(sizes: list[int], bin_times: list[float], fib_times: list[float]) -> None:
    """
    Builds and displays a Matplotlib graph of the execution times.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bin_times, marker='o', label='Binary Search (O(log n))', linewidth=2)
    plt.plot(sizes, fib_times, marker='s', label='Fibonacci Search (O(log n))', linewidth=2)

    plt.title('Performance Comparison: Binary vs Fibonacci Search (Worst Case)', fontsize=14, fontweight='bold')
    plt.xlabel('Array Size (N)', fontsize=12)
    plt.ylabel('Average Execution Time (seconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)

    # Use logarithmic scale for X-axis since sizes grow exponentially
    plt.xscale('log')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_benchmark()