#lab9_1(у рядку поліном та змінні)
from typing import Callable

def cleaning_polynomial(text_polynomial: str) -> tuple[list[str],list[str]]:
    lst_polynomial = text_polynomial.split(";")
    
    clean_polynomial = lst_polynomial[0].replace(" + "," +").replace("+ "," +").replace("+"," +")
    clean_polynomial = clean_polynomial.replace(" - "," -").replace("- "," -").replace("-"," -")
    clean_polynomial_lst = clean_polynomial.split()
    clean_variables_lst = lst_polynomial[1].split(",")

    return clean_polynomial_lst,clean_variables_lst

def solving_polinomial(text_polynomial: str, cleaning_polynomial: Callable[[str],tuple[list[str]]]) -> float:
    """
    First we have to clean the polinomial using "clean_polinomial" function,
    than we create a dict with variables and their values. Finally, we disamble
    the element of polinomial to "coef", "char" and "degree" and solving it into a sum
    """
    polynomial, variables = cleaning_polynomial(text_polynomial)
    dict_of_variables = {}
    for pair in variables:
        variable, value = pair.split("=")
        variable = variable.strip()
        value = float(value)
        dict_of_variables[variable.strip()] = value
    
    polynomial_sum = 0
    for elem in polynomial:
        for char in elem:
            if char.isalpha():
                coef = elem[:elem.index(char)]
                if not coef or coef == "+" : coef = 1.0
                elif coef == "-": coef = -1.0
                else: coef = float(coef)
                
                if "^" in elem:
                    degree = float(elem[elem.index('^')+1:])
                else:
                    degree = 1.0
                
                char_value = dict_of_variables[char]
                polynomial_sum += coef*char_value**degree
                
    return round(polynomial_sum, 4)

def main():
    text_polinomial = input("Input your polinomial: ")
    print(solving_polinomial(text_polinomial, cleaning_polynomial))

if __name__ == "__main__":
    main()