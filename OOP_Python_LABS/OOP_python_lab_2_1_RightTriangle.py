from accessify import protected, private
import math

class RightTriangle():
    __N = 10
    __lst_of_unique_triangles = []
    __lst_of_all_triangles = [] 
    __default_color = "red"

    def __new__(cls, a_side, b_side, c_side, color=None, *args, **kwargs):
        print(f"Recieved request for creating right triangle with sides {a_side, b_side, c_side}")

        if cls.__N <= len(cls.__lst_of_all_triangles):
            raise PermissionError(f"We are limited by {cls.__N} samples of right triangles")
        
        if RightTriangle.valid_triangle(a_side, b_side, c_side):
            new_triangle = super().__new__(cls)
            print(f"right triangle with sides {a_side, b_side, c_side} was created")
            RightTriangle.__lst_of_all_triangles.append(new_triangle)
            return new_triangle

        print(f"right triangle with sides {a_side, b_side, c_side} can't be created")
        

    def __init__(self, a_side, b_side, c_side, color = None):
        self._a_side = a_side
        self._b_side = b_side
        self._c_side = c_side
        self._sin_angleA = a_side / c_side
        self._sin_angleB = b_side / c_side
        self._color = color if color else RightTriangle.__default_color
        self.add_to_unique_lst(self)
    
    def __setattr__(self, name, value):
        allowed_fields_names = {"_a_side", "_b_side", "_c_side", 
        "_sin_angleA", "_sin_angleB", "_color"}
    
        if name in allowed_fields_names:
            return object.__setattr__(self, name, value)
    
        if isinstance(getattr(type(self), name, None), property):
            return
    
        raise AttributeError(f"Cannot add new attribute '{name}'")
    
    def __getattr__(self, name):
        return
    
    def __str__(self):
        return f"Right Triangle has sides {self._a_side}, {self._b_side}, {self._c_side} and squre {self.__calculate_square()}"
    
    def __delattr__(self, name):
        if name == "_color":
            object.__setattr__(self, "_color", RightTriangle.__default_color)
        object.__delattr__(self, name)

    @staticmethod
    def valid_triangle(a_side, b_side, c_side):
        return True if math.isclose((a_side ** 2 + b_side ** 2), c_side ** 2) else False
    
    @protected
    @staticmethod
    def calc_median(side: int |float, side2: int | float, side3: int | float) -> float:
        return 0.5 * (2*side2**2 + 2*side3**2 - side**2) ** 0.5
    
    @protected
    @staticmethod
    def calc_bisector(side: int |float, side2: int | float, side3: int | float) -> float:
        return (side2 * side3 * ((side2 + side3)**2 - side**2)) ** 0.5 / (side2 + side3)
    
    
    @protected
    @classmethod
    def add_to_unique_lst(cls, instance):
        instance_tuple = instance._a_side, instance._b_side, instance._c_side
        if not any((elem._a_side, elem._b_side, elem._c_side) == instance_tuple for elem in cls.__lst_of_unique_triangles):
            cls.__lst_of_unique_triangles.append(instance)
    
    @protected
    @classmethod
    def remove_from_unique_lst(cls, instance):
        instance_tuple = instance._a_side, instance._b_side, instance._c_side
        if any((elem._a_side, elem._b_side, elem._c_side) == instance_tuple for elem in cls.__lst_of_unique_triangles):
            cls.__lst_of_unique_triangles.remove(instance)

    @protected
    @classmethod
    def change_N(cls, value):
        cls.__N = value
    

    @classmethod
    def calc_number_of_unique_class_objects(cls):
        return len(cls.__lst_of_unique_triangles)
    
    @classmethod
    def apply_color_to_all(cls, new_color):
        for instance in cls.__lst_of_all_triangles:
            instance._color = new_color

    @classmethod
    def print_all_unique_triangles_sorted_by_square(cls) -> None:
        sorted_lst = sorted(cls.__lst_of_unique_triangles, key=lambda elem: elem.__calculate_square())
        sorted_lst = [f"RT(a = {instance._a_side:.3f}, b = {instance._b_side:.3f}, c = {instance._c_side:.3f})" for instance in sorted_lst]
        print(sorted_lst)
    
    @classmethod
    def draw_all_unique_triangles(cls):
        import turtle
        import random

        screen = turtle.Screen()
        screen.title("Right triangles")
        screen.setup(width=800, height=600)
        screen.bgcolor("white")
        screen.tracer(0)

        t = turtle.Turtle()
        t.speed(0)
        t.width(2)
        t.hideturtle()

        for instance in cls.__lst_of_unique_triangles:
            x_base_point = random.randint(-300, 300)
            y_base_point = random.randint(-200, 200)

            y1 = y_base_point + (instance._c_side / 2)
            y2 = y_base_point - (instance._c_side / 2)

            x3 = x_base_point - instance.altitude_dropped_to_the_hypotenuse

            t.pencolor(instance._color)
            t.penup()
            t.goto(x_base_point, y1)
            t.pendown()
            t.fillcolor(instance._color)
            t.begin_fill()
            t.goto(x_base_point, y2)
            t.goto(x3, y_base_point)
            t.goto(x_base_point, y1)
            t.end_fill()
            screen.update()
        turtle.done()


    def __calculate_square(self):
        return (self._a_side * self._b_side) / 2


    @property
    def a_side(self):
        return self._a_side
    
    @a_side.setter
    def a_side(self, value):
        self._a_side = value
        self._c_side = value / self._sin_angleA
        self._b_side = self._c_side * self._sin_angleB
        self.remove_from_unique_lst(self)
        self.add_to_unique_lst(self)
    
    @a_side.deleter
    def a_side(self):
        self._a_side = 0

    
    @property
    def b_side(self):
        return self._b_side
    
    
    @b_side.setter
    def b_side(self, value):
        self._b_side = value
        self._c_side = value / self._sin_angleB
        self._a_side = self._c_side * self._sin_angleA
        self.remove_from_unique_lst(self)
        self.add_to_unique_lst(self)
    
    @b_side.deleter
    def b_side(self):
        self._b_side = 0
    
    
    @property
    def c_side(self):
        return self._c_side
    
    
    @c_side.setter
    def c_side(self, value):
        self._c_side = value
        self._b_side = value * self._sin_angleA
        self._a_side = value * self._sin_angleB
        self.remove_from_unique_lst(self)
        self.add_to_unique_lst(self)
    
    @c_side.deleter
    def c_side(self):
        self._c_side = 0

    
    @property
    def median_a(self):
        return self.calc_median(self._a_side, self._b_side, self._c_side)
    
    @property
    def median_b(self):
        return self.calc_median(self._b_side, self._a_side, self._c_side)
    
    @property
    def median_c(self):
        return self.calc_median(self._c_side, self._b_side, self._a_side)
    

    @property
    def bisector_a(self):
        return self.calc_bisector(self._a_side, self._b_side, self._c_side)
    
    @property
    def bisector_b(self):
        return self.calc_bisector(self._b_side, self._a_side, self._c_side)
    
    @property
    def bisector_c(self):
        return self.calc_bisector(self._c_side, self._b_side, self._a_side)
    
    @property
    def altitude_dropped_to_the_hypotenuse(self):
        return round(self.__calculate_square() * 2 / self._c_side, 3)



def main():
    first_rt_triangle = RightTriangle(30, 40, 50, color="green")
    first_rt_triangle = RightTriangle(60, 80, 100, color="yellow")
    print(first_rt_triangle)
    #проблема в перезаписуванні атрибутів. Не знаю, як вирішити. Там проблема в самому модулі accessify.
    print(first_rt_triangle.a_side)
    first_rt_triangle.draw_all_unique_triangles()
    RightTriangle.print_all_unique_triangles_sorted_by_square()

if __name__ == "__main__":
    main()