#lab4_task2 (ряд Тейлора із точністю е)

while True:
    accuracy = input("Input eps accuracy: ")
    e = float(accuracy)
    engle = float(input("Input sin argument :"))
    pi = 3.14
    two_pi = 2 * pi
    x = engle * pi / 180
    if x > two_pi:
        q = x // two_pi
        x = x / (q * two_pi)
    n = 1
    S = x
    a = x
    f = x ** 2
    j = 2
    i = 3 #див. у зошиті
    factorial = 1
    
    while abs(a) >= e:
        
        if n % 2 == 0:
            a = (f * a) / (j * i)
            j += 2
            i += 3
        else:
             a = ((-1) * f * a) / (factorial * j * i)
             j += 2
             i += 3
        S += a
        n +=1
    S = round(S, accuracy.count('0'))
    print(f"sin({engle}) = {S} with accuracy {accuracy}; N = {n}")