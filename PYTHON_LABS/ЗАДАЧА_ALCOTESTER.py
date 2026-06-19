while True:
    def  plus_numbers(a,b):
        print(a + b)
    
    a = input('Введіть перше число або СТОП: ')
    b = input('Введіть друге число або СТОП: ')
    
    if a.isdigit and b.isdigit:
        plus_numbers(a,b)
    
    elif a.upper or b.upper == 'СТОП' :
            print('Дякуємо за використання нашого калькулятора!')
            break
    else:
         print('Спробуйте ввести дані за правилами.')
         continue