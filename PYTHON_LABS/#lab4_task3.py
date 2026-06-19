#lab4_task3 (числа Армстронга)

while True:
    n = int(input('Input your "n" : '))

    start = 10 ** (n-1)
    end = 10 ** n

    for number in range(start,end):
        copy_number = number
        summa = 0
        
        while copy_number >= 1:
            digit = copy_number % 10
            summa += digit ** n
            copy_number = copy_number // 10

        if summa == number:
            print(number)
