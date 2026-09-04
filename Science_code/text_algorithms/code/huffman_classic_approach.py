from __future__ import annotations
from collections import Counter
import heapq
from dataclasses import dataclass
import os


@dataclass
class Node:
    freq: int
    symbol: str | None = None
    left: Node | None = None
    right: Node | None = None

    def __lt__(self, other: 'Node') -> bool:
        return self.freq < other.freq



def huffman_code_tree(node: Node | None, code='', code_dict: dict[str | None, int | str] | None = None) -> dict[str | None, int | str]:
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


def build_huffman_tree(text):
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


def main():
    user_input = input("Choose type of program flow (type it in terminal): 'user_input' or 'file': ").strip()

    if not user_input:
        print("ERROR: You have not inputted a text.")
        return


    if user_input == "user_input":
        text  = input("Input some text to encode by Huffman: ")

        root, frequencies = build_huffman_tree(text)
        huffman_codes = huffman_code_tree(root)

        print("\n Symbol | Frequency  | Huffman code")
        print("---------------------------------")
        for char in sorted(frequencies.keys()):
            print(f" {repr(char):<6} | {frequencies[char]:^10} | {huffman_codes[char]}")

        encoded = ''.join(str(huffman_codes[char]) for char in text)
        print(f"\nEncoded text: {encoded}")


    elif user_input == "file":
        file_path = input("Input path for your text file to encode by Huffman (you will recive new file with encoded text in the same directory): ").strip('"" ')

        with open(file_path, "r", encoding="utf-8") as file:
            str_list = file.readlines()
            text = ''.join(str_list)

        root, frequencies = build_huffman_tree(text)

        huffman_codes = huffman_code_tree(root)

        encoded = ''.join(str(huffman_codes[char]) for char in text)
        path, orig_name = os.path.splitext(file_path)
        name, extantion = orig_name.split('.')
        result_filename = path + name + '_Huffman_encoded' + "." + extantion
        with open(result_filename, 'w', encoding="utf-8") as file:
            file.write(encoded)


if __name__ == "__main__":
    main()