#lab16_1 (module for vectors)
code = 
def input_vector() -> tuple[float] | TypeError:
    try:
        coordinates = tuple(map(float,input("Input POSITIVE coordinates of vector USING COMMA: ").split(",")))
        assert all(elem > 0 for elem in coordinates)

    except AssertionError:
        raise TypeError("You inputted not possitive coordinates")
    except:
        raise TypeError("Check your input and try again")
    
    if len(coordinates) == 2 or len(coordinates) == 3:
        print(coordinates)
        return coordinates
    raise TypeError("Input right number of coordinates")

def add_two_vectors(vector1: tuple[float], vector2: tuple[float]) -> tuple[float] | TypeError:
    lenght_1 = len(vector1)
    lenght_2 = len(vector2)
    try:
        assert lenght_1 == lenght_2
        new_vector = [vector1[i] + vector2[i] for i in range(lenght_1)]
        new_vector = tuple(new_vector)
        
        print(new_vector)
        return new_vector
    
    except AssertionError:
        raise TypeError("Make sure that you inputted vectors from the same space")

def diff_two_vectors(vector1: tuple[float], vector2: tuple[float]) -> tuple[float] | TypeError:
    lenght_1 = len(vector1)
    lenght_2 = len(vector2)
    try:
        assert lenght_1 == lenght_2
        new_vector = [vector1[i] - vector2[i] for i in range(lenght_1)]
        new_vector = tuple(new_vector)
        
        print(new_vector)
        return new_vector
    
    except AssertionError:
        raise TypeError("Make sure that you inputted vectors from the same space")

def mult_vector_on_scalar(vector: tuple[float], scalar: int|float) -> tuple[float] | TypeError:
    try:
        new_vector = tuple(list(map((lambda elem: elem * scalar), vector)))
        print(new_vector)
        return new_vector
    except:
        raise TypeError("Check that you have inputted")
    
def scalar_product(vector1: tuple[float], vector2: tuple[float]) -> float | str:
    try:
        return sum(map(lambda x: x[0]*x[1],zip(vector1, vector2)))
    except:
        raise TypeError("Check your input and try again")

def vector_product(vector1: tuple[float], vector2: tuple[float]) -> tuple[float] | TypeError:
    try:
        x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
        y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
        z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
        new_vector = x,y,z

        print(new_vector)
        return new_vector
    except IndexError:
        raise TypeError("You have inputted vectors from 2D space")
    except:
        return TypeError("Check your input and try again")

def draw_vector(vector: tuple[float]) -> None | TypeError:
    lenght = len(vector)
    match lenght:
        case 2:
            from matplotlib import pyplot as plt

            x, y = vector
            plt.quiver(0,0,x,y, angles = "xy", scale_units = "xy", scale= 1, color = 'red', label = "Вектор А")

            plt.xlim(-1, x+3)
            plt.ylim(-1,y+3)
            plt.axhline(0,color = "black", lw = 1)
            plt.axvline(0, color="black", lw = 1)
            plt.grid()
            plt.legend()
            plt.show()
        
        case 3:
            from matplotlib import pyplot as plt

            x, y, z = [0], [0], [0]
            u, v, w = vector

            fig = plt.figure(figsize=(u+3,v+3))
            ax = fig.add_subplot(111, projection="3d")

            ax.quiver(x, y, z, [u], [v], [w], color="blue", arrow_length_ratio=0.1)

            ax.set_xlim([0, u+3])
            ax.set_ylim([0,v+3])
            ax.set_zlim([0,w+3])

            ax.set_xlabel("Вісь Х")
            ax.set_ylabel('Вісь Y')
            ax.set_zlabel('Вісь Z')

            plt.show()
        
        case _:
            raise TypeError("Check your input and try again")
            """

#with open("vector.py", "w", encoding="utf-8") as file:
#     file.write(code)

import vector

vector_1 = vector.input_vector()
vector_2 = vector.input_vector()

vector.add_two_vectors(vector_1,vector_2)
vector.diff_two_vectors(vector_1, vector_2)
vector.mult_vector_on_scalar(vector_1,scalar=3)
vector.mult_vector_on_scalar(vector_2, scalar=4)
vector.vector_product(vector_1,vector_2)
vector.vector_product(vector_2,vector_1)
vector.scalar_product(vector_1, vector_2)
vector.scalar_product(vector_2,vector_1)
vector.draw_vector(vector_1)
vector.draw_vector(vector_2)