import numpy as np
from typing import Dict
from itertools import pairwise
from itertools import pairwise

from huffman import build_huffman_tree, huffman_code_tree


def build_matrix_16(text: str) -> np.ndarray:
    """
    Builds a 16x16 transition matrix based on broad semantic groups.
    Groups are specifically tailored for English language analysis.
    """
    groups: Dict[str, int] = {
        **{c: 0 for c in 'aeiouy'},               # Vowels
        **{c: 1 for c in 'bcdfghjklmnpqrstvwxz'}, # Consonants
        ' ': 2,                                   # Space
        **{c: 3 for c in '0123456789'},           # Digits
        **{c: 4 for c in '.,'},                   # Sentence-ending punctuation
        **{c: 5 for c in '!?'},                   # Emotional punctuation
        **{c: 6 for c in '"\'’“”'},               # Quotation marks
        **{c: 7 for c in '-—_'},                  # Dashes and underscores
        **{c: 8 for c in '()[]{}'},               # Brackets
        '\n': 9                                   # Newline character
        # Indexes 10-14 are reserved for future custom groups
        # Index 15 is the fallback bin for all unknown characters
    }

    # Initialize with float64 to prepare for probability normalization
    matrix = np.zeros((16, 16), dtype=np.float64)

    # pairwise() yields fast overlapping pairs: (char1, char2), (char2, char3)
    for c1, c2 in pairwise(text.lower()):
        g1 = groups.get(c1, 15)
        g2 = groups.get(c2, 15)
        matrix[g1, g2] += 1

    return matrix


def build_matrix_32(text: str) -> np.ndarray:
    """
    Builds a 32x32 transition matrix mapping individual English letters.
    """
    groups: Dict[str, int] = {
        # Map each lowercase letter to its own specific index (0-25)
        **{c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')},
        ' ': 26,                                  # Space
        **{c: 27 for c in '0123456789'},          # Group all digits together
        **{c: 28 for c in '.,!?'},                # Basic punctuation
        **{c: 29 for c in '"\'’“”'},              # Quotes
        **{c: 30 for c in '-—_()[]{}'}            # Formatting and brackets
        # Index 31 is the fallback bin
    }

    matrix = np.zeros((32, 32), dtype=np.float64)

    for c1, c2 in pairwise(text.lower()):
        g1 = groups.get(c1, 31)
        g2 = groups.get(c2, 31)
        matrix[g1, g2] += 1

    return matrix


def build_matrix_64(text: str) -> np.ndarray:
    """
    Builds a 64x64 transition matrix mapping both uppercase and lowercase letters.
    This helps in detecting capitalization patterns (e.g., in AI-generated code or text).
    """
    groups: Dict[str, int] = {
        # Lowercase letters (0-25)
        **{c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')},
        # Uppercase letters (26-51)
        **{c: i + 26 for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')},
        ' ': 52,                                  # Space
        # Map each digit to its own specific index (53-62)
        **{str(d): d + 53 for d in range(10)}
        # Index 63 is the fallback bin for punctuation and unknown symbols
    }

    matrix = np.zeros((64, 64), dtype=np.float64)

    # We DO NOT use text.lower() here because case sensitivity is the whole point of 64x64
    for c1, c2 in pairwise(text):
        g1 = groups.get(c1, 63)
        g2 = groups.get(c2, 63)
        matrix[g1, g2] += 1

    return matrix


def build_matrix_128(text: str) -> np.ndarray:
    """
    Builds a 128x128 transition matrix based strictly on standard ASCII codes.
    Safely ignores non-ASCII characters to prevent IndexError.
    """
    matrix = np.zeros((128, 128), dtype=np.float64)

    # Encode the string to ASCII bytes.
    # errors='ignore' safely strips out any character outside the 0-127 range.
    byte_data = text.encode('ascii', errors='ignore')

    for b1, b2 in pairwise(byte_data):
        matrix[b1, b2] += 1

    return matrix


def build_matrix_256(text: str) -> np.ndarray:
    """
    Builds a 256x256 transition matrix based on raw UTF-8 bytes.
    Captures absolutely every character mathematically without crashing.
    """
    matrix = np.zeros((256, 256), dtype=np.float64)

    # Encode to UTF-8. Every character becomes a byte or sequence of bytes (0-255).
    byte_data = text.encode('utf-8')

    for b1, b2 in pairwise(byte_data):
        matrix[b1, b2] += 1

    return matrix


def build_huffman_matrix(text: str) -> np.ndarray:
    root, _ = build_huffman_tree(text)

    codes = huffman_code_tree(root)

    encoded_text = "".join(codes[char] for char in text)

    matrix = np.zeros((2, 2), dtype=np.float64)

    for b1, b2 in pairwise(encoded_text):
        matrix[int(b1), int(b2)] += 1

    return matrix


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Перетворює матрицю частот на стохастичну матрицю ймовірностей.
    """
    # 1. Рахуємо суму кожного рядка.
    # keepdims=True зберігає форму стовпця (N, 1), щоб NumPy зміг правильно поділити матрицю.
    row_sums = matrix.sum(axis=1, keepdims=True)

    # 2. Захист від ділення на нуль (ZeroDivisionError)
    # Якщо якийсь символ чи клас жодного разу не зустрівся, сума його рядка буде 0.
    # Ми тимчасово міняємо ці нулі на 1 (оскільки 0 / 1 = 0, математика не ламається).
    row_sums[row_sums == 0] = 1.0

    # 3. Векторне ділення всієї матриці на стовпець сум
    normalized_matrix = matrix / row_sums

    return normalized_matrix


def analyze_eigenvalues(normalized_matrix: np.ndarray) -> np.ndarray:
    """
    Обчислює та повертає відсортовані власні значення матриці.
    """
    eigenvalues = np.linalg.eigvals(normalized_matrix)
    threshold = 0.05
    eigenvalues = [abs(ev) for ev in eigenvalues if abs(ev) > threshold] #type: ignore
    print(f"Eigenvalues above threshold {threshold}: {eigenvalues}")
    if not eigenvalues:
        raise ValueError("No valid eigenvalues found. The matrix may be degenerate or improperly normalized.")

    # Для текстового аналізу нас цікавить їхня амплітуда (модуль).
    abs_eigenvalues = np.abs(eigenvalues)

    # 3. Сортуємо від найбільшого до найменшого
    sorted_eigenvals = np.sort(abs_eigenvalues)[::-1]

    return sorted_eigenvals[:10]