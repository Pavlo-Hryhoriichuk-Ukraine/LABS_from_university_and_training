#lab15_2 (multiprocessing,itertools + vertexes of polygons)
import math
import itertools
import time
from concurrent.futures import ProcessPoolExecutor, wait
import multiprocessing


def get_distance(p1: tuple, p2: tuple) -> float:
    """Calculates distance between two points"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def get_vector(p1: tuple, p2: tuple) -> tuple:
    """Return vector from p1 to p2"""
    return tuple(b - a for a, b in zip(p1, p2))

def cross_product(v1: tuple, v2: tuple) -> tuple:
    """return cross product of v1 and v2"""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )

def dot_product(v1: tuple, v2: tuple) -> float:
    """Scalar product of two vectors"""
    return sum(a * b for a, b in zip(v1, v2))

def is_in_one_surface(points: tuple) -> bool:

    if len(points) <= 3:
        return True

    p0, p1, p2 = points[0], points[1], points[2]

    v1 = get_vector(p0, p1)
    v2 = get_vector(p0, p2)

    normal = cross_product(v1, v2)
    
    return all(math.isclose(dot_product(normal, get_vector(p0, p_i)), 0.0, abs_tol=1e-3) for p_i in points[3:])

def is_right(points: tuple, n: int) -> bool:

    # zip(*points) геніально групує всі x разом, всі y разом, і всі z.
    center = tuple(sum(coord) / n for coord in zip(*points))
    
    r0 = get_distance(points[0], center)
    
    if not all(math.isclose(get_distance(p, center), r0, abs_tol=1e-3) for p in points[1:]):
        return False
        
    dists = [get_distance(p1, p2) for p1, p2 in itertools.combinations(points, 2)]
    
    min_dist = min(dists)
    
    side_count = sum(1 for d in dists if math.isclose(d, min_dist, abs_tol=1e-3))
    
    return side_count == n



def find_n_gons(n: int, lst_of_points: list, dict_of_values: dict) -> None:
    count = sum(
        1 for group in itertools.combinations(lst_of_points, n) 
        if is_in_one_surface(group) and is_right(group, n)
    )
    
    if count > 0:
        dict_of_values[f"{n}-кутник"] = count

def find_n_gons_seq(n: int, lst_of_points: list) -> tuple:

    count = sum(
        1 for group in itertools.combinations(lst_of_points, n) 
        if is_in_one_surface(group) and is_right(group, n)
    )
    return f"{n}-кутник", count

def main():
    # Координати вершин правильного додекаедра (20 точок)
    lst_of_points = [
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
        (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
        (0, 0.618034, 1.618034), (0, 0.618034, -1.618034),
        (0, -0.618034, 1.618034), (0, -0.618034, -1.618034),
        (0.618034, 1.618034, 0), (0.618034, -1.618034, 0),
        (-0.618034, 1.618034, 0), (-0.618034, -1.618034, 0),
        (1.618034, 0, 0.618034), (1.618034, 0, -0.618034),
        (-1.618034, 0, 0.618034), (-1.618034, 0, -0.618034)
    ]

    # Перевіряємо n від 3 до кількості точок
    ns_to_check = range(3, len(lst_of_points) + 1)

    print("--- 1. Послідовне обчислення (одне ядро) ---")
    start_time_seq = time.time()
    
    # Знову уникаємо for, використовуючи генератор словника
    seq_results = {
        name: count for name, count in 
        (find_n_gons_seq(n, lst_of_points) for n in ns_to_check) 
        if count > 0
    }
    
    end_time_seq = time.time()
    print(f"Результат: {seq_results}")
    print(f"Час виконання: {end_time_seq - start_time_seq:.2f} секунд\n")

    print("--- 2. Паралельне обчислення (multiprocessing) ---")
    start_time_mp = time.time()
    
    # Використовуємо Manager для створення словника, доступного для всіх процесів
    with multiprocessing.Manager() as manager:
        dict_of_values = manager.dict()
        
        # ProcessPoolExecutor автоматично розподілить задачі по ядрах процесора
        with ProcessPoolExecutor() as executor:
            # Створюємо список задач генератором списку
            futures = [executor.submit(find_n_gons, n, lst_of_points, dict_of_values) for n in ns_to_check]
            wait(futures)
            
        mp_results = dict(dict_of_values)
        
    end_time_mp = time.time()
    print(f"Результат: {mp_results}")
    print(f"Час виконання: {end_time_mp - start_time_mp:.2f} секунд")

if __name__ == '__main__':
    main()