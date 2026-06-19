#lab13_3 (functions and collaborations)
import random
import math
import itertools
import numpy as np

def gen_rand_int_list_n_(n:int) -> list[int]:
    lenght = random.randint(1,5)
    int_list_n = [random.randint(-n,n) for i in range(lenght)]
    return int_list_n

def is_coeffs_in_quadratic_equation(int_list_n: list[int],n:int) -> list[int]:
        lenght = len(int_list_n)
        assert lenght >= 3

        match lenght:
            case 3:
                for elem in int_list_n:
                    assert elem != 0
                return int_list_n
            
            case 4:
                assert int_list_n[0] == 0
                for elem in int_list_n[1:]:
                    assert elem != 0
                return int_list_n[1:]
            
            case 5:
                assert int_list_n[0] == 0 and int_list_n[1] ==0
                for elem in int_list_n[2:]:
                    assert elem != 0
                return int_list_n[2:]
        
def specificly_solve_quadratic_equation(list_to_solve: list[int], n:int) -> tuple[float | float] | ValueError | TypeError | RuntimeError:
    a,b,c = list_to_solve
    D = b**2 - 4*a*c
    try:
        assert D > 0
    except AssertionError:
        raise ValueError(f"D<0 для коефіцієнтів {a}, {b}, {c}")
    else:
        coef_sum = a + b + c
        try:
            assert coef_sum == n
            return float(-b + math.sqrt(D)) /2*a , float(-b - math.sqrt(D)) /2*a
        
        except AssertionError:
            try:
                assert coef_sum > n
                raise TypeError
            
            except AssertionError:
                raise RuntimeError

def controler(N:int, n:int) -> list[list[float],dict[str,int]]:
    roots_gen = map((lambda _: specificly_solve_quadratic_equation(is_coeffs_in_quadratic_equation(gen_rand_int_list_n_(n),n),n)),range(N))
    final_lst = []
    dict_of_errors = {ValueError: 1, TypeError : 1, RuntimeError : 1, AssertionError: 1}

    def safe_iteration(roots_gen):
        nonlocal dict_of_errors
        nonlocal final_lst
        try:
            final_lst.append(*next(roots_gen))
        except ValueError as e:
            print(e)
            dict_of_errors[ValueError] += 1
        except TypeError:
            dict_of_errors[TypeError] += 1
        except RuntimeError:
            dict_of_errors[RuntimeError] += 1
        except AssertionError:
            dict_of_errors[AssertionError] += 1
    
    list(map(lambda _: safe_iteration(roots_gen),range(N)))
    print(dict_of_errors)
    print(final_lst)
    return final_lst

def count_and_sum_elems(final_lst:list[float]) -> str:
    counter = 0
    gen = map(str,final_lst)

    def iter():
        next(gen)
        nonlocal counter
        counter += 1
    
    try:
        itertools.repeat(iter(),np.inf)
    except StopIteration:
        return f"Number of elements: {counter}; sum of elements: {sum(final_lst)}"

def main():
    print(count_and_sum_elems(controler(100000,5)))

if __name__ == "__main__":
    main()