from functools import partial, reduce
from itertools import chain, repeat
from math import dist, sqrt
from operator import add, mul, sub, truediv
from random import random, randrange, seed
from typing import Any, Callable, Generator, Self, Sequence


class Row(list):
    def __truediv__(self, value: Any) -> Generator[Any, None, None]:
        return map(truediv, self, repeat(value))
    
    def __mul__(self, value: Any) -> Generator[Any, None, None]:
        return map(mul, self, repeat(value))
    
    def __sub__(self, value: Sequence[Any]) -> Generator[Any, None, None]:
        return map(sub, self, value)
    
    def __str__(self) -> str:
        return f"[{', '.join(map('{:>5.2f}'.format, self))}]"
    
    def __matmul__(self, other: Self) -> Any:
        return sum(map(mul, self, other))
    
    def norm_one(self) -> Any:
        return sum(map(abs, self))
    
    def norm_inf(self) -> Any:
        return max(map(abs, self))
    
    def norm_two(self) -> Any:
        return sqrt(sum(s**2 for s in self))
    
    def residual(self, other: Self) -> Self:
        return Row(self - other)
    
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
    
    @classmethod
    def augmented(cls, matrix: Self, vector: Row) -> Self:
        return cls([[*m, v] for m, v in zip(matrix, vector)])
    
    @classmethod
    def concat(cls, left: Self, right: Self) -> Self:
        return cls([list(chain(s, o)) for s, o in zip(left, right)])
    
    @classmethod
    def one(cls, size: int) -> Self:
        res = cls.zeros(size, size)
        for i in range(size):
            res[i][i] = 1
        return res
    
    def __str__(self) -> str:
        return "\n".join(map(str, self.rows))
    
    def __getitem__(self, index: int) -> Row:
        return self.rows[index]
    
    def __setitem__(self, index: int, value: Sequence[Any]):
        self.rows[index][:] = value
    
    def __len__(self) -> int:
        return self.height
    
    def __matmul__(self, other: Self) -> Self:
        other = other.T()
        res = list()
        for row in self:
            res.append(list())
            for column in other:
                res[-1].append(row @ column)
        return Matrix(res)
    
    def T(self):
        return Matrix(list(map(Row, zip(*self))))
    
    def transpose(self):
        self.rows = self.T().rows
    
    def get_vector_b(self) -> Row:
        return Row(row[-1] for row in self)
    
    def get_right_half(self) -> Self:
        return Matrix([row[self.width//2:] for row in self])
    
    def fit(self, nums: Sequence[Any]) -> Row:
        return Row(sum(map(mul, row, nums)) for row in self)
    
    def _gaussian_forward(self) -> Generator[Any, None, None]:
        for i in range(self.height):
            yield self[i][i]
            self[i] /= self[i][i]
            for ii in range(i+1, self.height):
                self[ii] -= self[i] * self[ii][i]
    def gaussian_forward(self):
        all(self._gaussian_forward())
    
    def gaussian_reverse(self):
        for i in reversed(range(self.height)):
            for ii in range(i):
                self[ii] -= self[i] * self[ii][i]
    
    def solve_gaussian_single(self):
        """метод Гаусса (схему единственного деления)"""
        self.gaussian_forward()
        self.gaussian_reverse()
        return self.get_vector_b()
    
    def find_determinant(self) -> Any:
        self.transpose()
        res = reduce(mul, list(self._gaussian_forward()))
        return res
    
    def norm_one(self) -> Any:
        return max(map(Row.norm_one, self.T()))
    
    def norm_inf(self) -> Any:
        return max(map(Row.norm_one, self))
    
    def norm_F(self) -> Any:
        return sqrt(sum(s**2 for s in chain(*self)))
    
    def norm_M(self) -> Any:
        return self.height * max(map(abs, chain(*self)))

if __name__ == "__main__":
    print("Исходные данные")
    A = [[2.18, 2.44, 2.49],
         [2.17, 2.31, 2.49],
         [3.15, 3.22, 3.17],]
    b = [-4.34, -3.91, -5.27]
    A = Matrix(A)
    b = Row(b)
    print("Расширенная матрица")
    matrix = Matrix.augmented(A, b)
    print(matrix)

    print("После прямого прохода")
    matrix.gaussian_forward()
    print(matrix)

    print("После обратного прохода")
    matrix.gaussian_reverse()
    print(matrix)

    print("Вектор x")
    res = matrix.get_vector_b()
    print(res)

    print("Вектор невязки")
    got = A.fit(res)
    expected = b
    residual = expected.residual(got)
    print(residual)
    
    print("Норма1 ветора невязки")
    print(residual.norm_one())
    
    print("Определитель")
    print(Matrix(A).find_determinant())
    
    print("Единичная матрица")
    matrix = Matrix.concat(A, Matrix.one(A.height))
    print(matrix)
    
    print("После преобразований")
    matrix.solve_gaussian_single()
    print(matrix)
    
    print("Обратная матрица")
    invertible = matrix.get_right_half()
    print(invertible)
    
    print("Произведение матриц")
    print(invertible @ A)



    print("Число обусловленности")
    names = ["Норма 1", "Норма ∞", "Норма Фробениуса", "Максимальная норма"]
    funcs = [Matrix.norm_one, Matrix.norm_inf, Matrix.norm_F, Matrix.norm_M]
    for name, func in zip(names, funcs):
        print(f"{name:>18}: {func(A)*func(invertible):.15f}", )
