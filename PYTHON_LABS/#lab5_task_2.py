#lab5_task_2 (pi by Gregory and Vallis (e-accuracy))
while True:
    e = float(input('Input your e-accuracy: '))

    #Gregory
    a = 3
    n = 1
    previous = 1
    current = (-1)**n * 1 / a
    summa = previous + current
    while abs (current - previous) >= e:
        previous = current
        n += 1
        a += 2
        if n % 2 == 0:
            current = 1 / a
        else:
            current = -1 / a
        summa += current
    
    #Vallis
    c = 1
    previous2 = d = 2
    current2 = d / c
    k = 2
    pi = current2 * previous2
    
    while abs(previous2 - current2) >= e or k == 2:
        previous2 = current2
        k += 1

        if k % 2 != 0:
            c += 2
            current2 = d / c
        else:
            d += 2
            current2 = d / c
        pi *= current2
    
    print(f"""The Gregory formula gives value {4*summa} with the accuracy {e} by using {n+1} members of series.
          The Vallis formula gives value {pi} with accuracy {e} by using {k} members of series""")

    