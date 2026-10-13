from random import shuffle, randint


def partition(arr, start, end, pivot_val):
    for i in range(start, end):
        if arr[i] == pivot_val:
            arr[i], arr[end] = arr[end], arr[i]
            break

    separator = start
    for i in range(start, end):
        if arr[i] < pivot_val:
            arr[i], arr[separator] = arr[separator], arr[i]
            separator += 1

    arr[separator], arr[end] = arr[end], arr[separator]

    return separator


def adapted_quicksort(nuts, bolts, start, end) -> None:
    if start >= end:
        return

    pivot_nut_index = randint(start, end)
    pivot_nut = nuts[pivot_nut_index]

    pivot_index = partition(bolts, start, end, pivot_nut)

    pivot_bolt = bolts[pivot_index]
    partition(nuts, start, end, pivot_bolt)

    adapted_quicksort(nuts, bolts, start, pivot_index - 1)
    adapted_quicksort(nuts, bolts, pivot_index + 1, end)


if __name__ == "__main__":
    nuts = [11, 23, 45, 28, 92, 18, 19, 20, 8, 7, 4, 32]

    bolts = nuts.copy()
    shuffle(bolts)

    adapted_quicksort(nuts, bolts, start=0, end=len(nuts) - 1)

    for pair in zip(nuts, bolts):
        print(pair)