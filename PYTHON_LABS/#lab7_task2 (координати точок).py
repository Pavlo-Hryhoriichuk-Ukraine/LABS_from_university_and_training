#lab7_task2 (координати точок)
import itertools
import math
points = []
k = 0
q = 0
def distance(p1,p2):
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    return (x1 - x2)**2 + (y1 - y2) **2 + (z1 - z2)**2

for i in range (1,6):
    point = input("Input point coordinates: ")
    coordinates = list(map(int,point.split()))
    points.append(coordinates)

for (p1,p2) in itertools.combinations(points, 2):
    max_dist = 0
    dist = math.sqrt(distance(p1,p2))
    if dist > max_dist:
        max_dist = dist
        max_point_1 = p1
        max_point_2 = p2
print(f"Відстань між точками {max_point_1} та {max_point_2} найбільша, та має значення: {max_dist:.3f}")


for (p1,p2,p3) in itertools.combinations(points, 3):
    squares_of_distances = []
    for (A,B) in itertools.combinations([p1,p2,p3], 2):
        side = distance(A,B)
        squares_of_distances.append(side)
        squares_of_distances = tuple(squares_of_distances)
        squares_of_distances = list(squares_of_distances)
    is_right_triangle = math.isclose(squares_of_distances[0] + squares_of_distances[1], squares_of_distances[2])
    if is_right_triangle:
        q = 1
        print(f"Точки {p1},{p2},{p3} утворюють прямокутний трикутник")
if q == 0:
    print("Жодні точки не утворюють прямокутний трикутник")



def determinant_3x3_(vector1,vector2,vector3):
    plus_part = (vector1[0] * vector2[1] * vector3[2]) + (vector3[0] * vector1[1] * vector2[2]) + (vector2[0] * vector1[2] * vector3[1])
    minus_part = -(vector1[2] * vector2[1] * vector3[0]) - (vector1[0] * vector3[1] * vector2[2]) - (vector3[2] * vector2[0] * vector1[1])
    return plus_part + minus_part 

for (A,B,C,D) in itertools.combinations(points, 4):
    vector_AB = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]
    vector_AC = [C[0]-A[0],C[1]-A[1],C[2]-A[2]]
    vector_AD = [D[0]-A[0],D[1]-A[1],D[2]-A[2]]
    if determinant_3x3_(vector_AB,vector_AC,vector_AD) == 0:
        k = 1 #лічилькик
        print(f"points:{A},{B},{C},{D} утворюють  плоский прямокутник у просторі!")
if k == 0:
    print("Жодна з даних точок не утворює плоский прямокутник у просторі!")