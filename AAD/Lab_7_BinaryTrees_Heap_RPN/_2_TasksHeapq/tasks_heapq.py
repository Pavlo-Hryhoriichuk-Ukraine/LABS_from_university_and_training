import heapq
import math


def distribute_tasks(A: list[int], k: int) -> tuple[list[list[int]], list[int], int]:

    if k < 1:
        raise ValueError("Кількість робітників k має бути не менше 1.")
    if len(A) < 1:
        raise ValueError("Список завдань A не може бути порожнім.")
    if any(t <= 0 for t in A):
        raise ValueError("Тривалість кожного завдання має бути додатною.")

    lower_bound = max(max(A), math.ceil(sum(A) / k))

    sorted_tasks = sorted(enumerate(A), key=lambda item: item[1], reverse=True)

    groups: list[list[int]] = [[] for _ in range(k)]

    heap: list[tuple[int, int]] = [(0, i) for i in range(k)]
    heapq.heapify(heap)

    for orig_idx, duration in sorted_tasks:
        curr_load, worker_id = heapq.heappop(heap)
        groups[worker_id].append(orig_idx)
        heapq.heappush(heap, (curr_load + duration, worker_id))

    loads = [0] * k
    for load, worker_id in heap:
        loads[worker_id] = load

    return groups, loads, lower_bound


if __name__ == "__main__":
    test_cases = [
        ("Тест 1 (із методички)", [7, 5, 4, 3, 3, 2], 3),
        ("Тест2(робітників більше ніж задач)", [4, 4], 5),
        ("Тест 3 (однакова тривалість)", [6, 6, 6, 6, 6, 6], 3),
        ("Тест 4 (домінуюче довге завдання)", [20, 3, 3, 2, 2], 2),
        ("Тест 5 (ідеально збалансований)", [8, 7, 6, 5, 4, 3, 2, 1], 4),
        ("Тест6(нерівномірний спектр робіт)", [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 3),
        ("Тест 7 (один робітник)", [5, 10, 15], 1),
    ]

    print("=" * 95)
    print(
        f"{'Назва тесту':<34} | {'k':<3} | {'Нижня межа':<11} | {'LPT факт':<9} | {'Різниця':<8} | {'Навантаження (loads)'}"
    )
    print("-" * 95)

    for name, tasks, k_workers in test_cases:
        task_groups, worker_loads, bound = distribute_tasks(tasks, k_workers)
        makespan = max(worker_loads)
        diff = makespan - bound

        all_assigned = sorted(i for g in task_groups for i in g)
        assert all_assigned == list(range(len(tasks)))
        assert sum(worker_loads) == sum(tasks)

        print(
            f"{name:<34} | "
            f"{k_workers:<3} | "
            f"{bound:<11} | "
            f"{makespan:<9} | "
            f"{diff:<8} | "
            f"{worker_loads}"
        )

    print("=" * 95)
