#lab10_1(point coordinates,3 functions)

import math

def point_coordinates() -> tuple[int]:
    """
    Docstring for point_coordinates
    
    :return: Description
    :rtype: tuple[int]
    """
    tuple_of_coordinates = tuple(map(int,input("Input point coordinates: ").split()))
    return tuple_of_coordinates

def point_distance(coord1: tuple[int | float],coord2: tuple[int | float]) -> int | float:
    """
    Docstring for point_distance
    
    :param coord1: Description
    :type coord1: tuple[int | float]
    :param coord2: Description
    :type coord2: tuple[int | float]
    :return: Description
    :rtype: int | float
    """
    zip_lst = zip(coord1,coord2)
    distance = math.sqrt(sum((map((lambda x: (x[0]-x[1])**2),zip_lst))))
    return distance

def triangular_area(a: float | int, b: float | int, c: float | int) -> float | int:
    """
    Docstring for triangular_area
    
    :param a: Description
    :type a: float | int
    :param b: Description
    :type b: float | int
    :param c: Description
    :type c: float | int
    :return: Description
    :rtype: float | int
    """
    half_perimeter = (a + b + c) / 2
    area = math.sqrt(half_perimeter * (half_perimeter - a) * (half_perimeter - b) * (half_perimeter - c))
    return area

def height_of_a_triangle(our_point: tuple[int | float], second_point, third_point, area: int | float) -> str:
    """
    Docstring for height_of_a_triangle
    
    :param coord_tuple: Description
    :type coord_tuple: int | float
    :param area: Description
    :type area: int | float
    :return: Description
    :rtype: str
    """
    side = point_distance(second_point, third_point)
    height = area * 2 / side
    print(f"Висота трикутника, опущена з вершини {(our_point)}: {height:.2f}")

def main():
    a = point_coordinates()
    b = point_coordinates()
    c = point_coordinates()

    a_side = point_distance(b,c)
    b_side = point_distance(a,c)
    c_side = point_distance(a,b)
    area = triangular_area(a_side,b_side,c_side)

    height_of_a_triangle(our_point=a, second_point=b, third_point=c, area=area)
    height_of_a_triangle(our_point=b, second_point=a, third_point=c, area=area)
    height_of_a_triangle(our_point=c, second_point=a, third_point=b, area=area)

if __name__ == "__main__":
    main()
