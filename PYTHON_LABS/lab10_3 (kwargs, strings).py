#lab10_3 (**kwargs, strings)
s1 = "I will go to school."
s2 = "They will go to university;"
s3 = "We will go for a walk,"
from typing import Callable

def log(*args: tuple[str], union, intersection, difference, symmetric_difference, **kwargs: dict[str,tuple[int]]) -> str:

    translation_dict = {index + 1: set(elem.strip(",. :;?\"\'-()!%`").split()) for index,elem in enumerate(args)}
    for key, value in kwargs.items():
        lst_of_sets = [translation_dict[elem] for elem in value]
        match key:
            case "union_":
                union(lst_of_sets)
            case "intersection_":
                intersection(lst_of_sets)
            case "difference_":
                  difference(lst_of_sets)
            case "symmetric_difference_":
                  symmetric_difference(lst_of_sets)
                  

def union(lst: list[set[str]]) -> str:
        for i in range(1,len(lst)):
            lst[0] = lst[0].union(lst[i])
        print(",".join(lst[0]))
    
def intersection(lst: list[set[str]]) -> str:
        for i in range(1,len(lst)):
            lst[0] = lst[0].intersection(lst[i])
        print(",".join(lst[0]))        

def difference(lst: list[set[str]]) -> str:
        for i in range(1,len(lst)):
            lst[0] = lst[0].difference(lst[i])
        print(",".join(lst[0]))
    
def symmetric_difference(lst: list[set[str]]) -> str:
        for i in range(1,len(lst)):
            lst[0] = lst[0].symmetric_difference(lst[i])
        print(",".join(lst[0]))

if __name__ == "__main__":
    print(log(s1,s2,s3,union=union, intersection=intersection, difference=difference, symmetric_difference=symmetric_difference, union_=(1,2),intersection_=(1,2,3),symmetric_difference_=(2,3) , difference_=(1,2,3)))