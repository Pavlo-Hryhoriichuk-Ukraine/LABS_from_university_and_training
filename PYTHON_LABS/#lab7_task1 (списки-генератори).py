#lab7_task1 (списки-генератори)
while True:
    user_input = input("Input n1 n2 m1 m2 numbers: ")
    n1, n2, m1, m2= tuple(map(int,user_input.split()))
    list_1 =[i**2 for i in range(n1,n2+1)]
    list_2 = [i**2 for i in range(m1,m2+1)]
    list_3 = list(tuple(list_1 +list_2))
    min_value = list_3[0]
    max_value = list_3[len(list_3)-1]
    print(f"list 1: {list_1} \nlist 2: {list_2} \nresult list: {list_3} \nmin value: {min_value} \nmax value: {max_value}.")