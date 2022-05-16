import unittest
import numpy as np
import criticality as cr


class Testget_avalanches(unittest.TestCase):
    expected_output_s = np.asarray([2, 3, 3, 6])
    expected_output_t = np.asarray([2, 2, 3, 1])
    data = np.array([[1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 3, 0],
                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]])

    data2 = np.nansum(data, axis=0)

    def test_get_avalanches(self):
        test_output = \
                cr.get_avalanches(self.data, perc=0.0, ncells=-1)
        test_output_s = test_output['S']
        test_output_t = test_output['T']
        msg = "get avalanches burst"
        self.assertEqual(self.expected_output_s.tolist(),
                         test_output_s.tolist(), msg)
        msg = "get avalanches T"
        self.assertEqual(self.expected_output_t.tolist(),
                         test_output_t.tolist(), msg)

    def test_get_avalanches_ncells(self):
        test_output = \
                cr.get_avalanches(self.data2, perc=0.0, ncells=2)
        test_output_s = test_output['S']
        test_output_t = test_output['T']
        msg = "get avalanches burst"
        self.assertEqual(self.expected_output_s.tolist(),
                         test_output_s.tolist(), msg)
        msg = "get avalanches T"
        self.assertEqual(self.expected_output_t.tolist(),
                         test_output_t.tolist(), msg)
