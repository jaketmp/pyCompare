import numpy
import pandas
import sys
import unittest
import tempfile
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import repeat

sys.path.append("..")
import pyCompare

class test_helpers(unittest.TestCase):

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


	def test_carkeetCIest(self):

		from pyCompare._carkeetCIest import carkeetCIest

		referenceValues = pandas.read_csv('referenceCIs.csv')

		# Calculation of bounds is so expensive we random select a small number of cases from the reference table rather thatn doing them all.
		noSamples = 4

		referenceValues = referenceValues.sample(n=noSamples)

		obtained = list()
		expected = list()
		n = list()
		gamma = list()

		for i, row in referenceValues.iterrows():
			level = numpy.random.randint(1, high=5, size=None)

			n.append(row.v + 1)
			expected.append(row.iloc[level])
			gamma.append(float(row.index[level]))

		with ProcessPoolExecutor(max_workers=None) as executor:
			for result in executor.map(carkeetCIest, n, gamma, repeat(1.96)):
				obtained.append(numpy.round(result, 4))

		numpy.testing.assert_allclose(expected, obtained, atol=0.001)
