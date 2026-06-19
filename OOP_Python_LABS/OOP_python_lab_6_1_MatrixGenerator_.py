from typing import Literal
from random import choice, randint
from OOP_python_lab_5_1__Matrix__asserT__ import Matrix
from accessify import private

class MatrixGenerator():
    def __init__(self, size_tuple: tuple[int], Type: Literal["zeros", "values", "random", "indentity", "inverse", "upper_triangle", "diag"], value: int | list = None):
        self._max_rows, self._max_cols = size_tuple
        self._value = value
        self._gen = self.match_type(Type)
    
    @private
    def match_type(self, Type):
        return {"zeros" : self.gen_zeros,
                "values": self.gen_values,
                "random": self.gen_random,
                "indentity": self.gen_indentity,
                "inverse": self.gen_inverse,
                "upper_triangle" : self.upper_triangle,
                "diag": self.gen_diag}[Type]()
    
    @private
    def get_next_value(self):
        i = 0
        lenght = len(self._value)
        while True:
            yield self._value[i % lenght]
            i += 1
               
    def gen_zeros(self):
        for row in range(self._max_rows):
            for col in range(self._max_cols): # Можна робити через if self_k < self._max_rows ..., але чи треба ? Ну або через itertools.product...
                yield row, col, 0
        return
    
    def gen_values(self):
        for row in range(self._max_rows):
            for col in range(self._max_cols):
                yield row, col, self._value
        return
    
    def gen_random(self):
        if not self._value:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    yield row, col, randint(0, 1)
        elif isinstance(self._value, list):
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    yield row, col, choice(self._value)
        else:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    yield row, col, randint(0, self._value)
        return

    def gen_indentity(self):
        for row in range(self._max_rows):
            for col in range(self._max_cols): 
                if row == col: yield row, col, 1
                else: yield row, col, 0
        return
    
    def gen_inverse(self):
        for row in range(self._max_rows):
            for col in range(self._max_cols): 
                if row + col == self._max_cols - 1: yield row, col, 1
                else: yield row, col, 0
        return
    
    def upper_triangle(self):
        if not self._value:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row < col: yield row, col, 0
                    else: yield row, col, randint(0, 1)
        elif isinstance(self._value, list):
            gen = self.get_next_value()
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row < col: yield row, col, 0
                    else: yield row, col, next(gen)
        else:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row < col: yield row, col, 0
                    else: yield row, col, self._value
        return
    
    def gen_diag(self):
        if not self._value:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row != col: yield row, col, 0
                    else: yield row, col, randint(0, 1)
        elif isinstance(self._value, list):
            gen = self.get_next_value()
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row != col: yield row, col, 0
                    else: yield row, col, next(gen)
        else:
            for row in range(self._max_rows):
                for col in range(self._max_cols):
                    if row != col: yield row, col, 0
                    else: yield row, col, self._value
        return

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._gen)

if __name__ == "__main__":
    gen_matrix_A = MatrixGenerator((3,4), "upper_triangle", 3)
    final_lst = [[None for i in range(4)] for j in range(3)]
    for row, col, value in gen_matrix_A:
        final_lst[row][col] = value
    matrix_A = Matrix(final_lst)
    print(matrix_A)