from __future__ import annotations

class Database:
    def __init__(self, data: list[int], name: str = "DB") -> None:
        self._data = data
        self.name = name
        self.query_count = 0

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> int:
        self.query_count += 1
        return self._data[index]

    def reset_query_count(self) -> None:
        self.query_count = 0


def find_median_logarithmic_recursive(
    db1: Database,
    db2: Database,
    start1: int,
    end1: int,
    start2: int,
    end2: int
) -> float:
    """
    Recursive median search in O(log n) time.
    """

    length = end1 - start1 + 1

    # 2. Base case 1 (1 element left in each array)
    if length == 1:
        return (db1[start1] + db2[start2]) / 2.0

    # 3. Base case 2 (2 elements left in each array)
    elif length == 2:

        elem_1_1 = db1[start1]
        elem_1_2 = db1[end1]

        elem_2_1 = db2[start2]
        elem_2_2 = db2[end2]

        left_max = max(elem_1_1, elem_2_1)
        right_min = min(elem_1_2, elem_2_2)
        return (left_max + right_min) / 2.0

    # 4. Find the middle indices of the current segments
    # Using shift from start!

    offset = (length - 1) // 2
    m1_idx = start1 + offset
    m2_idx = start2 + offset

    m1 = db1[m1_idx]
    m2 = db2[m2_idx]


    if m1 == m2:
        return float(m1)

    elif m1 < m2:
        if length % 2 == 1:
            # Odd length: medians might be the global median, keep them in range
            return find_median_logarithmic_recursive(db1, db2, m1_idx, end1, start2, m2_idx)
        else:
            # Even length: m1 is strictly too small, discard it completely
            return find_median_logarithmic_recursive(db1, db2, m1_idx + 1, end1, start2, m2_idx)

    else: # m1 > m2
        if length % 2 == 1:
            return find_median_logarithmic_recursive(db1, db2, start1, m1_idx, m2_idx, end2)
        else:
            # Even length: m2 is strictly too small, discard it completely
            return find_median_logarithmic_recursive(db1, db2, start1, m1_idx, m2_idx + 1, end2)

def find_median_merge_sort_naive(db1: Database, db2: Database) -> float:
    n = len(db1)
    if n == 0:
        return 0.0

    pointer_db1 = 0
    pointer_db2 = 0
    result_array = []

    # Cache the first elements
    val1 = db1[pointer_db1]
    val2 = db2[pointer_db2]

    while pointer_db1 < n and pointer_db2 < n:
        if val1 < val2:
            result_array.append(val1)
            pointer_db1 += 1
            # Make a new DB query ONLY if the pointer is still within bounds
            if pointer_db1 < n:
                val1 = db1[pointer_db1]
        else:
            result_array.append(val2)
            pointer_db2 += 1
            if pointer_db2 < n:
                val2 = db2[pointer_db2]

    while pointer_db1 < n:
        result_array.append(val1)
        pointer_db1 += 1
        if pointer_db1 < n:
            val1 = db1[pointer_db1]

    while pointer_db2 < n:
        result_array.append(val2)
        pointer_db2 += 1
        if pointer_db2 < n:
            val2 = db2[pointer_db2]

    # lenght always = 2*n
    median = (result_array[n - 1] + result_array[n]) / 2.0
    return median



if __name__ == "__main__":

    db_A = Database([1, 12, 15, 26, 38, 45, 50, 70, 85])
    db_B = Database([2, 13, 17, 30, 45, 60, 80, 90, 110])

    median_1 = find_median_logarithmic_recursive(db_A, db_B, 0, len(db_A) - 1, 0, len(db_B) - 1)
    print(f"Median_1: {median_1} ; fetch_times : DB_A : {db_A.query_count} , DB_B : {db_B.query_count}")

    db_A.reset_query_count() ; db_B.reset_query_count()

    median_2 = find_median_merge_sort_naive(db_A, db_B)
    print(f"Median_2: {median_2} ; fetch_times : DB_A : {db_A.query_count} , DB_B : {db_B.query_count}")