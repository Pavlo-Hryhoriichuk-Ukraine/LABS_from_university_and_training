#КАЛЬКУЛЯТОР

while True:
    try:
        numbers = list(map(int, input('Введіть два числа через кому (в межах від 0 до 100), які потрібно додати: ').split(',')))
    except ValueError:
        print('Ви ввели дані не за правилами, спробуйте щераз')
        continue

    a = numbers[0]
    b = numbers[1]

    if 0<= a <=100 and 0<= b <=100:
        print(a+b)
    else:
        print('Ви ввели дані не за правилами, спробуйте щераз')