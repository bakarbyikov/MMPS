from random import seed
import unittest

from matrix import Matrix
from row import Row


class TestStringMethods(unittest.TestCase):

    def test_shape(self):
        m = Matrix.zeros(2, 3)
        self.assertEqual(m.height, 2)
        self.assertEqual(m.width, 3)

    def test_zeros(self):
        m = Matrix.zeros(2, 3)
        string = (
            "[ 0.00,  0.00,  0.00]\n"
            "[ 0.00,  0.00,  0.00]"
        )
        self.assertEqual(str(m), string)

    def test_ones(self):
        m = Matrix.ones(3, 2)
        string = (
            "[ 1.00,  1.00]\n"
            "[ 1.00,  1.00]\n"
            "[ 1.00,  1.00]"
        )
        self.assertEqual(str(m), string)

    def test_full(self):
        m = Matrix.full(float, 3, 3)
        string = (
            "[ 0.00,  0.00,  0.00]\n"
            "[ 0.00,  0.00,  0.00]\n"
            "[ 0.00,  0.00,  0.00]"
        )
        self.assertEqual(str(m), string)

    def test_randint(self):
        seed(0)
        m = Matrix.randint(3, 3, 10)
        string = (
            "[ 6.00,  6.00,  0.00]\n"
            "[ 4.00,  8.00,  7.00]\n"
            "[ 6.00,  4.00,  7.00]"
        )
        self.assertEqual(str(m), string)

    def test_random(self):
        seed(0)
        m = Matrix.random(3, 3)
        string = (
            "[ 0.84,  0.76,  0.42]\n"
            "[ 0.26,  0.51,  0.40]\n"
            "[ 0.78,  0.30,  0.48]"
        )
        self.assertEqual(str(m), string)

    def test_zero_height(self):
        try:
            Matrix.zeros(0, 10)
        except Exception as e:
            self.assertIsInstance(e, NotImplementedError)

    def test_zero_width(self):
        try:
            Matrix.zeros(10, 0)
        except Exception as e:
            self.assertIsInstance(e, NotImplementedError)

    def test_row_divide_value(self):
        seed(0)
        m = Matrix.randint(2, 2, 10)
        self.assertEqual(str(m), (
            "[ 6.00,  6.00]\n"
            "[ 0.00,  4.00]"
        ))
        before = m[0]
        m[0] /= 2
        self.assertIs(before, m[0])
        self.assertEqual(str(m), (
            "[ 3.00,  3.00]\n"
            "[ 0.00,  4.00]"
        ))

    def test_transpose(self):
        seed(0)
        m = Matrix.randint(2, 3, 10)
        self.assertEqual(str(m), (
            "[ 6.00,  6.00,  0.00]\n"
            "[ 4.00,  8.00,  7.00]"
        ))
        m.transpose()
        self.assertEqual(str(m), (
            "[ 6.00,  4.00]\n"
            "[ 6.00,  8.00]\n"
            "[ 0.00,  7.00]"
        ))

    def test_matmul(self):
        A = Matrix([[4, 2],
                    [9, 0]])
        B = Matrix([[3, 1],
                    [-3, 4]])
        C = A @ B
        expected = Matrix([[6, 12],
                           [27, 9]])
        self.assertEqual(C, expected)

    def test_matmul2(self):
        A = Matrix([[2, 1],
                    [-3, 0],
                    [4, -1]])
        B = Matrix([[5, -1, 6],
                    [-3, 0, 7]])
        C = A @ B
        expected = Matrix([[7, -2, 19],
                           [-15, 3, -18],
                           [23, -4, 17]])
        self.assertEqual(C, expected)

    def test_matmul_row(self):
        A = Matrix([[2, 1, 1],
                    [-3, 0, 2],
                    [4, -1, 3]])
        B = Row([5, -1, 6])
        C = A @ B
        print()
        print(C)
        print()

        expected = Row([15, -3, 39])
        self.assertEqual(C, expected)


if __name__ == '__main__':
    unittest.main()
