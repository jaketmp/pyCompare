import numpy
import pandas
import sys
import unittest
import tempfile
import os
from unittest import mock
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import repeat

sys.path.append("..")
import pyCompare

class test_plotHelpers(unittest.TestCase):

	def test_rangeFrameLocator(self):

		from pyCompare._rangeFrameLocator import rangeFrameLocator

		obtained = rangeFrameLocator([1,2,3,4,5,6,7,8,9,10], (2,9))
		expected = [2, 3, 4, 5, 6, 7, 8, 9]

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLocator([1,4,6,8,10,12,14,16], (2,9))
		expected = [2, 4, 6, 8, 9]

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLocator([2,4,6,8,10,12,14,16], (1.1,13.5))
		expected = [1.1, 2, 4, 6, 8, 10, 12, 13.5]

		self.assertEqual(obtained, expected)


	def test_rangeFrameLabler(self):

		from pyCompare._rangeFrameLocator import rangeFrameLabler

		obtained = rangeFrameLabler([2, 3, 4, 5, 6, 7, 8, 9], ['2', '3', '4', '5', '6', '7', '8', '9'], 1)
		expected = ['2', '3', '4', '5', '6', '7', '8', '9']

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLabler([1,1.5, 4, 6, 9], ['1','1.5', '4', '6', '9'], 2)
		expected = ['1', '', '4', '6', '9']

		self.assertEqual(obtained, expected)

		obtained = rangeFrameLabler([1.1, 4, 6, 8, 10, 13, 13.5], ['1.1', '4', '6', '8', '10', '13', '13.5'], 2)
		expected = ['1.1', '4', '6', '8', '10', '', '13.5']

		self.assertEqual(obtained, expected)


class test_statsHelpers(unittest.TestCase):

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


	def test_detrend(self):

		from pyCompare._detrend import detrend

		sampleCount = numpy.random.randint(50, 500, size=None)
		data1 = numpy.random.randn(sampleCount)

		slope = (50 - 0.1) * numpy.random.random_sample() + 0.1

		with self.subTest(msg='None'):

			data2 = data1 * slope

			data2Obtained, slopeObtained, slopeErrObtained = detrend(None, data1, data2)

			numpy.testing.assert_array_equal(data2, data2Obtained)
			self.assertIsNone(slopeObtained)
			self.assertIsNone(slopeErrObtained)

		with self.subTest(msg='Linear'):

			data2 = data1 * slope

			data2Obtained, slopeObtained, slopeErrObtained = detrend('Linear', data1, data2)

			numpy.testing.assert_allclose(data1, data2Obtained)
			numpy.testing.assert_allclose(slope, slopeObtained)

		with self.subTest(msg='ODR'):

			data2 = data1 * slope

			data2Obtained, slopeObtained, slopeErrObtained = detrend('ODR', data1, data2)

			numpy.testing.assert_allclose(data1, data2Obtained)
			numpy.testing.assert_allclose(slope, slopeObtained)


	def test_detrend_raises(self):

		from pyCompare._detrend import detrend

		self.assertRaises(NotImplementedError, detrend, 'Not known', None, None)


	def test_calculateConfidenceIntervals(self):
		from pyCompare._calculateConfidenceIntervals import calculateConfidenceIntervals

		noSamp = numpy.random.randint(100, high=500, size=None)

		data1 = numpy.random.rand(noSamp)
		data2 = numpy.random.rand(noSamp)

		with self.subTest(msg='Approximate'):

			md = -16.26
			sd = 19.61
			n = 85
			loA = 1.96
			ci = 95

			expected = {'mean': (-20.49, -12.03),
						'upperLoA': (14.92, 29.43),
						'lowerLoA': (-61.95, -47.44)}

			obtained = calculateConfidenceIntervals(md, sd, n, loA, ci, 'Approximate')

			key = 'mean'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)
			key = 'upperLoA'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)
			key = 'lowerLoA'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)

		with self.subTest(msg='Exact paired'):

			md = -16.26
			sd = 19.61
			n = 85
			loA = 1.96
			ci = 95

			expected = {'mean': (-20.49, -12.03),
						'upperLoA': (3.35, 22.96),
						'lowerLoA': (-55.48, -35.87)}

			# Mock to avoid running carkeetCIest again
			with mock.patch('pyCompare._calculateConfidenceIntervals.parallelCarkeetCIest') as mocked:
				mocked.return_value = (1, 2)
				# mocked.__reduce__ = lambda self: (mock.MagicMock, ())
				obtained = calculateConfidenceIntervals(md, sd, n, loA, ci, 'exact paired')

			key = 'mean'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)
			key = 'upperLoA'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)
			key = 'lowerLoA'
			numpy.testing.assert_array_almost_equal(expected[key], obtained[key], decimal=2)


	def test_calculateConfidenceIntervals_raises(self):
		from pyCompare._calculateConfidenceIntervals import calculateConfidenceIntervals

		with self.subTest(msg='CI range smaller than 1%'):
			self.assertRaises(ValueError, calculateConfidenceIntervals, None, None, 1, None, 0, None)

		with self.subTest(msg='CI range greater than than 99%'):
			self.assertRaises(ValueError, calculateConfidenceIntervals, None, None, 1, None, 100, None)

		with self.subTest(msg='Unknown CI method'):
			self.assertRaises(NotImplementedError, calculateConfidenceIntervals, 1, 1, 1, 1.96, 95, 'Undefined Method')
