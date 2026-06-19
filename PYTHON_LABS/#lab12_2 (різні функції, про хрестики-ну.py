#lab12_2 (різні функції, про хрестики-нулики RANDOM)
from random import choice

def create_random_tic_tac_toe_board() -> list[list[str]]:
    """
    Docstring for create_random_tic_tac_toe_board
    
    :return: Description
    :rtype: list[list[str]]

    :DETAILS: Creates a list of lists (board) using random LIBRARY
    """
    choices_lst = ["*","X","0"]
    board_lst = [[choice(choices_lst) for i in range(3)] for j in range (3)]
    return board_lst

def allowed_case(lst: list[list[str]]) -> bool | list:
    """
    Docstring for allowed_case
    
    :param lst: Description
    :type lst: list[list[str]]
    :return: Description
    :rtype: bool | list

    :DETAILS: Checks if case of board are allowed to using "who_wins()"
    function 
    """
    opened_lst = [v for group in lst for v in group]
    if opened_lst.count("X") == opened_lst.count("0") or opened_lst.count("X") == opened_lst.count("0") + 1:
        return lst
    else:
        return []

def who_won(lst:list[list[str]]) -> str:
    """
    Docstring for who_wins
    
    :param lst: Description
    :type lst: list[list[str]]
    :return: Description
    :rtype: str

    :DETAILS: If case are not allowed, returns [], outherwise determines
    who won in tic_tac_toe game or it was a draw. Uses all() function, zip()...
    """
    if not lst:
        return []
    
    who_won_lst = []

    #1 ckeck (horizontal(normal))
    for group in lst:
        result_X = all(elem == 'X' for elem in group)
        result_0 = all(elem == '0' for elem in group)
        if result_X:
             who_won_lst.append("X")
        if result_0:
            who_won_lst.append("0")
        
    #2 check (vertical)
    zip_lst = list(zip(*lst))
    for group in zip_lst:
        result_X = all(elem == 'X' for elem in group)
        result_0 = all(elem == '0' for elem in group)
        if result_X:
            who_won_lst.append("X")
        if result_0:
            who_won_lst.append("0")
        
    #3 check (diagonal)
    target1 = lst[0][0]
    target2 = lst[0][2]

    if lst[1][1] == target1 and lst[2][2] == target1:
        if target1 != "*": who_won_lst.append(target1)

    if lst[1][1] == target2 and lst[2][0] == target2:
        if target2 != "*" : who_won_lst.append(target2)

    if len(who_won_lst) == 1:
        return "".join(who_won_lst)
    else:
        return '*'

def main():
    counter_X = 0
    counter_0 = 0
    counter_draw = 0
    counter_uncorrect_board = 0

    for i in range(100000):
        result = who_won(allowed_case(create_random_tic_tac_toe_board()))
        match result:
            case []:
                counter_uncorrect_board += 1
            case "X":
                counter_X += 1
            case "0":
                counter_0 += 1
            case "*":
                counter_draw += 1
    print(f"Persentage of 'X' wins: {((counter_X/100000)*100):.3f} %",
        f"Persentage of '0' wins: {((counter_0/100000)*100):.3f} % ",
        f"Persentage of draws: {((counter_draw/100000)*100):.3f} %",
        f"Persentage of uncorrect boards: {((counter_uncorrect_board/100000)*100):.3f} %", sep="\n")

if __name__ == "__main__":
    main()