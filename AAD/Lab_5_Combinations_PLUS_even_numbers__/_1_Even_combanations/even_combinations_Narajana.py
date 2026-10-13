import numpy as np
from numba import njit
from collections.abc import Generator
import collections
import math

@njit
def _next_permutation_inplace(arr: np.ndarray) -> bool:
    n = len(arr)

    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1

    if i < 0:
        return False

    j = n - 1
    while arr[i] >= arr[j]:
        j -= 1

    arr[i], arr[j] = arr[j], arr[i]

    left = i + 1
    right = n - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    return True

class LexicographicalPermutations:
    def __init__(self, elements: list[int]):
        self._state = np.array(sorted(elements), dtype=np.int32)

    def generate(self) -> Generator[np.ndarray, None, None]:
        yield self._state.copy()

        while _next_permutation_inplace(self._state):
            yield self._state.copy()





def _next_combination_inplace(array: list[int], k: int) -> bool:
    for i in range(len(array) - 1, -1, -1):
        if array[i] < k:
            array[i] += 1

            for j in range(i + 1, len(array)):
                array[j] = array[i]
            return True

    return False


class LexicographicallyOrderedCombinations:
    def __init__(self, lenght: int,  k: int):
        self._state = [1] * lenght
        self._k = k

    def generate(self):
        yield self._state.copy()

        while _next_combination_inplace(self._state, self._k):
            yield self._state.copy()


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    ceil = math.isqrt(n)
    for number in range(2, ceil + 1):
        if n % number == 0:
            return False
    return True


if __name__ == "__main__":
    N_DICE = 4
    K_FACES = 10

    total_outcomes = K_FACES ** N_DICE

    favorable_a = 0
    favorable_b = 0

    combinations = LexicographicallyOrderedCombinations(N_DICE, K_FACES)

    for combo in combinations.generate():
        if is_prime(sum(combo)):

            #A: Mathematical (Combinations + Formula)
            # Calculate the multinomial coefficient: N! / (c1! * c2! * ... * cm!)
            counts = collections.Counter(combo)
            denominator = math.prod(math.factorial(c) for c in counts.values())
            permutations_count = math.factorial(N_DICE) // denominator

            favorable_a += permutations_count

            # SOLUTION B: Algorithmic (Permutations Generator)
            permutations = LexicographicalPermutations(combo)
            for _ in permutations.generate():
                favorable_b += 1

    probability_a = favorable_a / total_outcomes
    probability_b = favorable_b / total_outcomes

    print(f"Total possible outcomes: {total_outcomes}")
    print(f"Solution A (Math) -> Favorable: {favorable_a}, Probability: {probability_a:.6f}")
    print(f"Solution B (Algo) -> Favorable: {favorable_b}, Probability: {probability_b:.6f}")

    assert favorable_a == favorable_b, "Both solutions must yield the same result!"