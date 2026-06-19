#lab5_task4 (визначник порядку n)

while True:
    n = int(input("Input n-number: "))
    if n % 2 == 0:
         D_n = (-1) * (2*n -1)
    else:
          D_n = 2*n -1
    print(D_n)