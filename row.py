import collections
from itertools import repeat
from math import sqrt
from numbers import Real
from operator import add, mul, neg, sub, truediv
from typing import Self, Sequence

from misc import centrify


class Row(list):
    def __truediv__(self, value: Real) -> Self:
        if not isinstance(value, collections.abc.Sequence):
            value = repeat(value)
        return Row(map(truediv, self, value))

    def __neg__(self) -> Self:
        return Row(map(neg, self))

    def __mul__(self, value: Real) -> Self:
        return Row(map(mul, self, repeat(value)))

    def __rmul__(self, value: Real) -> Self:
        return Row(map(mul, self, repeat(value)))

    def __add__(self, value: Self) -> Self:
        return Row(map(add, self, value))

    def __radd__(self, value: Self) -> Self:
        return self.__add__(value)

    def __iadd__(self, value: Self) -> Self:
        return self.__add__(value)

    def __sub__(self, value: Sequence[Real]) -> Self:
        return Row(map(sub, self, value))

    def __format__(self, format_spec: str) -> str:
        return f"[{' '.join(map(format, self, repeat(format_spec)))}]"

    def danil(self) -> list[str]:
        formated = [format(cell, ' g') for cell in self]
        maxim = [0, 0]
        point = False
        for value in formated:
            whole, _, decimal = map(len, value.partition('.'))
            point |= _
            maxim[:] = map(max, maxim, (whole, decimal))
        result = list()
        for value in formated:
            whole, _, decimal = map(len, value.partition('.'))
            if _ != 1 and point:
                decimal -= 1
            result.append(centrify(value, maxim[0]-whole, maxim[1]-decimal))
        return result

    def __str__(self) -> str:
        return format(self, 'g')

    def __matmul__(self, other: Self) -> Real:
        return sum(map(mul, self, other))

    def copy(self) -> Self:
        return Row(self)

    def abs(self) -> Self:
        return Row(map(abs, self))

    def norm_one(self) -> Real:
        return sum(map(abs, self))

    def norm_inf(self) -> Real:
        return max(map(abs, self))

    def norm_two(self) -> Real:
        return sqrt(sum(s**2 for s in self))

    def residual(self, other: Self) -> Self:
        return Row(self - other)

    def fit(self, x: Self) -> Real:
        return sum(map(mul, self, x), start=self[-1])


if __name__ == "__main__":
    from random import random, randrange
    row = Row([round(random()*100, randrange(10)) for _ in range(4)])
    for i in row.danil():
        print(i, "|")
    # print(f"{row:.2f}")
    # print(str(row))
