#lab2_task2 (я думав, вам +1 рік...)

while True:
    age1 = int(input("Input your age: "))

    if age1 < 0:
        print("Ви ще не народилися")
    elif age1 > 140:
        print("Стільки не живуть")
    else:
        age2 = age1 + 1
        if age2 == 10 or 11 or 12 or 13 or 14 or 111 or 112 or 113 or 114:
            ending = "років"
        elif age2 % 10 == 1:
            ending = "рік"
        elif age2 % 10 == 2 or 3 or 4:
            ending = "роки"
        elif age2 % 10 == 0 or 5 or 6 or 7 or 8 or 9:
            ending = "років"

    print(f"Я думав, вам {age2} {ending}")