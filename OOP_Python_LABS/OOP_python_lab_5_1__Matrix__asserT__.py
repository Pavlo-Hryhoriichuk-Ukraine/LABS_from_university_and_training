from typing import Any

class Matrix():
    def __init__(self, user_input):
        self.rows = [[]]
        if not self._verify_input_type(user_input):
            self._message = "Matrix was not initilized: type of input data is not list or tuple."
            return
        if not self._verify_elements_type(user_input):
            self._message = "Matrix was not initilized: elements are not int or float."
            return
        if not self._verify_rectangular_structure(user_input):
            self._message = "Matrix was not initialized because input data has no rectangular structure."
            return
        
        self.rows = user_input
        self._message = 'Matrix was successfully initialized'


    @property
    def nrows(self) -> int:
        return len(self.rows)
    
    @property
    def ncols(self) -> int:
        return len(self.rows[0])
    
    @staticmethod
    def _verify_input_type(user_input: Any) -> bool:
        return isinstance(user_input, list) and all(isinstance(elem, list) for elem in user_input)
    
    @staticmethod
    def _verify_elements_type(user_lst: list[list[int | float]]) -> bool: # Як зробити експресивніше і краще ?
        return all(isinstance(elem, (int, float)) for inner_lst in user_lst for elem in inner_lst)
    
    @staticmethod
    def _verify_rectangular_structure(user_lst: list[list[int | float]]) -> bool:
        standart = len(user_lst[0])
        return all(len(inner_lst) == standart for inner_lst in user_lst)
    
    def _verify_all(self, user_input: Any) -> bool:
        return self._verify_input_type(user_input) and self._verify_elements_type(user_input) and self._verify_rectangular_structure(user_input)
    
    
    def status(self) -> str:
        return self._message
    
    def __str__(self):
        string = ''
        for row in self.rows:
            for i, elem in enumerate(row):
                is_last = i + 1 == len(row)
                width = 7 if is_last else 8
                string += f"{elem:<{width}}"
            string += '\n'
        return string.strip('\n')
        
    
    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.ncols != other.ncols or self.nrows != other.nrows:
                return 'One or two dimensions of matrixes do not coincide'
            
            new_matrix = []
            for i in range(self.nrows):
                row = list(map(lambda elem: elem[0] + elem[1], zip(self.rows[i], other.rows[i]))) # можна краще ?
                new_matrix.append(row)

            return Matrix(new_matrix)
        
        if isinstance(other, (int, float)):
            return Matrix(list([elem + other for elem in inner_lst] for inner_lst in self.rows))
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __iadd__(self, other):
        self.rows = [[elem + other for elem in inner_lst] for inner_lst in self.rows]
        return self
    
    def __neg__(self):
        return Matrix([[-elem for elem in inner_lst] for inner_lst in self.rows])
    
    def __sub__(self, other):
        if self.ncols != other.ncols or self.nrows != other.nrows:
            return 'One or two dimensions of matrixes do not coincide'
        
        new_matrix = []
        for i in range(self.nrows):
            row = list(map(lambda elem: elem[0] - elem[1], zip(self.rows[i], other.rows[i]))) # можна краще ?
            new_matrix.append(row)
        return Matrix(new_matrix)
    
    def __mul__(self, other):
        if self.ncols != other.nrows:
            return "These matrixes can't be multiplied it this order"
    
        result = []
        for i in range(self.nrows):
            row = []
            for j in range(other.ncols):
                elem = sum(self.rows[i][k] * other.rows[k][j] for k in range(self.ncols))
                row.append(elem)
            result.append(row)
    
        return Matrix(result)
    
    
    def __eq__(self, other):
        return self.rows == other.rows
    
    def __len__(self):
        return self.ncols * self.nrows
    

    def __getitem__(self, key):
        if isinstance(key, tuple):  # m12[1, 0]
            row, col = key
            return self.rows[row][col]
        return self.rows[key]
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            row, col = key
            self.rows[row][col] = value
            return
        
        value = list(value)
        if len(value) != self.ncols or not self._verify_elements_type([value]):
            return
        
        self.rows[key] = value

    def __delitem__(self, key):
        if isinstance(key, tuple):  # del m12[1, 0]
            row, col = key
            del self.rows[row][col]
        else:
            del self.rows[key]

    
def test_matrix():
    m1 = Matrix([[0,2],[-4,1],[-9,5]])
    assert m1.status() == 'Matrix was successfully initialized'
    assert m1._message == 'Matrix was successfully initialized'
    assert m1.rows == [[0,2],[-4,1],[-9,5]]
    assert m1.nrows == 3 
    assert m1.ncols == 2
   
    m1.rows = [[1,2],[4,5],[7,1]]
    assert m1.rows == [[1,2],[4,5],[7,1]]
    assert str(m1) == '1       2      \n4       5      \n7       1      '
    m2 = Matrix([[1,2],[4,5,2],[7,1]])
    assert m2.status() == "Matrix was not initialized because input data has no rectangular structure."
    assert m2._message == "Matrix was not initialized because input data has no rectangular structure."
    assert m2.rows == [[]]

    m3 = Matrix("[1,2,3],[2,3,4]")
    assert m3.status() == "Matrix was not initilized: type of input data is not list or tuple."
    assert Matrix._verify_input_type("[1,2,3],[2,3,4]") == False
    assert m3._verify_input_type("[1,2,3],[2,3,4]") == False

    m4 = Matrix([[1,"a"],[4,5],[7,1]])
    assert m4.status() == "Matrix was not initilized: elements are not int or float."
    assert m4.rows == [[]]
    assert Matrix._verify_elements_type([[1,"a"],[4,5],[7,1]]) == False
    assert m4._verify_elements_type([[1,"a"],[4,5],[7,1]]) == False

    m5 = Matrix([[1,2,3,5],[2,3,4],[1,2,3]])
    assert m5.status() == "Matrix was not initialized because input data has no rectangular structure."
    assert m5.rows == [[]]
    assert Matrix._verify_rectangular_structure([[1,2,3,5],[2,3,4],[1,2,3]]) == False
    assert m5._verify_rectangular_structure([[1,2,3,5],[2,3,4],[1,2,3]]) == False
    assert m5._verify_elements_type([[1,2,3,5],[2,3,4],[1,2,3]]) == True
    assert m5._verify_input_type([[1,2,3,5],[2,3,4],[1,2,3]]) == True
    assert m5._verify_all([[1,2,3,5],[2,3,4],[1,2,3]]) == False    

    try:
        Matrix._verify_all([[1,2,3,5],[2,3,4],[1,2,3]]) # this is cubic, should fail!
    except TypeError as err:
        message = err.args[0]
    assert message == "Matrix._verify_all() missing 1 required positional argument: \'user_input\'" #ТУТ Я ПОМІНЯВ ВІДПОВІДНО ДО МОГО КОДУ (НАЗВУ ЗМІННОЇ)

    m6 = Matrix([[4,-1],[0,2],[3,-1]])
    assert m6.status()=='Matrix was successfully initialized'

    a = bool()
    print(a)
    m7 = m1 + m6
    assert str(m7) == '5       1      \n4       7      \n10      0      '
    assert isinstance(m7, Matrix)

    assert str(-m1) == '-1      -2     \n-4      -5     \n-7      -1     '
    assert isinstance(-m1, Matrix)

    m8 = m1 - m6
    assert isinstance(m8, Matrix)
    assert str(m8) == '-3      3      \n4       3      \n4       2      '

    m9 = Matrix([[4,-1,4],[0,2,2]])
    assert m9.status() == 'Matrix was successfully initialized'
    assert m1+m9 == 'One or two dimensions of matrixes do not coincide'

    m10 = m1*m9
    assert isinstance(m10, Matrix)
    assert str(m10) == '4       3       8      \n16      6       26     \n28      -5      30     '

    m11 = Matrix([[4,-1],[0,2]])
    m11.status() == 'Matrix was successfully initialized'
    assert m11*m1 == 'These matrixes can\'t be multiplied it this order'

    assert not (m11 == m1)
    m12 = Matrix([[1,2],[4,5],[7,1]])
    assert m12.status() == 'Matrix was successfully initialized'
    assert (m12 == m1)

    m13 = m12 + 1.51
    assert m13.rows == [[2.51,3.51],[5.51,6.51],[8.51,2.51]]
    
    m14 = 1.51 + m12
    assert m14.rows == [[2.51,3.51],[5.51,6.51],[8.51,2.51]]
    
    id_prev = id(m12)
    m12 += 1.51
    assert m12.rows == [[2.51,3.51],[5.51,6.51],[8.51,2.51]]
    assert id(m12) == id_prev
    assert len(m12) == 6
    
    assert m12[1] == [5.51,6.51]
    assert m12[1][0] == 5.51
    assert m12[1, 0] == 5.51 
    
    m12[1][0] = 100
    assert m12[1][0] == 100
    m12[1] = [0, 0]
    assert m12.rows[1] == [0,0]
    m12[1] = [1,2,3]
    assert m12.rows[1] == [0, 0]
    m12[1] = [2]
    assert m12.rows[1] == [0, 0]
    
    del m12[1]
    assert m12.rows == [[2.51,3.51],[8.51,2.51]]
    print("DONE")

if __name__ == "__main__":
    test_matrix()