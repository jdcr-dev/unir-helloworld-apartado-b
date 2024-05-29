import app
from typing import Final

class InvalidPermissions(Exception):
    pass


class Calculator:
    SQRT_VALUE: Final[float] = 0.5

    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def substract(self, x, y):
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y):
        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")

        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        return x ** y

    def sqrt(self, x):
        self.check_types(x)
        return self.power(x, self.SQRT_VALUE)

    def check_types(self, *args):        
        for arg in args:            
            if not isinstance(arg, (int, float)):
                raise TypeError("Parameters must be numbers")

if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
