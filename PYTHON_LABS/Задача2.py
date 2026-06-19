while True:
    def multiply(numbers):
        total = 1
        for number in numbers:
            total *=number
        print(total)


    numbers = input('Введіть числа через кому: ')
    numbers = numbers.split(',')

    numbers2 = []
    for i in numbers:
        numbers2.append(int(i))

    multiply(numbers2)