import math
from typing import Literal

class Triangle():
    __instance_list = []
    counter_birth = 0
    counter_del = 0


    def __new__(cls, *args, **kwargs):
        our_object = super().__new__(cls)
        cls.__instance_list.append(our_object)

        return our_object

    def __init__(self, first_side=None, second_side=None, third_side=None):
        """
        first_side also can be child of our class, when it heppens, we create a copy of our object
        """
        if isinstance(first_side, Triangle):
            self.first_side = first_side.first_side
            self.second_side = first_side.second_side
            self.third_side = first_side.third_side
        else:
            if first_side and second_side and third_side:
                self.first_side = first_side
                self.second_side = second_side
                self.third_side = third_side
            elif first_side and second_side:
                self.first_side = first_side
                self.second_side = second_side
                self.third_side = math.sqrt(first_side ** 2 + second_side ** 2)
        
        if Triangle.isvalid(self.first_side, self.second_side, self.third_side):
            Triangle.counter_birth += 1
            print(f"The {self.type()} you created has sides: {self.first_side}, {self.second_side}, {self.third_side}")
        else:
            Triangle.__instance_list.remove(self)
            print("Triangle with given sides cannot be created")

    def perimeter_calc(self) -> float:
        #round better
        return round(self.first_side + self.second_side + self.third_side, 3)
    
    def square_calc(self) -> float:
        hf_per = self.perimeter_calc() / 2
        val = hf_per * (hf_per - self.first_side) * (hf_per - self.second_side) * (hf_per - self.third_side)
        if val < 0: val = 0
        square = math.sqrt(val)
        return round(square,3)
    
    def angle1_calc(self):
        cos_a_val = (self.first_side ** 2 + self.second_side ** 2 - self.third_side ** 2) / (2 * self.first_side * self.second_side)
        cos_a_val = max(-1,min(1,cos_a_val))
        a = math.degrees(math.acos(cos_a_val))
        return round(a,3)

    def angle2_calc(self):
        #
        cos_b_val = (self.second_side ** 2 + self.third_side ** 2 - self.first_side ** 2) / (2 * self.second_side * self.third_side)
        cos_b_val = max(-1,min(1,cos_b_val))
        b = math.degrees(math.acos(cos_b_val))
        return round(b,3)

    def angle3_calc(self):
        cos_c_val = (self.first_side ** 2 + self.third_side ** 2 - self.second_side ** 2) / (2 * self.first_side * self.third_side)
        cos_c_val = max(-1,min(1,cos_c_val))
        c = math.degrees(math.acos(cos_c_val))
        return round(c,3)
    
    @staticmethod
    def isvalid(a, b, c):
        return a + b > c and a + c > b and b + c > a
    
    @staticmethod
    def print_birth_del():
        return f"Number of created: {Triangle.counter_birth}, number of deleted: {Triangle.counter_del}"
    
    def type(self):
        a = self.angle1_calc()
        b = self.angle2_calc()
        c = self.angle3_calc()
        angles = (a,b,c)

        if any(math.isclose(angle,90,abs_tol=1e-3) for angle in angles):
            return "right triangle"
        elif any(angle < 90 for angle in angles):
            return "acute triangle"
        
        return "obtuse triangle"
    
    def print_info(self):
        print(f"""Your {self.type()} has a first side: {self.first_side}, second side: {self.second_side}, third side: {self.third_side}.
              First angle: {self.angle1_calc()}, second angle: {self.angle2_calc()}, thrid angle: {self.angle3_calc()}.
              Perimeter: {self.perimeter_calc()}, square: {self.square_calc()}""")
    
    @staticmethod
    def print_entire_lst(method: Literal["by date","by square","by perimeter"], parameter: Literal["by decline", "by growth"]):

        lst = Triangle.__instance_list
        match parameter.strip():
            case "by decline":
                parameter = True
            case "by growth":
                parameter = False
            case _:
                print("Check your input and try again")
        
        match method.strip():
            #можна легше
            case "by date":
                for elem in sorted(lst, key= lambda elem: lst.index(elem), reverse=parameter):
                    elem.print_info()
            case "by square":
                for elem in sorted(lst, key=lambda elem: elem.square_calc(), reverse=parameter):
                    elem.print_info()
            case "by perimeter":
                for elem in sorted(lst, key=lambda elem: elem.perimeter_calc(), reverse=parameter):
                    elem.print_info()
            case _:
                print("Check your input and try again")
            
    @classmethod
    def _remove_triangle(cls, triangle):
        if triangle in cls.__instance_list:
            cls.__instance_list.remove(triangle)

    def __del__(self):
        Triangle.counter_del += 1
        Triangle._remove_triangle(self)
        if self in Triangle.__instance_list:
            Triangle.__instance_list.remove(self)
        print(f"""It`s a shame we have to say goodbye to our {self.type()},
              who has sides {self.first_side}, {self.second_side}, {self.third_side} and it`s square is {self.square_calc()}""")
        
def main():

    A = Triangle(3,4)
    B = Triangle(7,8,10)
    C = Triangle(5,12,15)
    D = Triangle(6,6,4)
    E = Triangle(10,10,19)
    H = Triangle(A)

    F = Triangle(1,2,10)

    Triangle.print_entire_lst("by date", "by decline")
    Triangle.print_birth_del()
    del A
    Triangle.print_birth_del()
    Triangle.print_birth_del()

if __name__ == "__main__":
    main()