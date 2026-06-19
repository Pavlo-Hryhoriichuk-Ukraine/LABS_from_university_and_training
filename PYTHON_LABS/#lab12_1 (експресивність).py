#lab12_1 (експресивність, трикутник Паскаля)

def recursively_print_Pascal_triangle_PLUS_CATALAN_NUMBERS(n: int) -> list[int]:
    """
    Recursive option of solving Pascal`s triangle. Uses shifts in Pascal`s triangle
    string (left and right) to print n+1 string of Pascal`s triangle
    """
    if n == 0:
        print("1 --- КАТАЛАН(0) --> 1 ")
        return [1]
    else:
        prev_lst = recursively_print_Pascal_triangle_PLUS_CATALAN_NUMBERS(n-1)
        left_shift = [0] + prev_lst
        right_shift = prev_lst + [0]
        new_lst = [sum(elem) for elem in zip(left_shift,right_shift)]
        str_lst = list(map(str,new_lst))
        if n % 2 == 0:
            str_lst.append(f"--- КАТАЛАН({n//2}) --> {new_lst[n//2] - new_lst[n//2-2]}")
        print(" ".join(str_lst))
        return new_lst

def non_recursively_print_Pascal_triangle(n: int):
    """
    Docstring for non_recursively_print_Pascal_triangle
    
    :param n: Description
    :type n: int

    :DETAIL: Writes every Pascal`s string to list and according to it
    fiends n+1 string of Pascal`s triangle.
    """
    match n:
        case 0:
            lst_group = [["1"]]
        case 1:
            lst_group = [["1"],["1","1"]]
        case _:
            lst_group = [["1"],["1","1"]]
            target_lst_group_lenght = n + 1
            while len(lst_group) < target_lst_group_lenght:
                last_group = lst_group[-1]
                group_to_append_lst = [str(int(last_group[i]) + int(last_group[i+1])) for i in range(len(last_group)-1)]
                group_to_append_lst = ["1"] + group_to_append_lst + ["1"]
                lst_group.append(group_to_append_lst)
            print(*map(" ".join,lst_group), sep="\n")

def main():
    try:
        n = int(input("Input integer number: "))
        print("\n\n----- TASK(1) RECURSIVE + TASK(3) CATALAN ----")
        recursively_print_Pascal_triangle_PLUS_CATALAN_NUMBERS(n)
        print("\n ---TASK (2) NON_RECURSIVE---")
        non_recursively_print_Pascal_triangle(n)
    except:
        print("Будь ласка, введіть коректне число")

if __name__ == "__main__":
    main()