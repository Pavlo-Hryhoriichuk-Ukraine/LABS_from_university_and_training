#lab5_task3 (системи рекурентних співвнідношень)

while True:
    n = int(input("Input n-number: "))
    if n == 1:
        print(5)
        continue
    a1 = 1
    a2 = 1
    b1 = 0
    b2 = 1
    multiplyer = 25 / 2
    q2 = multiplyer / (a2 + b2)
    q1 = 5
    S = q1 + q2
    if n == 2:
        print(S)
        continue

    for k in range (3,n+1):
        b3 = b2 + a2
        a3 = (a2 /k) + (a1 * b3)
        multiplyer = multiplyer * 5 / k
        q3 = multiplyer / (a3 + b3)
        S += q3
        a2_saver = a2
        a2 = a3
        a1 = a2_saver
        b2 = b3
    print(round(S, 4))



