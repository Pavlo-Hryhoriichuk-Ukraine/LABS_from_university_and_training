
def find_max_array(array: list[int], k: int, start: int, end: int) -> float:
    """Finds the maximum subarray sum with a minimum length of k."""
    length = end - start + 1
    if length < k:
        return float('-inf')

    if start == end:
        return float(array[start]) if k <= 1 else float('-inf')

    mid = (start + end) // 2
    left_max = find_max_array(array, k, start, mid)
    right_max = find_max_array(array, k, mid + 1, end)

    left_tails = [0]
    curr_sum = 0
    for i in range(mid, start - 1, -1):
        curr_sum += array[i]
        left_tails.append(curr_sum)

    right_tails = [0]
    curr_sum = 0
    for i in range(mid + 1, end + 1):
        curr_sum += array[i]
        right_tails.append(curr_sum)

    len_r = len(right_tails)
    max_r = [float('-inf')] * len_r
    if len_r > 1:
        max_r[-1] = right_tails[-1]
        for i in range(len_r - 2, 0, -1):
            max_r[i] = max(right_tails[i], max_r[i + 1])

    max_crossing_sum = float('-inf')
    for i in range(1, len(left_tails)):
        req_j = max(1, k - i)
        if req_j < len_r:
            max_crossing_sum = max(max_crossing_sum, left_tails[i] + max_r[req_j])

    return max(left_max, right_max, max_crossing_sum)

if __name__ == "__main__":
    array = [7, 8, -10, 20, -25, 25, 5]
    print(find_max_array(array, 3, 0, len(array) - 1))
