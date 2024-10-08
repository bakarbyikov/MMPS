from fractions import Fraction
from functools import partial
from itertools import chain, repeat
from math import sqrt
from numbers import Real
from operator import mul, sub
from random import random, randrange
from typing import Callable, Self, Sequence

from row import Row


class Matrix:
    def __init__(self, rows: list[list[Real]]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.rows = [Row(r) for r in rows]
        
    @classmethod
    def full(cls, filler: Callable[[], Real], height: int, width: int) -> Self:
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
    
    def as_fractions(self) -> Self:
        rows = [[Fraction.from_float(cell) for cell in row] for row in self]
        return Matrix(rows)
    
    def __rmul__(self, other: Real) -> Self:
        return Matrix(list(map(mul, self, repeat(other))))
    
    def __sub__(self, other: Real) -> Self:
        return Matrix(list(map(sub, self, other)))
    
    def __format__(self, format_spec: str) -> str:
        if format_spec.endswith('m'):
            ndigits = int(format_spec[:-1])
            return self.str_round(ndigits)
        return "\n".join(map(format, self.rows, repeat(format_spec)))
    
    def str_round(self, ndigits: int) -> str:
        return format(self, f">{ndigits+3}.{ndigits}f")
    
    def __str__(self) -> str:
        result = [row.danil() for row in self.T()]
        return "\n".join(f"[{' '.join(row)}]" for row in zip(*result))
        self.T()
        lines = [[format(cell, ' g') for cell in row] for row in self]
        result = list()
        for column in zip(*lines):
            column: list[str]
            mixim = 0, 0
            for value in column:
                left, _, right = value.partition('.')
                mixim = map(max, mixim, map(len, (left, right)))
            for value in column:
                left, _, right = map(len, value.partition('.'))
                result[-1].append(value.ljust)
                
        return '\n'.join(map(' '.join, zip(*result)))
    
    def __getitem__(self, index: int) -> Row:
        return self.rows[index]
    
    def __setitem__(self, index: int, value: Sequence[Real]):
        self.rows[index][:] = value
    
    def __len__(self) -> int:
        return self.height
    
    def __matmul(self, other: Self) ->Self:
        other = other.T()
        res = list()
        for row in self:
            res.append(list())
            for column in other:
                res[-1].append(row @ column)
        return Matrix(res)
    
    def __matmul__(self, other: Self|Row) -> Self|Row:
        if isinstance(other, Matrix):
            return self.__matmul(other)
        return self.__matmul(Matrix([other])).get_vector_b()
    
    def T(self):
        return Matrix(list(map(Row, zip(*self))))
    
    def transpose(self):
        self.rows = self.T().rows
    
    def get_vector_b(self) -> Row:
        return Row(row[-1] for row in self)
    
    def get_right_half(self) -> Self:
        return Matrix([row[self.width//2:] for row in self])
    
    def get_column(self, index: int) -> Row:
        return Row(row[index] for row in self)
    
    def get_coef_a(self) -> Self:
        return Matrix([row[:-1] for row in self])
    
    def deaug(self) -> tuple[Self, Row]:
        return self.get_coef_a(), self.get_vector_b()
    
    def fit(self, nums: Sequence[Real]) -> Row:
        return Row(sum(map(mul, row, nums)) for row in self)
    
    def swap(self, first: int, second: int):
        self.rows[first], self.rows[second] = self.rows[second], self.rows[first]
    
    def norm_one(self) -> Real:
        return max(map(Row.norm_one, self.T()))
    
    def norm_inf(self) -> Real:
        return max(map(Row.norm_one, self))
    
    def norm_F(self) -> Real:
        return sqrt(sum(s**2 for s in chain(*self)))
    
    def norm_M(self) -> Real:
        return self.height * max(map(abs, chain(*self)))
    
    def copy(self) -> Self:
        return Matrix(self)
    
    def to_iter_form(self) -> Self:
        result = self.copy()
        for i in range(self.height):
            result[i] /= -self[i][i]
            result[i][i] = 0
            result[i][-1] *= -1
        return result
    
if __name__ == "__main__":
    mat = Matrix.random(3, 3)
    print(mat)