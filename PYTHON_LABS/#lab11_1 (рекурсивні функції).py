#lab11_1 (рекурсивні функції)

def find_n_member(b1: int, n: int, q: int) -> int:
    """
    finding n-member of a geometric progression
    """
    if n == 1:
        return b1
    else:
        return find_n_member(b1, n-1, q) *q

def find_n_summa(b1: int, n: int, q) -> int:
    """
    calculation sum of n-members in geometric progression
    """
    if n == 1:
        return b1
    else:
        return find_n_member(b1, n, q) + find_n_summa(b1, n-1, q)

def sum_of_digits(number: str) -> int:
    """
    calculation sum of digits in n-member of geometric progression
    """
    if not number:
        return 0
    return int(number[0]) + sum_of_digits(number[1:])
    
def max_digit(n_member_str: str) -> int:
    """
    fiends max digit in n-member of geometric progression
    """
    if len(n_member_str) == 1:
        return int(n_member_str)
        
    first = int(n_member_str[0])
    max_rest = max_digit(n_member_str[1:])
        
    return first if first > max_rest else max_rest
            
def find_specific_number(n_member_str: str, specific_number: str) -> bool:
    """
    fiends specific number in n-member. During finding, if string
    will become empty, return False, if successed - return True.
    """
    try:
        if n_member_str[0] == specific_number:
            return True
        else:
            try:
                return find_specific_number(n_member_str[1:], specific_number)
            except ValueError:
                return False
    except IndexError:
        return False
    
def main():
    b1 = int(input("Input first member: "))
    q= int(input("Input denominator: ")) #знаменник
    n = int(input("Input n-number: "))
    specific_number = str(input("Input specific number: "))

    n_member = str(find_n_member(b1, n, q))

    print(f"b[{n}] - {n_member}")
    print(f"S[{n}] - {find_n_summa(b1, n, q)}")
    print(f"Sum of digits in member[{n}] = {sum_of_digits(n_member)}")
    print(f"Max digit in member[{n}] = {max_digit(n_member)}")
    print(f"The assertion that there is a specific_symbol in the mumber[{n}] was: {find_specific_number(n_member, specific_number)} ")
            
if __name__ == "__main__":
    main()