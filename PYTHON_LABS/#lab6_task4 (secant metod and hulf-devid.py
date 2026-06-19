#lab6_task4 (secant metod and hulf-deviding menod of solving algebric equations)

while True:
    e1 = input("Input your e-accuracy: ")
    e = float(e1)
    def function(x):
        value = (-2 * (x**3)) + (4 * (x**2)) -x + 1
        return value 
    
    #Secant_metod
    u0 = 0
    b = 4
    u1 = u0 - (function(u0)* ((b - u0) / (function(b) - function(u0))))
    while abs(u1 - u0) > e:
        u0 = u1
        u1 = u1 - (function(u1) * (b - u1) / (function(b) - function(u1)))

    #Bisection method
    a = 0
    b = 2
    while abs(a - b) > e:
        middle = (a + b) / 2
        f_mid = function(middle)
        if f_mid == 0:
            solution = f_mid
            break
        
        if function(a) * f_mid < 0:
            b = middle
        else:
            a = middle
    solution = (a + b) / 2
    print(f"""Your approximate roots with e-accuracy: '{e1}' is:
          BISECTION METHOD: {solution}
          SECANT METOD: {u1}""")
    print(f"SECANT: {function(u1)}, BISECTION: {function(solution)}")