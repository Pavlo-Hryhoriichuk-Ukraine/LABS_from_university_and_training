#lab11_2 (functions-generators)

def cubic_root(e: float,x: float) -> float|int:
    """
    Uses specific function to approximate cubic root
    of number and check the epsilon-accuraccy of approximation
    """
    X = x

    def functional(x:float|int):
        """
        Fiends next guess-value like generator in Newton's
        approximation of cubic root  
        """
        x /= 3
        yield x
        while True:
            x = 1/3 * (2 * x + X/(x**2))
            yield x

    gen = functional(x)
    while abs(x**3 - X) > e:
        x= next(gen)
    return x

def main():
    e = float(input("Input your epsilon-accuracy: "))
    x = float(input("Input number: "))
    print(cubic_root(e,x))

if __name__ == "__main__":
    main()