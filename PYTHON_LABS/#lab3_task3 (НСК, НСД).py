#lab3_task3 (НСК, НСД)

while True:
    number_1 = int(input("Input first natural number: "))
    number_2 = int(input('Input second natural number: '))

    if number_1 and number_2 > 0:
        
        if number_1 == number_2:
            GCD = number_1 
        
        else:
            a = number_1
            b = number_2

            while b > 0:
                r = a % b
                a = b
                b = r
            GCD = a
        LCM = (number_1 * number_2) // GCD
        
        print(f"GCD({number_1}, {number_2}) = {GCD} ; LCM({number_1}, {number_2}) = {LCM}.")
    else:
        print("You inputted not natural number, please, try again")