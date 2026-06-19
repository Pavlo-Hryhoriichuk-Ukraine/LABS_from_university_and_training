#lab5_task1 (вдале та щасливе число на проміжку)

while True:
    print("\n")
    M = int(input("Input start number: "))
    N = int(input('Input end number: '))
    full_list = []
    n = 1

    for number in range(M, N+1):
        summa = 0
        sum_of_square_digit = 0
        for i in range(1,number):
            if number % i == 0:
                summa += i
        if number != summa:
            continue
        else:
            lucky_number = False
            lst = []
            copy_number = number

            while lst.count(sum_of_square_digit) != 2:
                
                if sum_of_square_digit == 1:
                    lucky_number = True
                    break

                sum_of_square_digit = 0

                while copy_number >= 1:
                    digit = copy_number % 10
                    sum_of_square_digit += digit ** 2
                    copy_number = copy_number // 10
                lst.append(sum_of_square_digit)
                copy_number = sum_of_square_digit
        
        if lucky_number:
            full_list.append(number)
    
    if len(full_list) == 0:
        print("")
        continue
    
    for el in full_list:
        if n % 5 == 0 or el == 28:
            print(el,end="")

        elif n % 4 == 0:
            print(f", {el}", end=";\n")
        else:    
            print(f", {el}", end="")
        n += 1