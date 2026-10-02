from random import shuffle, randint

def partition(arr, start, end, pivot_val):
    """
    Helper function that partitions the array around the pivot_val.
    Returns the final index where the pivot is placed.
    """
    # 1. Find the pivot in the array and swap it to the end
    for i in range(start, end): # Iterate up to 'end' because 'end' is an inclusive index
        if arr[i] == pivot_val:
            arr[i], arr[end] = arr[end], arr[i]
            break

    # 2. Iterate through the array and move smaller elements to the left
    separator = start  # Start strictly from the boundary of the subproblem!
    for i in range(start, end):
        if arr[i] < pivot_val:
            arr[i], arr[separator] = arr[separator], arr[i]
            separator += 1

    # 3. Restore the pivot from the end to its rightful place (at separator)
    arr[separator], arr[end] = arr[end], arr[separator]

    return separator


def adapted_quicksort(nuts, bolts, start, end) -> None:
    # Base case: if the array is empty or has only 1 element
    if start >= end:
        return

    # 1. Choose a random nut as the pivot
    pivot_nut_index = randint(start, end)
    pivot_nut = nuts[pivot_nut_index]

    # 2. The nut sorts the bolts (getting the final index where they match)
    pivot_index = partition(bolts, start, end, pivot_nut)

    # 3. The matched bolt now sorts the nuts
    pivot_bolt = bolts[pivot_index]
    partition(nuts, start, end, pivot_bolt)

    # 4. Recursion for the left and right parts (excluding the pivot_index itself!)
    adapted_quicksort(nuts, bolts, start, pivot_index - 1)
    adapted_quicksort(nuts, bolts, pivot_index + 1, end)


if __name__ == "__main__":
    nuts = [11, 23, 45, 28, 92, 18, 19, 20, 8, 7, 4, 32]

    # Proper in-place shuffling
    bolts = nuts.copy()
    shuffle(bolts)

    # Call with the correct 'end' index (inclusive)
    adapted_quicksort(nuts, bolts, start=0, end=len(nuts) - 1)

    # Neatly print the matched pairs
    for pair in zip(nuts, bolts):
        print(pair)