#lab8_4(solving_quadratic)

import math

def solve_quadratic(text: str):
    '''
    Function for solving "easy-build" quadratic
    '''
    equation = text.split("=")[0].replace(' ','')
    clean_equation = equation.replace("+"," +").replace("-"," -")
    lst = clean_equation.split()
    a,b,c = 0,0,0

    for group in lst:
        if "x**2" in group:
            coeff = group.replace("*x**2",'').replace("x**2",'')
            #audit for empty list
            if not coeff or coeff =='+': a += 1.0
            elif coeff == '-': a += -1.0
            else: a += float(coeff)

        elif "x" in group:
            coeff = group.replace("*x",'').replace('x','')
            if not coeff or coeff == '+': b += 1.0
            elif coeff == '-': b += -1.0
            else: b += float(coeff)
        else:
            c += float(group)

    discriminator = b**2 -(4*a*c)
    if discriminator > 0:
        root_from_discriminator = math.sqrt(discriminator)
        x1 = (-b + root_from_discriminator)/(2*a)
        x2 = (-b - root_from_discriminator)/(2*a)
        print(f"x1 = {x1:.3f}, x2 = {x2:.3f}")
    elif discriminator == 0:
        x = -b/(2*a)
        print(f"x = {x:.3f}")
    else:
        print("Your equation has no solution in the set of real numbers")

def main():
    #text = input("Input your equation: ")
    text = "x**2 - 5x + 6 = 0"
    solve_quadratic(text)

if __name__ == "__main__":
    main()