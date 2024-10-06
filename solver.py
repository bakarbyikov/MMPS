from functools import reduce
from itertools import count
from numbers import Real
from operator import mul
from typing import Generator

from matrix import Matrix
from misc import argmax
from row import Row


def _gaussian_forward(self) -> Generator[Real, None, None]:
    for row in range(self.height):
        yield self[row][row]
        self[row] /= self[row][row]
        for below in range(row+1, self.height):
            self[below] -= self[row] * self[below][row]
def gaussian_forward(matrix: Matrix) -> None:
    all(_gaussian_forward(matrix))
    
def gaussian_backward(matrix: Matrix) -> None:
    for row in reversed(range(matrix.height)):
        for above in range(row):
            matrix[above] -= matrix[row] * matrix[above][row]

def solve_gaussian_single(matrix: Matrix) -> Row:
    """метод Гаусса схема единственного деления"""
    result = matrix.copy()
    gaussian_forward(result)
    gaussian_backward(result)
    return result.get_vector_b()

def solve_gaussian_choose(matrix: Matrix) -> Row:
    """метод Гаусса с выбором ведущего элемента"""
    for column in range(matrix.height):
        choosen = argmax(matrix.get_column(column)[column:]) + column
        matrix.swap(column, choosen)
        matrix[column] /= matrix[column][column]
        for below in range(column+1, matrix.height):
            matrix[below] -= matrix[column] * matrix[below][column]
    gaussian_backward(matrix)
    return matrix.get_vector_b()

def find_determinant(matrix: Matrix) -> Real:
    matrix = matrix.T()
    return reduce(mul, list(_gaussian_forward(matrix)))


def solve_iter(matrix: Matrix, eps: float) -> tuple[Row, int]:
    answer = matrix.get_vector_b()
    for n_iter in count(1):
        new_answer = (matrix.get_coef_a() @ answer) + matrix.get_vector_b()
        delta = new_answer - answer
        if (delta.norm_one() < eps):
            break
        answer = new_answer
    return new_answer, n_iter

def solve_Seidel(matrix: Matrix, eps: float) -> tuple[Row, int]:
    new_answer = answer = matrix.get_vector_b()
    for n_iter in count(1):
        new_answer = answer.copy()
        for i, row in enumerate(matrix):
            new_answer[i] = row.fit(new_answer)
        delta = new_answer - answer
        if (delta.norm_one() < eps):
            break
        answer = new_answer
    return new_answer, n_iter