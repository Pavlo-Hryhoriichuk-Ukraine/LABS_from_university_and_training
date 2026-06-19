#lab6_task1 (вирівняні вдалі числа)
while True:
    print(" \n")
    N = int(input("Input n-number: "))
    lst = []
    lst_remove = []
    k = 1
    for el in range(1,N,2):
        lst.append(el)
    while True:
        number = lst[k]
        if len(lst) < number:
            break
        for el in lst:
            if el == 1:
                continue
            elif (lst.index(el) +1) % number == 0:
                lst_remove.append(el)
        for el in lst_remove:
            lst.remove(el)
        lst_remove.clear()
        k += 1
    
    for el in lst:
        copy_number = N
        counter_N = 0
        while copy_number > 0:
            copy_number = copy_number // 10
            counter_N += 1

        if lst.index(el) % 5 == 0:
            print(" ")
            copy_number = el
            counter_el = 0
            while copy_number > 0:
                copy_number = copy_number // 10
                counter_el += 1
            difference = counter_N - counter_el
            print(difference * " " + str(el),end="  ")
        else:
            copy_number = el
            counter_el = 0
            while copy_number > 0:
                copy_number = copy_number // 10
                counter_el += 1
            difference = counter_N - counter_el
            print(difference * " " + str(el), end="  ")