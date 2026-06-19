#lab3_task2 (advanced прості числа)

while True:
    N = int(input('Input natural number: '))
    
    for num in range(1, N+1):
        prime0 = True
        prime1 = True
        i = 2
        
        if num == 1:
            print(num, end= ",")
        elif num == 2:
            print('', num , end ="" )
        else:
            while i <= num-1:
                if num % i == 0:
                    prime0 = False
                    break
                else:
                    i += 1
                    
            if prime1 and prime0:
                i = 2
                summa = 0
                copy_num = num
                
                while copy_num >= 1:
                    digit = copy_num % 10
                    summa += digit
                    copy_num = copy_num // 10
                
                while i <= summa-1:
                    if summa % i == 0:
                        prime1 = False
                        break
                    else:
                        i += 1        
            
            if num == N:
                print(".")

            if prime0 and prime1:
                print(',' , num, end= "")
                    
