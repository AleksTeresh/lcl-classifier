import unittest

from two_labels_classifier import get_complexity_of
from complexity import Complexity
from bitarray import bitarray
from random import *
import numpy as np
def complexity(that):
    return get_complexity_of(*(bitarray(that[0]),bitarray(that[1])))
def random_string(length):
    return ''.join(str(x) for x in np.random.randint(2,size = length))

class TestClassification(unittest.TestCase):
    def test_unsolvable(self):
        for l_w in range(3,10):
            for l_b in range (3,10):
                #I.a,I.c
                problem_1 = '1'+(l_w-1)*'0', '0'+random_string(l_b-1)
                self.assertEqual(complexity(problem_1), Complexity.Unsolvable)
                self.assertEqual(complexity(problem_1[::-1]), Complexity.Unsolvable)
                #I.b,I.d
                problem_2 = (l_w-1)*'0'+'1', random_string(l_b-1)+'0'
                self.assertEqual(complexity(problem_2), Complexity.Unsolvable)
                self.assertEqual(complexity(problem_2[::-1]), Complexity.Unsolvable)
                #II.a,II.b
                problem_3 = '0'*l_w,random_string(l_b)
                self.assertEqual(complexity(problem_3), Complexity.Unsolvable)
                self.assertEqual(complexity(problem_3[::-1]), Complexity.Unsolvable)
    def test_constant(self):
        for l_w in range(3,10):
            for l_b in range (3,10):
                #III.a,III.b
                x = random_string(l_w)
                while (x == l_w*'0'):
                    x = random_string(l_w)
                problem_1 = x,l_b*'1'
                self.assertEqual(complexity(problem_1), Complexity.Constant)
                self.assertEqual(complexity(problem_1[::-1]), Complexity.Constant)
                #IV.a
                problem_2 = '1'+random_string(l_w-1),'1'+random_string(l_b-1)
                self.assertEqual(complexity(problem_2), Complexity.Constant)
                self.assertEqual(complexity(problem_2[::-1]), Complexity.Constant)
                #IV.b
                problem_3 = random_string(l_w-1)+'1',random_string(l_b-1)+'1'
                self.assertEqual(complexity(problem_3), Complexity.Constant)
                self.assertEqual(complexity(problem_3[::-1]), Complexity.Constant)
    def test_global(self):
        for l_w in range(3,10):
            #V.a
            problem_1 = '1'+(l_w-2)*'0'+'1','010'
            self.assertEqual(complexity(problem_1), Complexity.Global)
            self.assertEqual(complexity(problem_1[::-1]), Complexity.Global)
            for l_b in range (3,10):
                problem_2 = (l_w-2)*'0'+'1'+random_string(1),random_string(1)+'1'+(l_b-2)*'0'
                self.assertEqual(complexity(problem_2), Complexity.Global)
                self.assertEqual(complexity(problem_2[::-1]), Complexity.Global)
    def test_logarithmic(self):
        problems = [('01110','01110'),('1010','010'),('111110','010'),('011110','010'),('0100000','101'),('0111110','101'),('010000','0100000'),('01000','100001'),('01000','110')]
        for x in problems:
            self.assertEqual(complexity(x), Complexity.Logarithmic)
            self.assertEqual(complexity(x[::-1]), Complexity.Logarithmic)

if __name__ == '__main__':
    unittest.main()