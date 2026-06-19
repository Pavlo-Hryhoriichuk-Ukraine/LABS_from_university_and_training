#lab4_task1 (рекурентні співвідношення та системи з ними)

while True:
    N = int(input('Input natural value: '))
    x = float(input('Input real value: '))

    #Б
    a = S = -2 * x
    for n in range(2, N+1):
        a = a * ((-2 * x) / n)
        S = S + a
    
    #В
    P = 1 / (1 + x)
    t = 1
    for n in range(2, N+1):
        t = n * t
        P = P * (1/(1 + (x/t)))
    
    #А
    q0 = N^2 + N
    factorial = 1
    for i in range(2, q0+1):
        factorial *= i
    X = (((-1)**N) * (x**(2*N))) / factorial
    
    #ВИСНОВОК
    S = round(S, 3)
    X = round(X, 3)
    P = round(P, 3)
    print(f"x_{n}= {X}; S_{n} = {S}; P_{n} = {P}" )