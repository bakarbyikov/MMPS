from random import seed
import unittest

from matrix import Matrix

class TestStringMethods(unittest.TestCase):
    
    def test_shape(self):
        m = Matrix.zeros(2, 3)
        self.assertEqual(m.height, 2)
        self.assertEqual(m.width, 3)
    
    def test_zeros(self):
        m = Matrix.zeros(2, 3)
        string = (
            "[0, 0, 0]\n"
            "[0, 0, 0]"
        )
        self.assertEqual(str(m), string)
    
    def test_ones(self):
        m = Matrix.ones(3, 2)
        string = (
            "[1, 1]\n"
            "[1, 1]\n"
            "[1, 1]"
        )
        self.assertEqual(str(m), string)
    
    def test_full(self):
        m = Matrix.full(float, 3, 3)
        string = (
            "[0.0, 0.0, 0.0]\n"
            "[0.0, 0.0, 0.0]\n"
            "[0.0, 0.0, 0.0]"
        )
        self.assertEqual(str(m), string)
    
    def test_randint(self):
        seed(0)
        m = Matrix.randint(3, 3, 10)
        string = (
            "[6, 6, 0]\n"
            "[4, 8, 7]\n"
            "[6, 4, 7]"
        )
        self.assertEqual(str(m), string)
        
    def test_random(self):
        seed(0)
        m = Matrix.random(3, 3)
        string = (
            "[0.8444218515250481, 0.7579544029403025, 0.420571580830845]\n"
            "[0.25891675029296335, 0.5112747213686085, 0.4049341374504143]\n"
            "[0.7837985890347726, 0.30331272607892745, 0.4765969541523558]"
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
            "[6, 6]\n"
            "[0, 4]"
        ))
        before = m[0]
        m[0] /= 2
        self.assertIs(before, m[0])
        self.assertEqual(str(m), (
            "[3.0, 3.0]\n"
            "[0, 4]"
        ))
        

if __name__ == '__main__':
    unittest.main()