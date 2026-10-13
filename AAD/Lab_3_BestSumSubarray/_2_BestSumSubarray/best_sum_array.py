def find_max_crossing_subarray(arr: list[int], low: int, mid: int, high: int) -> dict:
    # 1. Йдемо від центру вліво
    left_sum = float('-inf')
    current_sum = 0
    max_left = mid # Запам'ятовуємо індекс найкращого лівого краю

    for i in range(mid, low - 1, -1):
        current_sum += arr[i]
        if current_sum > left_sum:
            left_sum = current_sum
            max_left = i

    # 2. Йдемо від центру вправо
    right_sum = float('-inf')
    current_sum = 0
    max_right = mid + 1 # Запам'ятовуємо індекс найкращого правого краю

    for j in range(mid + 1, high + 1):
        current_sum += arr[j]
        if current_sum > right_sum:
            right_sum = current_sum
            max_right = j

    # 3. Пакуємо результат у словник, як ти й просив
    return {
        "sum": left_sum + right_sum,
        "subarray": arr[max_left : max_right + 1] # Зріз масиву від лівого до правого краю
    }


def find_maximum_subarray(arr: list[int], low: int, high: int) -> dict:
    if low == high:
        return {
            "sum": arr[low],
            "subarray": [arr[low]]
        }

    mid = (low + high) // 2

    left_dict = find_maximum_subarray(arr, low, mid)
    right_dict = find_maximum_subarray(arr, mid + 1, high)
    cross_dict = find_max_crossing_subarray(arr, low, mid, high)

    best_result = max([left_dict, right_dict, cross_dict], key=lambda item: item["sum"])

    return best_result


if __name__ == '__main__':
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

    result = find_maximum_subarray(arr, 0, len(arr) - 1)

    print(f"Початковий масив: {arr}")
    print("-" * 30)
    print(f"Максимальна сума: {result['sum']}")
    print(f"Сам підмасив:     {result['subarray']}")