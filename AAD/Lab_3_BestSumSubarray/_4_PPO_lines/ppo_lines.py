from random import randint, sample

class StraightLine:
    def __init__(self, k, b):
        self.k = k
        self.b = b

    def find_intersection_point(self, other: 'StraightLine'):
        # Calculates the x-coordinate where two lines intersect
        return (other.b - self.b) / (self.k - other.k)

    def __str__(self):
        return f"{self.k}x + {self.b}"


def find_lower_envelope(lines_lst: list[StraightLine]) -> list[StraightLine]:
    stack = [lines_lst[0], lines_lst[1]]

    for i in range(2, len(lines_lst)):
        L_new = lines_lst[i]

        # The loop runs ONLY if we have at least 2 lines to compare
        while len(stack) >= 2:
            L_top = stack[-1] # the highest in stack
            L_prev = stack[-2] # the one before "the highest"

            x1 = L_top.find_intersection_point(L_prev)
            x2 = L_new.find_intersection_point(L_top)

            # If L_new covered L_top before L_top could escape from L_prev
            if x2 <= x1:
                stack.pop() # pops L_top
            else:
                break # No overlapping, we can safely exit the while loop

        # Append the new line after filtering out the covered ones
        stack.append(L_new)

    return stack


if __name__ == '__main__':
    # 1. Generate 19 unique k values to avoid ZeroDivisionError (parallel lines)
    unique_k_values = sample(range(-20, 20), 19)
    lines_lst = [StraightLine(k=k_val, b=randint(0, 20)) for k_val in unique_k_values]

    # 2. Sort by slope (k) in descending order
    lines_lst.sort(key=lambda line: line.k, reverse=True)

    print("--- Full sorted lines list ---")
    for line in lines_lst:
        print(line)

    print("\n--- Results (Lower Envelope) ---")
    # find_lower_envelope returns a list, so we can iterate over it directly
    for line in find_lower_envelope(lines_lst):
        print(line)