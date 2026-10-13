from itertools import pairwise
from collections.abc import Callable
from math import floor
import math
from abc import ABC, abstractmethod

# Sentinel object for Open Addressing deletions
DELETED = object()


def convert_binary_message(binary_string: str) -> str:
    length = len(binary_string)
    if length < 8:
        raise ValueError("Argument 'binary_string' must contain at least 8 bits.")

    # Guard against incomplete trailing bytes
    valid_length = length - (length % 8)
    return "".join(
        chr(int(binary_string[i : i + 8], 2))
        for i in range(0, valid_length, 8)
    )

def decode_file(
    path_message: str,
    path_key1: str,
    path_key2: str,
    collection_key1: set[str] | None = None,
    collection_key2: set[str] | None = None
) -> str:
    """
    Decodes the hidden binary message from message.txt using keys key1.txt and key2.txt.
    """
    keys_1 = set() if collection_key1 is None else collection_key1
    keys_2 = set() if collection_key2 is None else collection_key2

    with open(path_message, "r", encoding="utf-8") as f:
        message_str = f.read()
    with open(path_key1, "r", encoding="utf-8") as f:
        key1_str = f.read()
    with open(path_key2, "r", encoding="utf-8") as f:
        key2_str = f.read()

    for char1, char2 in pairwise(key1_str):
        keys_1.add(char1 + char2)

    for char1, char2 in pairwise(key2_str):
        keys_2.add(char1 + char2)

    bit_tokens = []
    for i in range(0, len(message_str) - 1, 2):
        pair = message_str[i : i + 2]

        in_key1 = pair in keys_1
        in_key2 = pair in keys_2

        if in_key1 and in_key2:
            bit_tokens.append("1")
        elif not in_key1 and not in_key2:
            bit_tokens.append("0")

    return "".join(bit_tokens)

# --- Hash Functions ---

def get_16bit_key(char_pair: str) -> int:
    """Converts a 2-character ASCII string into a 16-bit integer."""
    if len(char_pair) != 2:
        return ord(char_pair[0]) if char_pair else 0
    return (ord(char_pair[0]) << 8) + ord(char_pair[1])


def hash_pair_division(char_pair: str, number_of_cells: int) -> int:
    k = get_16bit_key(char_pair)
    return k % number_of_cells


def hash_pair_mul(char_pair: str, number_of_cells: int) -> int:
    k = get_16bit_key(char_pair)
    A: float = 0.6180339887 # Golden ratio
    return floor(number_of_cells * ((k * A) % 1))


def hash_middle_square(char_pair: str, number_of_cells: int) -> int:
    k = get_16bit_key(char_pair)
    squared = k * k

    r = int(math.log2(number_of_cells)) if number_of_cells > 0 else 1
    shift_amount = (32 - r) // 2
    mask = (1 << r) - 1

    hash_val = (squared >> shift_amount) & mask
    return hash_val % number_of_cells


# --- Hash Table Implementations ---

class HashTable:
    # Changed default size to 128 (power of 2) for optimal bitwise hashing
    def __init__(self, hash_func: Callable, number_of_cells: int = 128, max_load_factor: float = 0.75):
        self.table: list = [None] * number_of_cells
        self.hash_func = hash_func
        self.number_of_cells = number_of_cells
        self.max_load_factor = max_load_factor
        self.num_of_elements = 0

        # Statistics
        self.total_collisions = 0
        self.max_chain_length = 0

    def get_statistics(self) -> str:
        """Returns a formatted string containing performance statistics."""
        return (f"[{self.__class__.__name__}] "
                f"Elements: {self.num_of_elements}, "
                f"Cells: {self.number_of_cells}, "
                f"Total Collisions: {self.total_collisions}, "
                f"Max Chain/Probe Length: {self.max_chain_length}")


class HashTableChaining(HashTable):
    """
    Implements Separate Chaining for collision resolution.
    """
    def __contains__(self, item: str) -> bool:
        item_hash = self.hash_func(item, self.number_of_cells)
        bucket = self.table[item_hash]

        if bucket is not None:
            return item in bucket
        return False

    def add(self, item: str) -> None:
        self.maybe_rehash_table()

        item_hash = self.hash_func(item, self.number_of_cells)
        bucket: list = self.table[item_hash]

        if bucket is None:
            self.table[item_hash] = [item]
            self.num_of_elements += 1
            if self.max_chain_length < 1:
                self.max_chain_length = 1
        elif item not in bucket:
            # Collision detected
            self.total_collisions += 1
            bucket.append(item)
            self.num_of_elements += 1

            if len(bucket) > self.max_chain_length:
                self.max_chain_length = len(bucket)

    def maybe_rehash_table(self) -> None:
        if self.num_of_elements / self.number_of_cells >= self.max_load_factor:
            old_table = self.table

            self.number_of_cells *= 2
            self.table = [None] * self.number_of_cells
            self.num_of_elements = 0

            # Reset stats to recalculate for the new distribution
            self.total_collisions = 0
            self.max_chain_length = 0

            for bucket in old_table:
                if bucket is not None:
                    for elem in bucket:
                        self.add(elem)


class HashTableOpenAddressing(HashTable, ABC):
    """
    Abstract base class for Open Addressing hash tables.
    """
    @abstractmethod
    def _get_probe_index(self, item: str, attempt: int, base_hash: int) -> int:
        pass

    def __contains__(self, item: str) -> bool:
        base_hash = self.hash_func(item, self.number_of_cells)
        attempt = 0

        while attempt < self.number_of_cells:
            idx = self._get_probe_index(item, attempt, base_hash)
            cell_value = self.table[idx]

            if cell_value is None:
                return False

            if cell_value == item:
                return True

            attempt += 1

        return False

    def add(self, item: str) -> None:
        self.maybe_rehash_table()

        base_hash = self.hash_func(item, self.number_of_cells)
        attempt = 0

        while attempt < self.number_of_cells:
            idx = self._get_probe_index(item, attempt, base_hash)
            cell_value = self.table[idx]

            if cell_value is None or cell_value is DELETED:
                self.table[idx] = item
                self.num_of_elements += 1

                # attempt=0 means 1 probe, attempt=1 means 2 probes, etc.
                probe_sequence_length = attempt + 1
                if probe_sequence_length > self.max_chain_length:
                    self.max_chain_length = probe_sequence_length
                return

            if cell_value == item:
                return

            # Collision occurred at this probe
            self.total_collisions += 1
            attempt += 1

        raise RuntimeError("Hash table is completely full. Rehashing failed.")

    def maybe_rehash_table(self) -> None:
        if self.num_of_elements / self.number_of_cells >= self.max_load_factor:
            old_table = self.table

            self.number_of_cells *= 2
            self.table = [None] * self.number_of_cells
            self.num_of_elements = 0

            # Reset stats
            self.total_collisions = 0
            self.max_chain_length = 0

            for cell_value in old_table:
                if cell_value is not None and cell_value is not DELETED:
                    self.add(cell_value)


class HashTableLinearProbing(HashTableOpenAddressing):
    # Added strict 0.5 max_load_factor limit to prevent primary clustering death
    def __init__(self, hash_func: Callable, number_of_cells: int = 128, max_load_factor: float = 0.5):
        super().__init__(hash_func, number_of_cells, max_load_factor)

    def _get_probe_index(self, item: str, attempt: int, base_hash: int) -> int:
        return (base_hash + attempt) % self.number_of_cells


class HashTableQuadraticProbing(HashTableOpenAddressing):
    def __init__(self, hash_func: Callable, number_of_cells: int = 128, max_load_factor: float = 0.5):
        super().__init__(hash_func, number_of_cells, max_load_factor)

    def _get_probe_index(self, item: str, attempt: int, base_hash: int) -> int:
        # Triangular number sequence guarantees covering all cells when m = 2^r
        offset = (attempt + attempt ** 2) // 2
        return (base_hash + offset) % self.number_of_cells


class HashTableDoubleHashing(HashTableOpenAddressing):
    def __init__(self, hash_func: Callable, number_of_cells: int = 128, max_load_factor: float = 0.5):
        super().__init__(hash_func, number_of_cells, max_load_factor)

    def _get_h2(self, item: str) -> int:
        k = get_16bit_key(item)
        return (k % (self.number_of_cells - 1)) | 1

    def _get_probe_index(self, item: str, attempt: int, base_hash: int) -> int:
        h2_val = self._get_h2(item)
        return (base_hash + attempt * h2_val) % self.number_of_cells


# --- Bitset Implementation ---

class ASCIIBitset:
    def __init__(self):
        # 65536 bits // 8 = 8192 bytes
        self._data = bytearray(8192)

    def _get_key(self, item: str) -> int:
        return (ord(item[0]) << 8) + ord(item[1])

    def add(self, item: str) -> None:
        k = self._get_key(item)
        byte_index = k // 8
        bit_offset = k % 8
        self._data[byte_index] |= (1 << bit_offset)

    def __contains__(self, item: str) -> bool:
        k = self._get_key(item)
        byte_index = k // 8
        bit_offset = k % 8
        return (self._data[byte_index] & (1 << bit_offset)) != 0