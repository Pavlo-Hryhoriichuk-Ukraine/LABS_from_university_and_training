import random
import re
from collections import deque


class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left: None | Node = None
        self.right: None | Node = None


class SearchTree:
    def __init__(self, path):
        """Зчитує слова з файлу `path` (див. домовленості) і зберігає їх."""
        self.root: None | Node = None
        self.words = self._read_words(path)

    @staticmethod
    def _read_words(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().lower()  # одразу переводимо в нижній регістр

        pattern = r"[a-zа-яіїєґ]+(?:['’\-][a-zа-яіїєґ]+)*"
        return re.findall(pattern, text)

    def _insert(self, key: str) -> None:
        curr_node = self.root
        if curr_node is None:
            self.root = Node(key)
            return
        while True:
            if key < curr_node.key:  # type : ignore
                if curr_node.left is not None:
                    curr_node = curr_node.left
                else:
                    curr_node.left = Node(key)
                    return
            elif key > curr_node.key:
                if curr_node.right is not None:
                    curr_node = curr_node.right
                else:
                    curr_node.right = Node(key)
                    return
            else:
                return

    def build(self, flag: bool = True, seed: int | None = None) -> None:
        """Builds the binary search tree sequentially or randomly."""
        self.root = None
        words_to_insert = list(dict.fromkeys(self.words))

        if not flag:
            rng = random.Random(seed)
            rng.shuffle(words_to_insert)

        for word in words_to_insert:
            self._insert(word)

    def search(self, word: str) -> tuple[bool, int]:
        curr = self.root
        comparisons = 0

        while curr is not None:
            comparisons += 1
            if word == curr.key:
                return True, comparisons

            comparisons += 1
            if word < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        return False, comparisons

    def delete(self, key: str) -> bool:
        """Публічний метод для видалення слова з дерева.

        Повертає True, якщо ключ був у дереві і його успішно видалено,
        або False, якщо слова в дереві не виявилося.
        """
        # Спочатку перевіряємо, чи є слово взагалі в дереві (використовуємо наш search)
        found, _ = self.search(key.lower())
        if not found:
            return False

        # Оновлюємо корінь за функціонально-рекурсивним патерном
        self.root = self._delete_node(self.root, key.lower())

        # Якщо в класі підтримується список слів words, видаляємо ключ і звідти
        if hasattr(self, "words") and key.lower() in self.words:
            self.words = [w for w in self.words if w != key.lower()]

        return True

    @staticmethod
    def _delete_node(node: Node | None, key: str) -> Node | None:
        """Рекурсивний допоміжний метод для видалення вузла.

        Повертає новий або модифікований корінь піддерева.
        """
        if node is None:
            return None

        # 1. Пошук вузла в дереві
        if key < node.key:
            node.left = SearchTree._delete_node(node.left, key)
        elif key > node.key:
            node.right = SearchTree._delete_node(node.right, key)
        else:
            # 2. Знайшли вузол для видалення (key == node.key)

            # Випадок 1 і 2а: немає лівого сина (або листок)
            # Якщо листок — node.right це None, тому повернеться None
            # Якщо є тільки правий син — повернеться node.right (підтягується вгору)
            if node.left is None:
                return node.right

            # Випадок 2б: немає тільки правого сина
            # Повертається node.left (підтягується вгору)
            if node.right is None:
                return node.left

            # Випадок 3: у вузла двоє дітей
            # Шукаємо максимум у лівому піддереві (найбільший попередник)
            max_left = node.left
            while max_left.right is not None:
                max_left = max_left.right

            # Підміняємо значення в поточному вузлі
            node.key = max_left.key

            # Рекурсивно видаляємо старий дублікат з лівого піддерева
            node.left = SearchTree._delete_node(node.left, max_left.key)

        return node

    def stats(self) -> tuple[int, int, int, int]:
        if self.root is None:
            return 0, 0, 0, 0

        leaves = 0
        internal = 0
        depth = 0
        queue = deque([(self.root, 0)])

        while queue:
            curr, depth = queue.popleft()

            if curr.left is None and curr.right is None:
                leaves += 1
            else:
                internal += 1

            if curr.left is not None:
                queue.append((curr.left, depth + 1))
            if curr.right is not None:
                queue.append((curr.right, depth + 1))

        edges = leaves + internal - 1
        return leaves, internal, edges, depth

    def sorted_words(self) -> list[str]:
        result: list[str] = []
        stack: list[Node] = []
        curr = self.root

        while stack or curr is not None:
            while curr is not None:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()
            result.append(curr.key)

            curr = curr.right

        return result

    def leaf_path_lengths(self) -> list[int]:
        if self.root is None:
            return []

        leaf_lengths: list[int] = []
        queue = deque([(self.root, 0)])

        while queue:
            curr, depth = queue.popleft()

            if curr.left is None and curr.right is None:
                leaf_lengths.append(depth)
            else:
                if curr.left is not None:
                    queue.append((curr.left, depth + 1))
                if curr.right is not None:
                    queue.append((curr.right, depth + 1))

        return leaf_lengths

    def path_length_variance(self) -> float:
        lengths = self.leaf_path_lengths()
        m = len(lengths)
        if m == 0:
            return 0.0

        mean = sum(lengths) / m
        variance = sum((d - mean) ** 2 for d in lengths) / m
        return variance


if __name__ == "__main__":
    # --- Базовый тест из методички ---
    sample = "Автобус, поїзд; автомобіль! трамвай. Автобус поїзд."
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write(sample)

    tree = SearchTree("sample.txt")
    tree.build(flag=True)

    assert tree.sorted_words() == ["автобус", "автомобіль", "поїзд", "трамвай"]
    assert tree.search("поїзд")[0] is True
    assert tree.search("метро")[0] is False

    leaves, internal, edges, height = tree.stats()
    assert leaves + internal == 4 and edges == 3
    print("Завдання 1: базові тести пройдено успішно!\n")

    # --- Экспериментальная часть ---
    # 1. Текст длиной >= 5000 слов с достаточным количеством уникальных лексем
    # Генерируем 1000 базовых слов из чистых букв
    letters = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
    vocab = ["".join(random.choices(letters, k=6)) for _ in range(1000)]
    natural_words = random.choices(vocab, k=5500)
    with open("text_5000.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(natural_words))

    # 2. Файл из 5000 уникальных слов, отсортированных по алфавиту (только буквы)
    # Кодируем числа в 4-значные буквенные комбинации для строгого алфавитного порядка
    def int_to_alpha(n: int) -> str:
        res = []
        for _ in range(4):
            res.append(letters[n % len(letters)])
            n //= len(letters)
        return "".join(reversed(res))

    sorted_words = sorted({int_to_alpha(i) for i in range(5000)})
    with open("sorted_words.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(sorted_words))

    # Набор отсутствующих слов для теста
    missing_100 = [f"zzz{i}" for i in range(100)]

    configs = [
        ("text_5000.txt", True, "Текст >=5000 (послідовно)"),
        ("text_5000.txt", False, "Текст >=5000 (випадково)"),
        ("sorted_words.txt", True, "Відсортовані (послідовно)"),
        ("sorted_words.txt", False, "Відсортовані (випадково)"),
    ]

    print("=" * 110)
    print(
        f"{'Конфігурація':<30} | {'Листки':<7} | {'Внутр':<6} | {'Ребра':<6} | "
        f"{'h':<6} | {'Дисперсія':<10} | {'Шукати (є)':<11} | {'Шукати (нема)':<12}"
    )
    print("-" * 110)

    for path, flg, label in configs:
        st = SearchTree(path)
        st.build(flag=flg, seed=42)

        l_cnt, i_cnt, e_cnt, h = st.stats()
        var = st.path_length_variance()

        # Тестируем 100 существующих слов и 100 отсутствующих
        unique_in_tree = list(dict.fromkeys(st.words))
        test_exist = unique_in_tree[:100]

        comp_exist = sum(st.search(w)[1] for w in test_exist) / len(test_exist)
        comp_miss = sum(st.search(w)[1] for w in missing_100) / len(missing_100)

        print(
            f"{label:<30} | {l_cnt:<7} | {i_cnt:<6} | {e_cnt:<6} | "
            f"{h:<6} | {var:<10.2f} | {comp_exist:<11.2f} | {comp_miss:<12.2f}"
        )
    print("=" * 110)
