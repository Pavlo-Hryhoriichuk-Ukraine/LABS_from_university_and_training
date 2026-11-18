import math
import random
import time
from collections.abc import Sequence


class AirDefense:
    def __init__(
        self, targets: Sequence[tuple[float, float, float]], point: tuple[float, float]
    ) -> None:
        """Ініціалізація та побудова дерева відрізків за O(N).

        :param targets: список кортежів координат цілей (x, y, h)
        :param point: координати точки ураження (px, py), висота z = 0
        """
        if not targets:
            raise ValueError("Список цілей не може бути порожнім.")

        self.n: int = len(targets)
        self.point: tuple[float, float] = point

        # Масив розміром 2N:
        # Індекси [1 .. n-1] — внутрішні вузли-предки
        # Індекси [n .. 2n-1] — листки (самі цілі)
        # Кожен елемент: (target_index, (x, y, h), distance)
        self.tree: list[tuple[int, tuple[float, float, float], float] | None] = [
            None
        ] * (2 * self.n)

        # 1. Заповнюємо листки у другій половині масиву
        for i in range(self.n):
            target = targets[i]
            dist = self._calc_dist(target)
            self.tree[self.n + i] = (i, target, dist)

        # 2. Побудова внутрішніх вузлів знизу вгору за O(N)
        for i in range(self.n - 1, 0, -1):
            left_child = self.tree[2 * i]
            right_child = self.tree[2 * i + 1]

            # Обираємо дитину з меншою відстанню
            if left_child is not None and right_child is not None:
                self.tree[i] = (
                    left_child if left_child[2] <= right_child[2] else right_child
                )
            elif left_child is not None:
                self.tree[i] = left_child
            else:
                self.tree[i] = right_child

    def _calc_dist(self, target: tuple[float, float, float]) -> float:
        """Обчислює евклідову відстань від цілі (x, y, h) до (px, py, 0)."""
        x, y, h = target
        px, py = self.point
        return math.hypot(x - px, y - py, h)

    def update(self, i: int, x: float, y: float, h: float) -> None:
        """Оновлює координати цілі i за O(log N)."""
        if not (0 <= i < self.n):
            raise IndexError(f"Індекс цілі {i} виходить за межі [0, {self.n - 1}].")

        # 1. Оновлюємо листок
        pos = self.n + i
        new_target = (x, y, h)
        new_dist = self._calc_dist(new_target)
        self.tree[pos] = (i, new_target, new_dist)

        # 2. Підйом угору та оновлення предків
        pos //= 2
        while pos > 0:
            left_child = self.tree[2 * pos]
            right_child = self.tree[2 * pos + 1]

            if left_child is not None and right_child is not None:
                self.tree[pos] = (
                    left_child if left_child[2] <= right_child[2] else right_child
                )
            elif left_child is not None:
                self.tree[pos] = left_child
            else:
                self.tree[pos] = right_child

            pos //= 2

    def nearest(
        self, l: int | None = None, r: int | None = None
    ) -> tuple[int, tuple[float, float, float], float]:
        """Повертає (номер, (x, y, h), відстань) найближчої цілі.

        Якщо l та r не вказані, повертає глобальний мінімум за O(1).
        Якщо вказані — шукає мінімум на підвідрізку [l, r] за O(log N).
        """
        if l is None:
            l = 0
        if r is None:
            r = self.n - 1

        if not (0 <= l <= r < self.n):
            raise ValueError(
                f"Некоректний діапазон [{l}, {r}] для кількості цілей {self.n}."
            )

        # Глобальний мінімум лежить безпосередньо в корені
        if l == 0 and r == self.n - 1:
            root = self.tree[1]
            if root is None:
                raise RuntimeError("Дерево порожнє.")
            return root

        # Запит на довільному підвідрізку індексів [l, r]
        l += self.n
        r += self.n
        best: tuple[int, tuple[float, float, float], float] | None = None

        while l <= r:
            if l % 2 == 1:
                item = self.tree[l]
                if item is not None and (best is None or item[2] < best[2]):
                    best = item
                l += 1
            if r % 2 == 0:
                item = self.tree[r]
                if item is not None and (best is None or item[2] < best[2]):
                    best = item
                r -= 1
            l //= 2
            r //= 2

        if best is None:
            raise RuntimeError("Не вдалося знайти найближчу ціль у діапазоні.")
        return best


class NaiveAirDefense:
    """Наївна реалізація без спеціальних структур даних (список + лінійний пошук)."""

    def __init__(
        self,
        targets: Sequence[tuple[float, float, float]],
        point: tuple[float, float],
    ) -> None:
        self.targets: list[tuple[float, float, float]] = list(targets)
        self.point: tuple[float, float] = point

    def _calc_dist(self, target: tuple[float, float, float]) -> float:
        x, y, h = target
        px, py = self.point
        return math.hypot(x - px, y - py, h)

    def update(self, i: int, x: float, y: float, h: float) -> None:
        """Оновлення за O(1)."""
        self.targets[i] = (x, y, h)

    def nearest(
        self, l: int | None = None, r: int | None = None
    ) -> tuple[int, tuple[float, float, float], float]:
        """Лінійний пошук мінімуму за O(R - L + 1) або O(N)."""
        if l is None:
            l = 0
        if r is None:
            r = len(self.targets) - 1

        best_idx = l
        best_target = self.targets[l]
        best_dist = self._calc_dist(best_target)

        for idx in range(l + 1, r + 1):
            target = self.targets[idx]
            dist = self._calc_dist(target)
            if dist < best_dist:
                best_dist = dist
                best_idx = idx
                best_target = target

        return best_idx, best_target, best_dist


def run_benchmark(n: int, num_ops: int = 10_000) -> None:
    """Генерує випадкові цілі, операції оновлення та запитів діапазону [L, R]

    і вимірює сумарний час виконання для обох підходів.
    """
    print(f"\n{'=' * 75}")
    print(f"Тестування на N = {n:,} цілей, кількість операцій = {num_ops:,}")
    print(f"{'=' * 75}")

    # Фіксуємо seed для відтворюваності однакових наборів цілей та запитів
    random.seed(42)
    point = (0.0, 0.0)

    # Генерація випадкових цілей: x, y in [-5000, 5000], h in [100, 10000]
    raw_targets = [
        (
            random.uniform(-5000.0, 5000.0),
            random.uniform(-5000.0, 5000.0),
            random.uniform(100.0, 10000.0),
        )
        for _ in range(n)
    ]

    # Генерація 50% операцій оновлення та 50% запитів діапазону
    operations = []
    for _ in range(num_ops):
        if random.random() < 0.5:
            # Оновлення: ('update', index, new_x, new_y, new_h)
            idx = random.randint(0, n - 1)
            operations.append(
                (
                    "update",
                    idx,
                    random.uniform(-5000.0, 5000.0),
                    random.uniform(-5000.0, 5000.0),
                    random.uniform(100.0, 10000.0),
                )
            )
        else:
            # Запит: ('nearest', left, right)
            l = random.randint(0, n - 1)
            r = random.randint(0, n - 1)
            if l > r:
                l, r = r, l
            operations.append(("nearest", l, r))

    # 1. Бенчмарк Дерева відрізків (AirDefense)
    t0 = time.perf_counter()
    ad_tree = AirDefense(raw_targets, point)
    tree_build_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for op in operations:
        if op[0] == "update":
            ad_tree.update(op[1], op[2], op[3], op[4])
        else:
            ad_tree.nearest(op[1], op[2])
    tree_ops_time = time.perf_counter() - t0

    # 2. Бенчмарк Наївного підходу (NaiveAirDefense)
    t0 = time.perf_counter()
    naive = NaiveAirDefense(raw_targets, point)
    naive_build_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for op in operations:
        if op[0] == "update":
            naive.update(op[1], op[2], op[3], op[4])
        else:
            naive.nearest(op[1], op[2])
    naive_ops_time = time.perf_counter() - t0

    # Вивід результатів
    print(f"{'Метрика':<32} | {'Дерево відрізків':<18} | {'Лінійний пошук':<15}")
    print("-" * 75)
    print(
        f"{'Час побудови (ініціалізації)':<32} | {tree_build_time:10.4f} с     | {naive_build_time:10.4f} с"
    )
    print(
        f"{'Час виконання 10 000 операцій':<32} | {tree_ops_time:10.4f} с     | {naive_ops_time:10.4f} с"
    )
    print(
        f"{'Загальний час':<32} | {tree_build_time + tree_ops_time:10.4f} с     | {naive_build_time + naive_ops_time:10.4f} с"
    )

    speedup = naive_ops_time / tree_ops_time if tree_ops_time > 0 else float("inf")
    print(
        f"\nПрискорення на операціях: у ~{speedup:.1f} раз(ів) швидше з деревом відрізків."
    )


if __name__ == "__main__":
    # Базові тести з методички
    ad = AirDefense([(100, 0, 50), (10, 10, 5), (300, 400, 100)], point=(0, 0))
    assert ad.nearest()[0] == 1  # [cite: 50]

    ad.update(1, 1000, 1000, 10)  # [cite: 50]
    assert ad.nearest()[0] == 0  # [cite: 50]

    ad.update(2, 1, 1, 1)  # [cite: 50]
    assert ad.nearest()[0] == 2  # [cite: 50]

    # Додатковий тест діапазону [L, R]
    # На індексах [0, 1] ціль 0 значно ближча (1000 проти ~111)
    res_range = ad.nearest(0, 1)
    assert res_range[0] == 0

    print("Завдання 3: базові тести пройдено успішно!\n\n\n")

    run_benchmark(n=100_000, num_ops=10_000)
    run_benchmark(n=1_000_000, num_ops=10_000)
