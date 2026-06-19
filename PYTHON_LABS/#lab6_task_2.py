#lab6_task_2 (рекурентні послідновності)

while True:
    a = int(input("Input a-number: "))
    x0 = x2 = 1
    x1 = 0

    if a == 1:
        print(x1)
    elif a == 0:
        print(x0)
    elif a == 2:
        print(x2)
    else:
        for i in range(3,a+1):
            x3 = 2 * x2 + 3 * x0
            x0 = x1
            x1 = x2
            x2 = x3
        print(x3)