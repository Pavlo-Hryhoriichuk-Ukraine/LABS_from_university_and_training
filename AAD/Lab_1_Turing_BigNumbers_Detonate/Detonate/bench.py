import os
import matplotlib.pyplot as plt
from functools import cache
from pathlib import Path

ROOT_PATH = Path(__file__).parent

@cache
def hybrid_worst_case_trials(n: int, k: int) -> int:
    # Base cases
    if n <= 0:
        return 0
    if k == 1:
        return n

    mid = (1 + n) // 2 # middle of our all path

    # Case A: Munition detonates
    # We must search the floors below 'mid' (mid - 1 floors)
    # We lose 1 munition.
    detonates_case = hybrid_worst_case_trials(mid - 1, k - 1)

    # Case B: Munition does NOT detonate
    # We must search the floors above 'mid' (n - mid floors)
    # We keep all current munitions.
    survives_case = hybrid_worst_case_trials(n - mid, k)

    # The worst case is the maximum of the two possibilities,
    # plus 1 for the drop we just made.
    return 1 + max(detonates_case, survives_case)



def plot_hybrid_experiments() -> None:
    """
    Generates and saves the graph comparing worst-case trials for different k values.
    """
    # Test heights from 10 to 1000 with a step of 10
    n_values = list(range(10, 1001, 10))
    k_values = [1, 2, 3, 10]

    plt.figure(figsize=(10, 6))

    colors = {1: 'red', 2: 'orange', 3: 'blue', 10: 'green'}

    for k in k_values:
        trials = [hybrid_worst_case_trials(n, k) for n in n_values]

        label = f'k = {k}'
        if k == 1:
            label += ' (Pure Linear)'
        elif k >= 10:
            label += ' (Pure Binary)'

        plt.plot(n_values, trials, label=label, color=colors[k], linewidth=2)

    plt.title('Worst-Case Trials vs Drone Maximum Height (Hybrid Algorithm)')
    plt.xlabel('Maximum Height / Number of Floors (n)')
    plt.ylabel('Maximum Number of Trials in Worst Case')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot
    res_dir = ROOT_PATH / "results"
    os.makedirs(res_dir, exist_ok=True)
    file_path = res_dir / "hybrid_drone_experiment.png"
    plt.savefig(file_path, dpi=300)
    print(f"Graph saved successfully to {file_path}")
    plt.show()

if __name__ == "__main__":
    print("Calculating worst-case complexities and generating plot...")
    plot_hybrid_experiments()