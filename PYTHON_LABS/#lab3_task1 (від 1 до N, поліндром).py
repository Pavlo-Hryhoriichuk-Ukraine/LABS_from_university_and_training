#lab3_task1 (від 1 до N, поліндром)

N = int(input("Input natural number: "))
list0 = []
reversed_number = ''

for i in range (1, N+1):
    reversed_number = ''
    i1 = i ** 2
    i2 = i ** 2
    while i1 >= 1:
        digit = i1 % 10
        reversed_number += f"{digit}"
        i1 = i1 // 10
    reversed_number = int(reversed_number)

    if i2 == reversed_number:
        list0.append(i)
        
    else:
        continue
print(list0)
for value in list0:
    maxv = len(list0)
    if  list0.index(value) != maxv - 1:
        print(value, end= ", ")
    else:
        print(value, end= ".")