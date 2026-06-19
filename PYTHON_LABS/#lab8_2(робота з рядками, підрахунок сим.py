#lab8_2(робота з рядками, підрахунок символів, визначення спільного)

#a
def count_words(list_of_words_1,list_of_words_2) -> int:
    return len(list_of_words_1) + len(list_of_words_2)

#б,в
def find_special_letter_words(list_of_words: list, special_letter: str) -> tuple[int,int]:
    begin_counter = 0
    end_counter = 0

    for word in list_of_words:
        if word[0] == special_letter:
            begin_counter += 1
        if word[-1] == special_letter:
            end_counter += 1

    return begin_counter, end_counter

#г
def find_special_words_1(list_of_words_1: list[str], list_of_words_2: list[str]) -> list[str]:
    #edited

    #special_words = [(f"{word} " * counter).split() for word in list_of_words_1 if (counter :=list_of_words_2.count(word)) > 1]
    #special_words = [word for group in special_words for word in group]
   #         if not list_of_words_2.count(word) == 1:
    #            #edited
    #            for i in range (list_of_words_2.count(word)):
    #                special_words.append(word)
    #    else:
    #        special_words.append(word)
    
    return set(list_of_words_1).difference(set(list_of_words_2))

#д
def find_special_words_2(first_set: set, second_set: set) -> set[str]:
    return first_set.intersection(second_set)

#е
def find_unique_words(first_set: set[str], second_set: set[str]) -> set[str]:
     return find_special_words_2(first_set,second_set).intersection(find_special_words_2(second_set,first_set))

#є
def one_words(first_set: set[str], second_set: set[str], list_of_words_1: list[str], list_of_words_2: list[str]):
    lst_1 = [elem for elem in first_set if list_of_words_1.count(elem) == 1]
    lst_2 = [elem for elem in second_set if list_of_words_2.count(elem) == 1]

    #list_of_unique_words = []
    #mix_set = first_set.union(second_set)
    #for word in mix_set:
    #    if word in list_of_words_1 and list_of_words_2:
    #        if list_of_words_1.count(word) == 1 and list_of_words_2.count(word) == 1:
    #            list_of_unique_words.append(word)
    #       else:
    #            pass
    #    else:
    #        pass
    
    return set(lst_1).union(set(lst_2))

#ж
def symm_differ(first_set: set[str], second_set: set[str]):
    lst = first_set.symmetric_difference(second_set)
    if lst:
        return list(lst)
    return []


#функція для виклику результату
def main():
    list_of_words_1 = input("Input your string 1: ").split()
    list_of_words_2 = input("Input your string 2: ").split()
    special_letter = input("Input your special letter: ")
    first_set = set(list_of_words_1)
    second_set = set(list_of_words_2)

    # для того,щоб нормально додати результати роботи двох функцій
    a,b = find_special_letter_words(list_of_words_1,special_letter)
    c,d = find_special_letter_words(list_of_words_2, special_letter)
    a += c
    b += d

    final_lst = [] 
    final_lst.append(('a', count_words(list_of_words_1,list_of_words_2)))
    final_lst.append(('б',a))
    final_lst.append(('в', b))
    final_lst.append(('г',find_special_words_1(list_of_words_1,list_of_words_2)))
    final_lst.append(('д', list(find_special_words_2(first_set, second_set))))
    final_lst.append(('e', list(find_unique_words(first_set, second_set))))
    final_lst.append(('є', one_words(first_set, second_set, list_of_words_1, list_of_words_2)))
    final_lst.append(('ж', symm_differ(first_set, second_set)))
#edited
    return final_lst
#printlist((('a', count_words(list_of_words_1,list_of_words_2)), ('б',a), ('в', b),('г',find_special_words_1(list_of_words_1,list_of_words_2)),
           #     ('д', list(find_special_words_2(first_set, second_set))), ('e', list(find_special_words_2(first_set, second_set))),
           #     ('є', one_words(first_set, second_set, (list_of_words_1, list_of_words_2)), ('ж', symm_differ(first_set, second_set)))))

if __name__ == "__main__":
    main()