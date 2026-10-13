import time
from typing import TypeAlias
from collections.abc import Generator

Item: TypeAlias = tuple[float, float]
Inventory: TypeAlias = list[Item]


def generate_partitions(
    elements: Inventory,
    max_capacity: float,
    use_pruning: bool = True,
    index: int = 0,
    rooms: list[Inventory] | None = None,
) -> Generator[list[Inventory], None, None]:
    if rooms is None:
        rooms = []

    if index == len(elements):
        yield [room.copy() for room in rooms]
        return

    current_elem = elements[index]
    elem_weight = current_elem[0]

    can_open_new = (not use_pruning) or (elem_weight <= max_capacity)
    if can_open_new:
        rooms.append([current_elem])
        yield from generate_partitions(
            elements, max_capacity, use_pruning, index + 1, rooms
        )
        rooms.pop()

    for room in rooms:
        current_room_weight = sum(item[0] for item in room)

        can_add_to_room = (not use_pruning) or (
            current_room_weight + elem_weight <= max_capacity
        )
        if can_add_to_room:
            room.append(current_elem)
            yield from generate_partitions(
                elements, max_capacity, use_pruning, index + 1, rooms
            )
            room.pop()


def run_benchmark(items: Inventory, capacity: float, use_pruning: bool):
    mode_name = "З ВІДСІКАННЯМ (Pruning)" if use_pruning else "БЕЗ ВІДСІКАННЯ (Full Bell Search)"
    print(f"\n--- Запуск: {mode_name} ---")

    start_time = time.perf_counter()

    partitions_count = 0
    max_utility = 0.0
    best_backpack: Inventory | None = None

    for lst_backpack in generate_partitions(items, capacity, use_pruning=use_pruning):
        partitions_count += 1
        for backpack in lst_backpack:
            current_weight = sum(item[0] for item in backpack)
            current_utility = sum(item[1] for item in backpack)

            if current_weight <= capacity and current_utility > max_utility:
                max_utility = current_utility
                best_backpack = backpack

    elapsed = time.perf_counter() - start_time

    print(f"Час виконання: {elapsed:.4f} секунд")
    print(f"Згенеровано розбиттів: {partitions_count}")
    print(f"Максимальна корисність: {max_utility:.1f}")
    print(f"Найкращий набір (вага={sum(x[0] for x in best_backpack):.1f} кг): {best_backpack}") # type: ignore


if __name__ == "__main__":
    items_pool: Inventory = [
        (5.0, 150.0),   # Item 0
        (3.5, 90.0),    # Item 1
        (2.0, 110.0),   # Item 2
        (4.0, 190.0),   # Item 3
        (9.5, 352.0),   # Item 4
        (1.0, 42.0),    # Item 5
        (9.0, 32.0),    # Item 6
        (2.5, 93.0),    # Item 7
        (7.0, 93.0),    # Item 8
        (1.0, 64.0),    # Item 9
        (3.0, 120.0),   # Item 10
    ]

    MAX_WEIGHT_CAPACITY = 10.0

    print(f"Пул предметів: {len(items_pool)} шт. Ліміт ваги: {MAX_WEIGHT_CAPACITY} кг.")

    run_benchmark(items_pool, MAX_WEIGHT_CAPACITY, use_pruning=True)

    run_benchmark(items_pool, MAX_WEIGHT_CAPACITY, use_pruning=False)