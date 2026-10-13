from __future__ import annotations
from collections import Counter
import heapq
from dataclasses import dataclass
from pathlib import Path
import re
import os
import numpy as np


@dataclass
class Node:
    freq: int
    symbol: str | None = None
    left: Node | None = None
    right: Node | None = None

    def __lt__(self, other: 'Node') -> bool:
        return self.freq < other.freq

def tokenize_text(text: str) -> list[str]:
    """
    Розбиває текст на слова та 'не-слова' (пробіли, розділові знаки).
    Це дозволяє ідеально відновити оригінальний текст при декодуванні.
    """
    if not text:
        return []
    return re.findall(r'\w+|[^\w]+', text)

def huffman_code_tree(node: Node | None, code='', code_dict: dict[str | None, str] | None = None) -> dict[str | None, str]:
    if code_dict is None:
        code_dict = {}
    if node is None:
        return code_dict

    if node.left is None and node.right is None:
        code_dict[node.symbol] = code or '0'
        return code_dict

    huffman_code_tree(node.left, code + '0', code_dict)
    huffman_code_tree(node.right, code + '1', code_dict)
    return code_dict

def build_huffman_tree(tokens: list[str]) -> tuple[Node, dict[str, int]]:
    if not tokens:
        raise ValueError("Текст для кодування не може бути порожнім.")

    freq_dict = Counter(tokens)

    heap = [Node(freq, symbol) for symbol, freq in freq_dict.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        root = heap[0]
        return root, dict(freq_dict)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0], dict(freq_dict)

def decode_huffman(encoded_text: str, root: Node) -> str:
    """
    Крок за кроком проходить по бінарному рядку та спускається по дереву,
    щоб відновити початкові токени (слова та пунктуацію).
    """
    decoded_tokens = []
    current_node = root

    # Спеціальний випадок: якщо текст складався з одного унікального слова
    if root.left is None and root.right is None:
        # Для коректної роботи треба знати початкову кількість слів,
        # але для спрощення повертаємо базовий символ.
        return (root.symbol or "") * len(encoded_text)

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left # type: ignore
        else:
            current_node = current_node.right # type: ignore

        # Якщо дійшли до листка (кінця коду для поточного токена)
        if current_node.left is None and current_node.right is None: # type: ignore
            decoded_tokens.append(current_node.symbol) # type: ignore
            current_node = root # Повертаємося в корінь для наступного слова

    return "".join(decoded_tokens) # type: ignore

def encode_text_to_binary(text: str) -> str:
    """
    Приймає сирий текст, розбиває його на слова (токени),
    будує дерево Гаффмана та повертає суцільний бінарний рядок.
    Ідеально для імпорту як API в інші модулі.
    """
    if not text:
        return ""

    tokens = tokenize_text(text)
    root, frequencies = build_huffman_tree(tokens)
    huffman_codes = huffman_code_tree(root)

    # Склеюємо всі бітові коди в один довгий рядок
    encoded_string = ''.join(huffman_codes[token] for token in tokens)

    return encoded_string

def get_binary_from_file(filename: str) -> str:
    """
    Шукає файл у папці '../texts/', читає його та повертає бінарний рядок
    послівного кодування Гаффмана.
    """
    import os

    # Формуємо правильний шлях до папки texts
    file_path = Path(__file__).parent.parent.resolve() / "texts" / (filename + ".txt")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл не знайдено за шляхом: {os.path.abspath(file_path)}")

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return encode_text_to_binary(text)


def analyze_word_huffman_metrics(
    total_tokens: int,
    word_frequencies: dict[str, int],
    word_huffman_codes: dict[str, str]
) -> tuple[float, float, float]:
    """
    Обчислює семантичну ентропію, середню довжину коду слова та надлишковість.
    """
    if total_tokens == 0:
        return 0.0, 0.0, 0.0

    H = 0.0  # Лексична Ентропія
    L = 0.0  # Середня бітова довжина слова

    for word, count in word_frequencies.items():
        # 1. Ймовірність появи конкретного слова в тексті
        p_i = count / total_tokens

        # 2. Ентропія Шеннона
        if p_i > 0:
            H -= p_i * np.log2(p_i)

        # 3. Середня довжина коду слова
        code_length = len(word_huffman_codes[word])
        L += p_i * code_length

    # 4. Надлишковість (наскільки Гаффман відхиляється від ідеалу Шеннона)
    R = L - H

    return H, L, R

def main():
    print("=== Аналіз тексту: Word-Level Huffman ===")
    filename = "Human 147 (30000)"

    # Формуємо шлях: піднімаємося на рівень вище (..) і заходимо в папку texts
    # os.path.join автоматично підбере правильні слеші (\ для Windows, / для Linux)
    file_path = os.path.join(".", "Science_code\\text_algorithms\\texts", filename + '.txt')

    # Перевіряємо, чи дійсно файл існує за цим шляхом
    if not os.path.isfile(file_path):
        absolute_path = os.path.abspath(file_path)
        print(f"ПОМИЛКА: Файл не знайдено!")
        print(f"Програма шукала його тут: {absolute_path}")
        return

    print(f"\nЧитання файлу: {os.path.abspath(file_path)}...")

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        print("ПОМИЛКА: Файл порожній.")
        return

    # 1. Токенізація
    tokens = tokenize_text(text)
    total_tokens = len(tokens)

    # 2. Побудова дерева та кодів
    root, frequencies = build_huffman_tree(tokens)
    huffman_codes = huffman_code_tree(root)

    # 3. Аналіз метрик (H, L, R)
    # Переконайся, що функція analyze_word_huffman_metrics є у файлі!
    H, L, R = analyze_word_huffman_metrics(total_tokens, frequencies, huffman_codes) # type: ignore

    with open(f".\\Science_code\\text_algorithms\\gen_results\\WH_{filename}_word_huffman.txt", 'w') as file:

        print("=== ЛЕКСИЧНІ МЕТРИКИ (Word-Level) ===", file=file)
        print(f"Загальна кількість токенів (слів+пунктуації): {total_tokens}", file=file)
        print(f"Унікальних токенів (розмір словника):         {len(frequencies)}", file=file)
        print("-" * 50)
        print(f"Ентропія Шеннона (H):     {H:.5f} біт/слово (Багатство словника)", file=file)
        print(f"Середня довжина коду (L): {L:.5f} біт/слово (Практичне стиснення)", file=file)
        print(f"Надлишковість (R = L-H):  {R:.5f} біт/слово (Маркер штучної генерації)", file=file)
        print("-" * 50)

    # 4. Кодування

    print(f"\n✅ Успіх! Файл проаналізовано та закодовано.")

if __name__ == "__main__":
    main()