from __future__ import annotations
from typing import Annotated, ClassVar
from dataclasses import dataclass, field, fields
from itertools import zip_longest
from functools import total_ordering
import string

BaseRange = Annotated[int, "Must be an integer in range [2, 32]"]

def _build_alphabet_mappings() -> tuple[dict[str, int], dict[int, str]]:
    char_to_int = {str(i): i for i in range(10)}
    int_to_char = {i: str(i) for i in range(10)}
    for i, char in enumerate(string.ascii_uppercase[:22], start=10):
        char_to_int[char] = i
        int_to_char[i] = char
    return char_to_int, int_to_char


@dataclass
class OperationStats:
    additions: int = 0
    multiplications: int = 0
    divisions: int = 0
    comparisons: int = 0
    carries: int = 0

    def reset(self) -> None:
        for f in fields(self):
            setattr(self, f.name, 0) # type: ignore

    def get_total(self) -> int:
        return sum(getattr(self, f.name) for f in fields(self))  # type: ignore



@total_ordering
@dataclass
class BigInt:
    digits: list[int]
    base: BaseRange
    is_negative: bool = False
    stats: OperationStats = field(default_factory=OperationStats)

    _c2i, _i2c = _build_alphabet_mappings()
    _CHAR_TO_INT: ClassVar[dict[str, int]] = _c2i
    _INT_TO_CHAR: ClassVar[dict[int, str]] = _i2c

    def __post_init__(self) -> None:
        if not (2 <= self.base <= 32):
            raise ValueError(f"Base must be between 2 and 32. Got: {self.base}")
        self._normalize()

    def _normalize(self) -> None:
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()

        if len(self.digits) == 1 and self.digits[0] == 0:
            self.is_negative = False

    @classmethod
    def from_string(cls, number: str, base: BaseRange, stats: OperationStats | None = None) -> BigInt:
        is_negative = number.startswith('-')
        clean_number = number.lstrip('-').lstrip('0') or '0'

        digits = [cls._CHAR_TO_INT[char] for char in reversed(clean_number)]
        return cls(digits, base, is_negative, stats or OperationStats())

    def convert_to(self, target_base: BaseRange) -> BigInt:
        """
        Converts the current BigInt to a new base using Horner's scheme.
        Returns a new BigInt instance, preserving the sign.
        """
        if not (2 <= target_base <= 32):
            raise ValueError(f"Target base must be between 2 and 32. Got: {target_base}")

        if self.base == target_base:
            return BigInt(self.digits.copy(), self.base, self.is_negative, self.stats)

        result: list[int] = [0]

        # Read from most significant to least significant (reverse of Little-endian)
        for val in reversed(self.digits):
            carry = val

            for i in range(len(result)):
                self.stats.multiplications += 1
                self.stats.additions += 1
                self.stats.divisions += 2 # Modulo and floor division

                temp = result[i] * self.base + carry
                result[i] = temp % target_base
                carry = temp // target_base

                self.stats.carries += 1

            while carry > 0:
                self.stats.divisions += 2
                result.append(carry % target_base)
                carry //= target_base
                self.stats.carries += 1

        return BigInt(result, target_base, self.is_negative, self.stats)

    def __str__(self) -> str:
        """
        Converts the Little-endian array back to a readable string, including the sign.
        """
        if not self.digits:
            return "0"

        sign = "-" if self.is_negative else ""
        number_str = "".join(self._INT_TO_CHAR[num] for num in reversed(self.digits))

        return f"{sign}{number_str}"


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BigInt):
            return NotImplemented
        self.stats.comparisons += 1
        return (self.is_negative == other.is_negative and
                self.base == other.base and
                self.digits == other.digits)

    def __lt__(self, other: BigInt) -> bool:
        if self.base != other.base:
            raise ValueError("Bases must match for comparison")

        self.stats.comparisons += 1

        if self.is_negative != other.is_negative:
            return self.is_negative

        if len(self.digits) != len(other.digits):
            is_less = len(self.digits) < len(other.digits)
            return is_less if not self.is_negative else not is_less

        for d1, d2 in zip(reversed(self.digits), reversed(other.digits)):
            if d1 != d2:
                is_less = d1 < d2
                return is_less if not self.is_negative else not is_less

        return False

    def __add__(self, other: BigInt) -> BigInt:
        if self.base != other.base:
            raise ValueError("Cannot add BigInts with different bases")

        # -A + (-B) -> -(A + B)
        if self.is_negative and other.is_negative:
            pos_self = BigInt(self.digits, self.base, False, self.stats)
            pos_other = BigInt(other.digits, other.base, False, self.stats)
            result = pos_self + pos_other
            result.is_negative = True
            return result

        # -A + B -> B - |A|
        # A + (-B) -> A - |B|
        elif self.is_negative != other.is_negative:
            pos_self = BigInt(self.digits, self.base, False, self.stats)
            pos_other = BigInt(other.digits, other.base, False, self.stats)
            return pos_other - pos_self if self.is_negative else pos_self - pos_other

        result_digits: list[int] = []
        carry = 0

        for digit_a, digit_b in zip_longest(self.digits, other.digits, fillvalue=0):
            current_sum = digit_a + digit_b + carry
            remain = current_sum % self.base
            carry = current_sum // self.base

            result_digits.append(remain)

            self.stats.additions += 2
            self.stats.divisions += 2
            self.stats.carries += 1

        if carry > 0:
            result_digits.append(carry)

        return BigInt(result_digits, self.base, self.is_negative, self.stats)


    def __sub__(self, other: BigInt) -> BigInt:
        if self.base != other.base:
            raise ValueError("Cannot subtract BigInts with different bases")

        # A - (-B) -> A + B
        # -A - B -> -(A + B)
        if self.is_negative != other.is_negative:
            pos_self = BigInt(self.digits, self.base, False, self.stats)
            pos_other = BigInt(other.digits, other.base, False, self.stats)

            result = pos_self + pos_other
            result.is_negative = self.is_negative
            return result

        pos_self = BigInt(self.digits, self.base, False, self.stats)
        pos_other = BigInt(other.digits, other.base, False, self.stats)

        if pos_self < pos_other:
            # A - B (where B > A) -> -(B - A)
            # -A - (-B) -> B - A (where B > A) -> +(B - A)
            result = pos_other - pos_self
            result.is_negative = not self.is_negative
            return result



        result_digits: list[int] = []
        borrow = 0

        for digit_a, digit_b in zip_longest(self.digits, other.digits, fillvalue=0):
            d = digit_a - digit_b - borrow

            if d < 0:
                d += self.base
                borrow = 1
                self.stats.additions += 1  # For d += self.base
            else:
                borrow = 0

            result_digits.append(d)


            self.stats.additions += 2
            self.stats.comparisons += 1
            if borrow:
                self.stats.carries += 1

        return BigInt(result_digits, self.base, self.is_negative, self.stats)



    def __mul__(self, other: BigInt) -> BigInt:
        if self.base != other.base:
            raise ValueError("Cannot multiply BigInts with different bases")

        result_is_negative = self.is_negative != other.is_negative

        # 2. Pre-allocate result array
        result_digits = [0] * (len(self.digits) + len(other.digits))

        for i, digit_a in enumerate(self.digits):
            carry = 0
            for j, digit_b in enumerate(other.digits):
                # Add existing value in the array to the partial product
                current_sum = (digit_a * digit_b) + carry + result_digits[i + j]

                result_digits[i + j] = current_sum % self.base
                carry = current_sum // self.base

                self.stats.multiplications += 1
                self.stats.additions += 2
                self.stats.divisions += 2
                self.stats.carries += 1

            if carry > 0:
                # Mathematically safer to use += here, though the cell is initially 0
                result_digits[i + len(other.digits)] += carry
                self.stats.additions += 1
                self.stats.carries += 1

        return BigInt(result_digits, self.base, result_is_negative, self.stats)