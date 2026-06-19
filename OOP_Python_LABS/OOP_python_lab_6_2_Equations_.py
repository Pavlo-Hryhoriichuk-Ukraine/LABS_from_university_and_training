import numpy
import time

class LiniarEquation():
    __slots__ = ('b', 'c')
    def __init__(self, b, c):
        self._b = b
        self._c = c
    
    def solve(self) -> list[str | int | float]:
        if self._b == 0 and self._c == 0:
            return ['inf'], "linear"
        elif self._b == 0:
            return ['undefined'], "linear"
        return [-self._c / self._b], "linear"

class QuadraticEquation(LiniarEquation):
    __slots__ = ('a',)
    
    def discriminant(self) -> int | float:
        return self._b ** 2 - 4 * self._a * self._c
    
    def solve(self) -> list[str | int | float]:
        if self._a == 0:
            return super().solve()
        
        d = self.discriminant()

        if d < 0:
            return ['undefined'], "quadratic" 
        elif d == 0:
            return [-self._b / (2 * self._a), -self._b / (2 * self._a)], "quadratic" 
        else:
            sqrt_d = d ** 0.5
            x_1 = (-self._b + sqrt_d) / (2 * self._a)
            x_2 = (-self._b - sqrt_d) / (2 * self._a)
            return [x_1, x_2],  "quadratic"

class BiQuadraticEquation(QuadraticEquation):
    def solve(self):
        if self._t == 0 or self._b != 0:
            return super().solve()
        resoult = []
        solutions = super().solve()

        for root in solutions:
            if type(root) == str:
                resoult.append(root)
            elif root == 0:
                resoult.append(0)
            elif root > 0:
                x_1 = root ** 0.5
                x_2 = -x_1
                resoult.append(x_1)
                resoult.append(x_2)
            else:
                resoult.append('undefined')
        
        return resoult, "biquadratic"

class QubicEquation(QuadraticEquation):
    __slots__ = ('q', )
    
    def solve(self):
        if self._q == 0:
            return super().solve()
        return numpy.roots([self._q, self._a, self._b, self._c]), "cubic"
        

class AlgebraicEquation(QubicEquation, BiQuadraticEquation):
    __slots__ = ()

    def __init__(self, string: str):
        self._t, self._q, self._a, self._b, self._c = self.parse_string(string)

    def solve(self):
        current_time = time.time()
        resoult = super().solve()
        return {"roots": resoult[0], "type": resoult[1], "time": time.time() - current_time}
    
    @staticmethod
    def parse_string(string) -> tuple[float]:
        equation = string.split("=")[0].replace(' ','')
        clean_equation = equation.replace("+"," +").replace("-"," -")
        lst = clean_equation.split()
        t,q,a,b,c = 0,0,0,0,0

        for group in lst:
            if "x^4" in group:
                coeff = group.replace("*x^4",'').replace("x^4",'')
                if not coeff or coeff =='+': t += 1.0
                elif coeff == '-': t += -1.0
                else: t += float(coeff)

            elif "x^3" in group:
                coeff = group.replace("*x^3",'').replace("x^3",'')
                if not coeff or coeff =='+': q += 1.0
                elif coeff == '-': q += -1.0
                else: q += float(coeff)

            elif "x^2" in group:
                coeff = group.replace("*x^2",'').replace("x^2",'')
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

        return t,q,a,b,c

if __name__ == "__main__":
    equation = AlgebraicEquation("5x^3 + 8x^2 + 0x + 3 = 0")
    print(equation.solve())