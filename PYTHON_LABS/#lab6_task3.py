#lab6_task3 (рекурентні старших порядків номер 2)

while True:
    n = int(input("Input n-number: "))
    a1 = 1
    a2 = 1
    b1 = 1
    b2 = 1
    multiplier = 2
    q = 1
    S = 0
    S += q
    multiplier *= 2
    q = multiplier / (a2 + b2)
    S += q

    for k in range (3, n+1):
        b3 = b2 + a2
        a3 = (a2 / k) + (a1 * b3)
        multiplier *= 2
        q = multiplier / (a3 + b3)
        S += q
        a1 = a2
        a2 = a3
        b1 = b2
        b2 = b3
    print(S)