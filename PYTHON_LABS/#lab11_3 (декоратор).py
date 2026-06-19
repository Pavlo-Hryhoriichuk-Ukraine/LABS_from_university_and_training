#lab11_3 (декоратор)
from typing import Callable
import functools

def derivative(func: Callable, point: float, dx: float = 0.00000000001) -> float:
    return func(point + dx) - func(point) / dx

def max_min_value_of_function(a: float | int, b: float | int, eps: float) -> Callable:
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper() -> list: 

            accuracy = 1

            while epsilon <= 1:
                accuracy *= 10
                epsilon *= 10

            first_value = (a,f(a))
            second_value = (b,f(b))
            x_points = (i for i in range(a, b, accuracy))
            dict_of_values = {f(point) : point for point in x_points if derivative(f,point) < eps}

            if len(dict_of_values.values()) == 0:
                values = first_value[1], second_value[1]
            else:
                values = first_value[1], second_value[1], max(dict_of_values), min(dict_of_values)

            max_value = max(values)
            min_value = min(values)

            if max_value in dict_of_values.keys():
                max_SORCE = tuple((dict_of_values[max_value], max_value))

            elif max_value == first_value[1]:
                max_SORCE = first_value
            elif max_value == second_value[1]:
                max_SORCE = second_value
            
            if min_value in dict_of_values.keys():
                min_SORCE = tuple((dict_of_values[min_value], min_value))

            elif min_value == first_value[1]:
                min_SORCE = first_value
            elif min_value == second_value[1]:
                min_SORCE = second_value

            lst = [("min",min_SORCE),("max",max_SORCE)]
            return lst
        return wrapper
    return decorator

def main():
    @max_min_value_of_function(1,4,0.0001)
    def x_squared(x):
        return x**2
    print(x_squared())

if __name__ == "__main__":
    main()
