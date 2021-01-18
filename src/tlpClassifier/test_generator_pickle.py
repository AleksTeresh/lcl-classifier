import unittest
from fileHelp import import_data_set
from complexity import Complexity
import pickle
WHITE_DEGREE = 2
BLACK_DEGREE = 3

class TestClassification(unittest.TestCase):
    def test1(self):
        problems, restrictions, relaxations = import_data_set(WHITE_DEGREE,BLACK_DEGREE,"UC")
        for x in list(relaxations.keys()):
            for elem in relaxations[x]:
                self.assertIn(x,restrictions[elem])
                elem.set_complexity(Complexity.Constant)
            for elem in restrictions[x]:
                elem.set_complexity(Complexity.Constant)
        self.assertTrue(all([x.get_complexity() == Complexity.Constant for x in problems]))
if __name__ == '__main__':
    unittest.main()