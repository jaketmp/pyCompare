import numpy
import pandas
import sys
import unittest
import tempfile
import os

sys.path.append("..")
import pyCompare

class test_plotting(unittest.TestCase):

	def test_blandAtlman_output(self):

		noSamp = numpy.random.randint(100, high=500, size=None)

		with tempfile.TemporaryDirectory() as tmpdirname:
			with self.subTest(msg='Default Parameters'):
				outputPath = os.path.join(tmpdirname, 'plot')
				pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
										  numpy.random.rand(noSamp)*50+100,
										  confidenceIntervalMethod='exact paired',
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg="Don't plot CI"):
				outputPath = os.path.join(tmpdirname, 'plot_no_CI')
				pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
										  numpy.random.rand(noSamp)*50+100,
										  confidenceInterval=None,
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg="Detrend"):
				outputPath = os.path.join(tmpdirname, 'detrend')
				pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
										  numpy.random.rand(noSamp)*50+100,
										  confidenceInterval=None,
										  detrend='linear',
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='Modify LoA'):
				outputPath = os.path.join(tmpdirname, 'plot_mod_LoA')
				pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
										  numpy.random.rand(noSamp)*50+100,
										  limitOfAgreement=1.1,
										  confidenceIntervalMethod='approximate', # Use aproximate method for speed
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='title'):
				outputPath = os.path.join(tmpdirname, 'plot_detrend')
				pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
										  numpy.random.rand(noSamp)*50+100,
										  confidenceInterval=None,
										  title='comparison of x and y',
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))


	def test_blandAtlman_screen(self):

		noSamp = numpy.random.randint(100, high=500, size=None)

		pyCompare.blandAltman(numpy.random.rand(noSamp)*100+100,
								  numpy.random.rand(noSamp)*50+100,
								  confidenceIntervalMethod='approximate',
								  savePath=None)


	def test_blandAtlman_raises(self):

		noSamp = numpy.random.randint(100, high=500, size=None)
		values = numpy.random.rand(noSamp)

		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, limitOfAgreement=-2)
		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, confidenceInterval=-2)
		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, confidenceInterval=100)
		self.assertRaises(NotImplementedError, pyCompare.blandAltman, values, values, detrend='Unknown method')
		self.assertRaises(NotImplementedError, pyCompare.blandAltman, values*2, values, confidenceIntervalMethod='Unknown method')
