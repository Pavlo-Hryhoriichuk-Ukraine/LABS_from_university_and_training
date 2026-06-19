#lab4_task4 (k-та цифра послідовності усіх квадратів натуральних чисел)

while True:
    k = int(input('Input your k-number: '))

    square = 1
    sequence = [1]
    add = 3

    for i in range (2,k):
        square += add
        add += 2
        copy_square1 = square
        reversed_number = " "
        
        while copy_square1 >= 1:
            digit1 = copy_square1 % 10
            reversed_number += f'{digit1}'
            copy_square1 = copy_square1 // 10
            
        reversed_number = int(reversed_number)

        while reversed_number >= 1:
            digit = reversed_number % 10
            sequence.append(digit)
            reversed_number = reversed_number // 10
    
    if k >=5 :
        print(sequence[k-1])
    elif k == 1:
        print(1)
    elif k == 2:
        print(4)
    elif k == 3:
        print(9)
    elif k == 4:
        print(1)