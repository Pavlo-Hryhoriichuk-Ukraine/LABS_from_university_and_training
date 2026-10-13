from pathlib import Path


class StackUnderflowError(Exception):
    def __str__(self) -> str:
        return "Missing opening bracket (Stack Underflow)"


class BracketMismatchError(Exception):
    def __str__(self) -> str:
        return "Bracket types do not match (Nesting Violation)"


class UnclosedBracketError(Exception):
    def __str__(self) -> str:
        return "Missing closing bracket (Stack Not Empty)"


def is_balanced(expression: str) -> bool:
    stack: list[str] = []
    BRACKET_MAP = {
        ')': '(',
        ']': '[',
        '}': '{',
    }

    OPENING_BRACKETS = frozenset(BRACKET_MAP.values())

    for char in expression:
        if char in OPENING_BRACKETS:
            stack.append(char)

        elif char in BRACKET_MAP:
            if not stack:
                raise StackUnderflowError

            if BRACKET_MAP[char] != stack[-1]:
                raise BracketMismatchError

            stack.pop()

    if stack:
        raise UnclosedBracketError

    return True


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    test_files = ["test_1.txt", "test_2.txt", "test_3.txt"]

    print("--- File Bracket Balancing Analysis ---")
    for filename in test_files:
        file_path = current_dir / filename

        content = file_path.read_text(encoding="utf-8")
        try:
            is_balanced(content)
            print(f"SUCCESS: '{filename}' is perfectly balanced.")
        except Exception as e:
            print(f"FAILED : '{filename}' -> {e}")