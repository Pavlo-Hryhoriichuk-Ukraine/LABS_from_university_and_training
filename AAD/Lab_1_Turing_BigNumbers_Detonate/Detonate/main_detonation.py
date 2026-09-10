def simulate_hybrid_drone_drop(n: int, k: int, n_max: int) -> None:
    """
    Simulates a hybrid search strategy.
    If k >= 2: Performs binary search (halves the interval).
    If k == 1: Switches to linear search (checks floor by floor from the bottom).
    """
    print(f"\n--- HYBRID SEARCH SIMULATION (n={n}, k={k}, n_max={n_max}) ---")

    low = 1
    high = n
    munitions = k
    trial = 1

    while low <= high and munitions > 0:
        if munitions >= 2:
            drop_height = (low + high) // 2
        else:
            # start liniar
            drop_height = low

        is_detonated = drop_height > n_max
        result_str = "DETONATED" if is_detonated else "DID NOT DETONATE"

        if is_detonated:
            munitions -= 1

        print(f"Trial {trial}: height {drop_height} m. Result: {result_str}. Munitions left: {munitions}.")

        if is_detonated:
            high = drop_height - 1
        else:
            low = drop_height + 1

        trial += 1

    if low > n and n_max >= n:
        print("Conclusion: Use a drone with a higher flight altitude")
    else:
        print(f"Conclusion: Maximum safe height n_max = {low - 1} m")


if __name__ == "__main__":
    # Test 1: k=1 -> Acts purely as Linear Search
    simulate_hybrid_drone_drop(n=10, k=1, n_max=7)

    # Test 2: k=2 -> Jumps to middle, breaks, then goes linearly
    simulate_hybrid_drone_drop(n=100, k=2, n_max=42)

    # Test 3: Large k -> Acts purely as Binary Search
    simulate_hybrid_drone_drop(n=100, k=10, n_max=85)