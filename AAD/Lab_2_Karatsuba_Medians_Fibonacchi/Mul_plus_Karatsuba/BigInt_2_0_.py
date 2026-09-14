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



@total_ordering
@dataclass
class BigInt:
    digits: list[int]
    base: BaseRange = field(default=10)
    is_negative: bool = False

    _c2i, _i2c = _build_alphabet_mappings()
    _CHAR_TO_INT: ClassVar[dict[str, int]] = _c2i
    _INT_TO_CHAR: ClassVar[dict[int, str]] = _i2c
    KARATSUBA_THRESHOLD: ClassVar[int] = 64
    TOOM_THRESHOLD: ClassVar[int] = 128

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
    def from_string(cls, number: str, base: BaseRange) -> BigInt:
        is_negative = number.startswith('-')
        clean_number = number.lstrip('-').lstrip('0') or '0'

        digits = [cls._CHAR_TO_INT[char] for char in reversed(clean_number)]
        return cls(digits, base, is_negative)

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
        return (self.is_negative == other.is_negative and
                self.base == other.base and
                self.digits == other.digits)

    def __lt__(self, other: BigInt) -> bool:
        if self.base != other.base:
            raise ValueError("Bases must match for comparison")

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
            pos_self = BigInt(self.digits, self.base, False)
            pos_other = BigInt(other.digits, other.base, False)
            result = pos_self + pos_other
            result.is_negative = True
            return result

        # -A + B -> B - |A|
        # A + (-B) -> A - |B|
        elif self.is_negative != other.is_negative:
            pos_self = BigInt(self.digits, self.base, False)
            pos_other = BigInt(other.digits, other.base, False)
            return pos_other - pos_self if self.is_negative else pos_self - pos_other

        result_digits: list[int] = []
        carry = 0

        for digit_a, digit_b in zip_longest(self.digits, other.digits, fillvalue=0):
            current_sum = digit_a + digit_b + carry
            remain = current_sum % self.base
            carry = current_sum // self.base

            result_digits.append(remain)

        if carry > 0:
            result_digits.append(carry)

        return BigInt(result_digits, self.base, self.is_negative)


    def __sub__(self, other: BigInt) -> BigInt:
        if self.base != other.base:
            raise ValueError("Cannot subtract BigInts with different bases")

        # A - (-B) -> A + B
        # -A - B -> -(A + B)
        if self.is_negative != other.is_negative:
            pos_self = BigInt(self.digits, self.base, False)
            pos_other = BigInt(other.digits, other.base, False)
            result = pos_self + pos_other
            result.is_negative = self.is_negative
            return result

        pos_self = BigInt(self.digits, self.base, False)
        pos_other = BigInt(other.digits, other.base, False)

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
            else:
                borrow = 0

            result_digits.append(d)

        return BigInt(result_digits, self.base, self.is_negative)



    def __mul__(self, other: BigInt | int ) -> BigInt:
        if isinstance(other, int):
            return self._mul_by_int(other)

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

            if carry > 0:
                # Mathematically safer to use += here, though the cell is initially 0
                result_digits[i + len(other.digits)] += carry

        return BigInt(result_digits, self.base, result_is_negative)

    def __rmul__(self, other: int) -> 'BigInt':
        """Allows reverse multiplication like `3 * BigInt`."""
        return self * other

    def _mul_by_int(self, multiplier: int) -> 'BigInt':
        """
        Multiplies the BigInt by a small integer scalar in O(n) time.
        """
        if multiplier == 0:
            return BigInt([0], self.base)


        mul_len = 0
        copy_mul = multiplier
        while copy_mul:
            copy_mul //= 10
            mul_len += 1


        result_is_negative = self.is_negative != (multiplier < 0)
        multiplier = abs(multiplier)

        result_digits: list[int] = []
        carry = 0

        for digit in self.digits:
            current_val = digit * multiplier + carry
            result_digits.append (current_val % self.base)
            carry = current_val // self.base

        while carry > 0:
            result_digits.append(carry % self.base)
            carry //= self.base

        return BigInt(result_digits, self.base, result_is_negative)


    def __floordiv__(self, divisor: int) -> BigInt:
        if not isinstance(divisor, int):
            raise NotImplementedError("Division is currently only supported for standard int divisors.")
        if divisor == 0:
            raise ZeroDivisionError("Division by zero is undefined.")

        result_is_negative = self.is_negative != (divisor < 0)
        abs_divisor = abs(divisor)

        result_digits: list[int] = []
        remainder = 0

        for digit in reversed(self.digits):
            current_value = remainder * self.base + digit
            quotient = current_value // abs_divisor
            remainder = current_value % abs_divisor
            result_digits.append(quotient)

        result_digits.reverse()

        # Handle the edge case where the quotient is zero
        if not result_digits:
            result_digits = [0]

        return BigInt(result_digits, self.base, result_is_negative)

    def shift(self, k: int) -> BigInt:
            """
            Multiplies the BigInt by base^k by prepending k zeros.
            Since we use Little-endian representation, shifting means
            adding zeros to the beginning of the list.
            Time complexity: O(n + k).
            """
            if k <= 0 or (len(self.digits) == 1 and self.digits[0] == 0):
                return self

            shifted_digits = [0] * k + self.digits
            return BigInt(shifted_digits, self.base, self.is_negative)


    def mul_karatsuba_recursively(self, other: BigInt) -> BigInt:
        """
        Pure Karatsuba algorithm (O(n^1.585)) without thresholds.
        """
        if self.base != other.base:
            raise ValueError("Bases must match for multiplication")

        # Fallback to O(n^2) schoolbook multiplication when below threshold
        if len(self.digits) <= self.KARATSUBA_THRESHOLD or len(other.digits) <= self.KARATSUBA_THRESHOLD:
            return self * other

        max_len = max(len(self.digits), len(other.digits))

        # BASE CASE: Strictly isolated, drops to single digits
        if max_len <= 1:
            val_self = self.digits[0] if self.digits else 0
            val_other = other.digits[0] if other.digits else 0
            val = val_self * val_other

            res = [val % self.base, val // self.base] if val >= self.base else [val]
            result = BigInt(res, self.base)

            result.is_negative = self.is_negative != other.is_negative
            if len(result.digits) == 1 and result.digits[0] == 0:
                result.is_negative = False
            return result

        m = max_len // 2

        x0 = BigInt(self.digits[:m] or [0], self.base)
        x1 = BigInt(self.digits[m:] or [0], self.base)

        y0 = BigInt(other.digits[:m] or [0], other.base)
        y1 = BigInt(other.digits[m:] or [0], other.base)

        z0 = x0.mul_karatsuba_recursively(y0)
        z2 = x1.mul_karatsuba_recursively(y1)

        sum_x = x1 + x0
        sum_y = y1 + y0
        z1 = sum_x.mul_karatsuba_recursively(sum_y) - z2 - z0

        top_nums = z2.shift(2 * m)
        middle = z1.shift(m)

        final_result = top_nums + middle + z0

        final_result.is_negative = self.is_negative != other.is_negative
        if len(final_result.digits) == 1 and final_result.digits[0] == 0:
            final_result.is_negative = False

        return final_result


    def mul_toom_cook_3_recursively(self, other: BigInt) -> BigInt:
        """
        Pure Toom-Cook 3-way algorithm (O(n^1.465)) without thresholds.
        """
        if self.base != other.base:
            raise ValueError("Bases must match for multiplication")

        if len(self.digits) <= self.TOOM_THRESHOLD or len(other.digits) <= self.TOOM_THRESHOLD:
            return self.mul_karatsuba_recursively(other)

        max_len = max(len(self.digits), len(other.digits))

        # BASE CASE: Strictly isolated, drops to single digits
        if max_len <= 1:
            val_self = self.digits[0] if self.digits else 0
            val_other = other.digits[0] if other.digits else 0
            val = val_self * val_other

            res = [val % self.base, val // self.base] if val >= self.base else [val]
            result = BigInt(res, self.base)

            result.is_negative = self.is_negative != other.is_negative
            if len(result.digits) == 1 and result.digits[0] == 0:
                result.is_negative = False
            return result

        m = (max_len + 2) // 3

        x0 = BigInt(self.digits[:m] or [0], self.base)
        x1 = BigInt(self.digits[m:2*m] or [0], self.base)
        x2 = BigInt(self.digits[2*m:] or [0], self.base)

        y0 = BigInt(other.digits[:m] or [0], self.base)
        y1 = BigInt(other.digits[m:2*m] or [0], self.base)
        y2 = BigInt(other.digits[2*m:] or [0], self.base)

        p0 = x0
        p1 = x0 + x1 + x2
        p_minus_1 = x0 - x1 + x2
        p_minus_2 = x0 - x1 * 2 + x2 * 4
        p_inf = x2

        q0 = y0
        q1 = y0 + y1 + y2
        q_minus_1 = y0 - y1 + y2
        q_minus_2 = y0 - y1 * 2 + y2 * 4
        q_inf = y2

        r0 = p0.mul_toom_cook_3_recursively(q0)
        r1 = p1.mul_toom_cook_3_recursively(q1)
        r_minus_1 = p_minus_1.mul_toom_cook_3_recursively(q_minus_1)
        r_minus_2 = p_minus_2.mul_toom_cook_3_recursively(q_minus_2)
        r_inf = p_inf.mul_toom_cook_3_recursively(q_inf)

        w0 = r0
        w4 = r_inf
        w3 = (r_minus_2 - r1) // 3
        w1 = (r1 - r_minus_1) // 2
        w2 = r_minus_1 - w0
        w3 = (w2 - w3) // 2 + (w4 * 2)
        w2 = w2 + w1 - w4
        w1 = w1 - w3

        w4_shifted = w4.shift(4 * m)
        w3_shifted = w3.shift(3 * m)
        w2_shifted = w2.shift(2 * m)
        w1_shifted = w1.shift(m)

        final_result = w4_shifted + w3_shifted + w2_shifted + w1_shifted + w0

        final_result.is_negative = self.is_negative != other.is_negative
        if len(final_result.digits) == 1 and final_result.digits[0] == 0:
            final_result.is_negative = False

        return final_result


if __name__ == "__main__":
    pass
    #num1_str = "123456789" * 10  # 90-digit number to force Toom-Cook recursion
    #num2_str = "987654321" * 10

    #b1 = BigInt.from_string(num1_str, 10)
    #b2 = BigInt.from_string(num2_str, 10)

    # Python built-in math verification
    #expected_result = str(int(num1_str) * int(num2_str))

    #print("Testing Karatsuba...")
    #assert str(b1.mul_karatsuba_recursively(b2)) == expected_result

    #print("Testing Toom-Cook 3...")
    #assert str(b1.mul_toom_cook_3_recursively(b2)) == expected_result

    #print("All algorithms passed successfully!")