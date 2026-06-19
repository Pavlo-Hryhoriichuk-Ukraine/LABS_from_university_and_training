#lab7_task3 (матриці)

#перша матриця
matrix_1 = []
matrix_1_number_of_columbs = int(input("Input number of columbs: ")) #стовпці
matrix_1_number_of_rows = int(input("Input number of rows: ")) #рядки
for current_row in range(matrix_1_number_of_rows):
    row = list(map(int, input(f"Input elements of {current_row+1} row: ").split()))
    matrix_1.append(row)

#друга матриця
matrix_2 = []
matrix_2_number_of_columbs = int(input("Input number of columbs: ")) #стовпці
matrix_2_number_of_rows = int(input("Input number of rows: ")) #рядки
for current_row in range(matrix_2_number_of_rows):
    row_ = list(map(int, input(f"Input elements of {current_row+1} row: ").split()))
    matrix_2.append(row_)

print(matrix_1)
print(matrix_2)
#1- множення матриць


if matrix_1_number_of_columbs == matrix_2_number_of_rows:
    j = -1 #для переключання між стовпцями в matrix2
    product_matrix = []
    q = 0
    for iterations in range(1,len(matrix_2[0])+1):
        j += 1
        for row1 in matrix_1:
            i = 0 #для переключання між цифрами в row1
            summa = 0
            for row2 in matrix_2:
              summa += row1[i] * row2[j]
              i += 1
            if j >= 1:
                product_matrix[q].append(summa)
                q += 1
            else:
               product_matrix.append([summa])
    print(product_matrix)
else:
    print("These matrices cannot be multimpied")

#сідлові точки матриці
index_list = []
i = -1
for row in product_matrix:
    i += 1 #рядки
    j = -1 #стовпці
    for element in row:
        j += 1
        if element == min(row):
            max = True
            for row1 in product_matrix:
                if row1[j] > element:
                    max = False
                    break
            if max:
                index_list.append((i+1,j+1))
print(index_list)

#особливі елементи матриці
unique_elements = []
for row in product_matrix:
    j = -1
    for element in row:
        j += 1
        summa = 0
        i = 0
        for row1 in product_matrix:
            if i == 0:
                continue
            else:
                summa += row1[j]
            i += 1
        if element > summa:
            for row in product_matrix:
                for element in row:
                    true = True
                    for el in row:
                        if row.index(element) > row.index(el):
                            if element > el:
                                pass
                            else:
                                true = False
                        if row.index(element) < row.index(el):
                            if element < el:
                                pass
                            else:
                                true = False
                    if true:
                        unique_elements.append(element)
print(unique_elements)