import time
import random
import matplotlib.pyplot as plt
from turing_machine import TuringMachine, TypeTuringComandTable

def benchmark_turing_machine(transitions, end_states, lengths: list[int]):
    step_counts = []
    execution_times = []

    for length in lengths:
        test_string = "".join(random.choice(['0', '1']) for _ in range(length))

        tm = TuringMachine(
            machine_code_table=transitions,
            state='q0',
            end_states=end_states,
            blank_symbol='_'
        )

        start_time = time.perf_counter()
        tm.run(test_string, on_step=None)
        elapsed_time = time.perf_counter() - start_time

        step_counts.append(tm._steps)
        execution_times.append(elapsed_time)

    return step_counts, execution_times


def plot_complexity_results(lengths: list[int], steps: list[int], times: list[int]) -> None:

    plt.figure(figsize=(13, 5))
    # Subplot 1: Algorithmic steps vs Input length
    plt.subplot(1, 2, 1)
    plt.plot(lengths, steps, marker='o', color='tab:blue', label='Measured Steps')
    plt.title("Step Count vs Input Size", fontsize=11, fontweight='bold')
    plt.xlabel("Input Size (N)", fontsize=10)
    plt.ylabel("Number of Steps", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    # Subplot 2: Physical execution time vs Input length
    plt.subplot(1, 2, 2)
    plt.plot(lengths, times, marker='s', color='tab:red', label='Execution Time')
    plt.title("Execution Time vs Input Size", fontsize=11, fontweight='bold')
    plt.xlabel("Input Size (N)", fontsize=10)
    plt.ylabel("Execution Time (seconds)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    test_table: TypeTuringComandTable = {
        ('q0', '0'): ('q0', '1', 'R'),
        ('q0', '1'): ('q0', '0', 'R'),
        ('q0', '_'): ('q_done', '_', 'N')
    }
    terminal_states = {'q_done': None}

    test_lengths = [10, 20, 50, 80, 100, 200, 250, 400, 500, 700, 1000, 1300, 1500, 1800, 2000]

    steps, times = benchmark_turing_machine(test_table, terminal_states, test_lengths)
    plot_complexity_results(test_lengths, steps, times)