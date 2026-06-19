#lab10_2 (функція integrate(декоратори...))
from typing import Callable
import random
from math import ceil

def get_first_derevative(func: Callable, point: int | float, dx: float = 0.0001) -> int | float:
    """
    Fiends derevative of function in specific point
    """
    return (func(point+dx) - func(point)) / dx

def get_second_derivative(func: Callable, x: float, h: float = 0.0001) -> float:
    """
    Calculate a second derevative
    """
    return (func(x + h) - 2 * func(x) + func(x - h)) / (h**2)


def integrate(func:Callable,parameters: tuple[int|float], method: Callable):
   """
   Hepls with integration of function with inputed method
   """
   return method(func, parameters)

def left_triangles(func: Callable, parameters: tuple[int | float]):
    start, end, step = parameters
    n = (end - start) / step
    total_sum = sum(func(start + i * step) for i in range(ceil(n)))
    error = (((end-start) ** 2) / (2*n)) * get_max_derevative_value(func,start,end, get_first_derevative)
    return total_sum * step, error # total_sum * step -> our full area, instead of multiplying each appendix 

def right_triangles(func: Callable,parameters: tuple[int|float]):
    start, end, step = parameters
    n = (end - start) / step
    total_sum = sum(func(start + i * step) for i in range(1,ceil(n + 1)))
    error = (((end-start) ** 2) / (2*n)) * get_max_derevative_value(func,start,end, get_first_derevative)
    return total_sum * step, error

def central_triangles(func: Callable,parameters: tuple[int|float]):
    start, end, step = parameters
    n = (end - start) / step
    total_sum = sum(func(start + i * step + step / 2) for i in range(ceil(n)))
    error = (((end-start) ** 3) / (24*n**2)) * get_max_derevative_value(func,start,end, get_second_derivative)
    return total_sum * step,error

def trapezoid(func: Callable,parameters: tuple[int | float]):
    start, end, step = parameters
    n = (end - start) / step
    adder = (func(start) + func(end)) / 2
    total_sum = sum(func(start + i * step) for i in range(1,ceil(n)))
    error = (((end-start) ** 3) / (12*n**2)) * get_max_derevative_value(func,start,end, get_second_derivative)
    return step *(adder + total_sum),error

def get_max_derevative_value(func: Callable[[float],float], start: float, end: float, derev_func: Callable) -> float:
    """ 
    Fiends max derevative value of function in segment
    """
    max_value = 0
    for i in range (1,1001):
        value = abs(derev_func(func,random.randint(start,end)))
        if value > max_value:
            max_value = value
    return max_value

def main():
    print(integrate(lambda x: x**2, (1,5,0.0001), trapezoid))
    
if __name__ == "__main__":
    main()