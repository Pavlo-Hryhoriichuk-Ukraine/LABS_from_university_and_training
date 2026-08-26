from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import heapq
import numpy as np


@dataclass
class Node:
    freq: int
    symbol: str | None = None
    left: Node | None = None
    right: Node | None = None

    def __lt__(self, other: Node) -> bool:
        return self.freq < other.freq


def huffman_code_tree(
    node: Node | None,
    code_dict: dict[str, str] | None = None,
    code: str = "",
) -> dict[str, str]:
    if code_dict is None:
        code_dict = {}

    if node is None:
        return code_dict

    # Leaf node contains a character symbol
    if node.left is None and node.right is None:
        if node.symbol is not None:
            code_dict[node.symbol] = code or "0"
        return code_dict

    huffman_code_tree(node.left, code_dict, code + "0")
    huffman_code_tree(node.right, code_dict, code + "1")
    return code_dict


def build_huffman_tree(text: str) -> tuple[Node, dict[str, int]]:
    if not text:
        raise ValueError("Текст для кодування не може бути порожнім.")

    freq_dict = Counter(text)

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


def encode_huffman_pipeline(text: str) -> tuple[str, int, int, float]:
    """
    Takes input plain text and returns:
    (encoded_string, original_size_bits, compressed_size_bits, compression_ratio)
    """
    if not text:
        return "", 0, 0, 0.0

    root, _ = build_huffman_tree(text)

    # Pass a fresh dictionary (or leave default None) to collect str -> str codes
    huffman_codes = huffman_code_tree(root)
    encoded: str = "".join(huffman_codes[char] for char in text)

    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    ratio = round((1.0 - (compressed_bits / original_bits)) * 100, 2) if original_bits else 0.0

    return encoded, original_bits, compressed_bits, ratio



def analyze_huffman_metrics(text_length: int, frequencies: dict[str, int], huffman_codes: dict[str, str]) -> tuple[float, float, float]:
    """
    Аналізує ентропію, середню довжину коду та надлишковість на основі дерева Гаффмана.
    """
    H = 0.0  # Ентропія
    L = 0.0  # Середня довжина коду

    for char, count in frequencies.items():
        # 1. Знаходимо ймовірність символу
        p_i = count / text_length

        # 2. Рахуємо Ентропію (Шеннон)
        if p_i > 0:
            H -= p_i * np.log2(p_i)

        # 3. Рахуємо середню довжину коду (Гаффман)
        # Довжина коду - це просто кількість нулів і одиниць у згенерованому рядку
        code_length = len(huffman_codes[char])
        L += p_i * code_length

    # 4. Надлишковість
    R = L - H

    return H, L, R



def result_analize(text: str) -> tuple[float, float, float]:
    if not text:
        return 0.0, 0.0, 0.0

    root, frequencies = build_huffman_tree(text)
    huffman_codes = huffman_code_tree(root)
    H, L, R = analyze_huffman_metrics(len(text), frequencies, huffman_codes)

    return H, L, R