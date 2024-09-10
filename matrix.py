from functools import partial
from itertools import repeat
from operator import mul, sub, truediv
from random import random, randrange, seed
from typing import Any, Callable, Generator, Self, Sequence


class Row(list):
    def __truediv__(self, value: int|float) -> Generator[Any, None, None]:
        return map(truediv, self, repeat(value))
    
    def __mul__(self, value: int|float) -> Generator[Any, None, None]:
        return map(mul, self, repeat(value))
    
    def __sub__(self, value: int|float) -> Generator[Any, None, None]:
        return map(sub, self, value)
    
class Matrix:
    def __init__(self, rows: list[list[Any]]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.rows = [Row(r) for r in rows]
        
    @classmethod
    def full(cls, filler: Callable[[], Any], height: int, width: int) -> Self:
        if height <= 0 or width <= 0:
            raise NotImplementedError(
                "Don't do this! Why do you want matrix "
                f"with shape {height}x{width}?"
                )
        return cls([[filler() for _ in range(width)] for _ in range(height)])
    
    @classmethod
    def zeros(cls, height: int, width: int) -> Self:
        return cls.full(int, height, width)
    
    @classmethod
    def ones(cls, height: int, width: int) -> Self:
        return cls.full(partial(int, 1), height, width)
    
    @classmethod
    def randint(cls, height: int, width: int, *args) -> Self:
        return cls.full(partial(randrange, *args), height, width)
    
    @classmethod
    def random(cls, height: int, width: int, *args) -> Self:
        return cls.full(partial(random, *args), height, width)
    
    def __str__(self) -> str:
        return "\n".join(map(str, self.rows))
    
    def __getitem__(self, index: int) -> Row:
        return self.rows[index]
    
    def __setitem__(self, index: int, value: Sequence):
        self.rows[index][:] = value


if __name__ == "__main__":
    seed(0)
    matrix = Matrix.randint(4, 5, 10)
    print(matrix)
    print()
    for i in range(matrix.height):
        matrix[i] /= matrix[i][i]
        for ii in range(i+1, matrix.height):
            matrix[ii] -= matrix[i] * matrix[ii][i]
    print(matrix)
    print()
        
    for i in reversed(range(matrix.height)):
        for ii in range(i):
            matrix[ii] -= matrix[i] * matrix[ii][i]
    print(matrix)