#lab12_3 (generate random email)
import re
import random
from typing import Literal

def clear_input(user_input: str) -> list[tuple[str]]:
    """
    Docstring for clear_input
    
    :param user_input: Description
    :type user_input: str
    :return: Description
    :rtype: list[tuple[str]]
    :DETAILS: Hepls with preparing and clearing inputed text, usesing "re" MODULE.
    """
    lst_clear_user_input = user_input.split(';')
    lst_clear_user_input = [elem.split(",") for elem in lst_clear_user_input]
    lst_clear_tuple = [(re.sub(r"[^a-zA-Zа-яА-ЯіїєґІЇЄҐ`]","",group[0]).strip(),re.sub(r"[^a-zA-Zа-яА-ЯіїєґІЇЄҐ`]","",group[1]).strip(), re.sub(r"[^0-9]","",group[2]).strip()) for group in lst_clear_user_input]
    return lst_clear_tuple

def generate_random_email(lst: list[tuple[str]]) -> list[tuple[str]]:
    """
    Docstring for generate_random_email
    
    :param lst: Description
    :type lst: list[tuple[str]]
    :return: Description
    :rtype: list[tuple[str]]
    :DETAILS: Generates random "correct" and "protected" email for every user,
    and append it into user`s tuple in list.
    """

    new_lst = []
    for elem in lst:
        number_of_letters = random.randint(5,10)
        number_of_big_letters = random.randint(1,number_of_letters//2)
        number_of_digits = random.randint(1,number_of_letters//2)
        number_of_letters_after_dog = random.randint(3,6)
        number_of_letters_after_dot = random.randint(2,5)
        number_of_special_symbols = random.randint(1,3)

        email = ""
        for i in range(number_of_letters):
            number = random.randint(97,112)
            letter = chr(number)
            email += letter
        for i in range(number_of_digits):
            number = random.randint(48,57)
            digit = chr(number)
            email += digit
        for i in range(number_of_special_symbols):
            number = random.randint(13785,182487)
            symbol = chr(number)
            email += symbol
        for i in range(number_of_big_letters):
            number = random.randint(65,90)
            big_letter = chr(number)
            email += big_letter
        email += "@"
        for i in range(number_of_letters_after_dog):
            number = random.randint(97,112)
            letter = chr(number)
            email += letter
        email += "."
        for i in range(number_of_letters_after_dot):
            number = random.randint(97,122)
            letter = chr(number)
            email += letter
        elem += (email,)
        new_lst.append(elem)
    return new_lst

def sort_our_list(lst: list[tuple[str]], praram1: Literal["asc", "desc"], param2: Literal["asc", "desc"]) -> list[tuple[str]]:
    """
    Docstring for sort_our_list
    
    :param lst: Description
    :type lst: list[tuple[str]]
    :param praram1: Description
    :type praram1: str
    :param param2: Description
    :type param2: str
    :return: Description
    :rtype: list[tuple[str]]

    :DETAIL: Sorting our list according to your`s parameters, fistly by year, secondary by
    alphabet. And also delate unadoult users.
    """
    lst = filter(lambda x: 2026 - int(x[2]) >= 18, lst)

    match praram1:
        case "asc":
            lst = sorted(lst,key=lambda x: int(x[2]),reverse=True)
        case "desc":
            lst = sorted(lst,key=lambda x: int(x[2]))
    
    match param2:
        case "asc":
            for i in range(len(lst)-1):
                if lst[i][2] == lst[i+1][2]:
                    if lst[i][0] > lst[i+1][0]:
                        lst[i], lst[i+1] = lst[i+1], lst[i]
            return lst
        case "desc":
            for i in range(len(lst)-1):
                if lst[i][2] == lst[i+1][2] and lst[i][0] == lst[i+1][0]:
                    if lst[i][1] < lst[i+1][1]:
                        lst[i], lst[i+1] = lst[i+1], lst[i]
                elif lst[i][2] == lst[i+1][2]:
                    if lst[i][0] < lst[i+1][0]:
                        lst[i], lst[i+1] = lst[i+1], lst[i]
            return lst

def main():
    user_input = "Па/вл4о,Гр4иг1орійч%ук,20D#07;Алі12н{а,Ол14е{нюк,20-08; Ро3м*-ан,Ше21в5чук, 2o0I08"
    param1 = "asc"
    param2 = "desc"
    print(sort_our_list(generate_random_email(clear_input(user_input)), param1, param2))

if __name__ == "__main__":
    main()