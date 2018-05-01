import numpy
import pandas
import sys
import unittest
import tempfile
import os

sys.path.append("..")
import pyCompare

class test_plotting_helpers(unittest.TestCase):

	def test_rangeFrameLocator(self):

		from pyCompare._rangeFrameLocator import rangeFrameLocator

		obtained = rangeFrameLocator([1,2,3,4,5,6,7,8,9,10], (2,9))
		expected = [2, 3, 4, 5, 6, 7, 8, 9]

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLocator([1,4,6,8,10,12,14,16], (2,9))
		expected = [2, 4, 6, 9]

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLocator([2,4,6,8,10,12,14,16], (1.1,13.5))
		expected = [1.1, 4, 6, 8, 10, 12, 13.5]

		self.assertEqual(obtained, expected)

