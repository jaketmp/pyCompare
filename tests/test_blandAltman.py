import numpy
import sys
import unittest
import tempfile
import os

sys.path.append("..")
import pyCompare

class test_plotting(unittest.TestCase):

	def setUp(self):

		self.noSamp = numpy.random.randint(100, high=500, size=None)


	def test_blandAtlman_saves(self):

		with tempfile.TemporaryDirectory() as tmpdirname:
			with self.subTest(msg='Default Parameters'):
				outputPath = os.path.join(tmpdirname, 'plot')
				pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
										  numpy.random.rand(self.noSamp)*50+100,
										  confidenceIntervalMethod='approximate',
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='No CIs'):
				outputPath = os.path.join(tmpdirname, 'noCIplot')
				pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
										  numpy.random.rand(self.noSamp)*50+100,
										  confidenceInterval=None,
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='Percentage'):
				outputPath = os.path.join(tmpdirname, 'plot_percentage')
				pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
										  numpy.random.rand(self.noSamp)*50+100,
										  confidenceIntervalMethod='approximate',
										  percentage=True,
										  savePath=outputPath)

				self.assertTrue(os.path.exists(outputPath))


	def test_blandAtlman_axis_handle(self):

		import matplotlib

		with self.subTest(msg='Single axis'):

			fig, ax = matplotlib.pyplot.subplots()

			ax = pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
									  numpy.random.rand(self.noSamp)*50+100,
									  confidenceIntervalMethod='approximate',
									  savePath=None,
									  ax=ax)

			self.assertTrue(isinstance(ax, matplotlib.axes._subplots.Axes))

		with self.subTest(msg='Multiple axes'):

			fig, ax = matplotlib.pyplot.subplots(2,2)

			ax1 = pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
									   numpy.random.rand(self.noSamp)*50+100,
									   confidenceIntervalMethod='approximate',
									   savePath=None,
									   ax=ax[1,1])

			ax2 = pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
									   numpy.random.rand(self.noSamp)*50+100,
									   confidenceIntervalMethod='approximate',
									   savePath=None,
									   ax=ax[0,0])

			self.assertTrue(isinstance(ax1, matplotlib.axes._subplots.Axes))
			self.assertTrue(isinstance(ax2, matplotlib.axes._subplots.Axes))


	def test_blandAtlman_screen(self):

		pyCompare.blandAltman(numpy.random.rand(self.noSamp)*100+100,
								  numpy.random.rand(self.noSamp)*50+100,
								  confidenceIntervalMethod='approximate',
								  savePath=None)


	def test_blandAtlman_raises(self):

		values = numpy.random.rand(self.noSamp)

		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, limitOfAgreement=-2)
		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, confidenceInterval=-2)
		self.assertRaises(ValueError, pyCompare.blandAltman, values, values, confidenceInterval=100)
		self.assertRaises(NotImplementedError, pyCompare.blandAltman, values, values, detrend='Unknown method')
		self.assertRaises(NotImplementedError, pyCompare.blandAltman, values*2, values, confidenceIntervalMethod='Unknown method')


	def test_drawBlandAtlman(self):
		from pyCompare._plotBlandAltman import _drawBlandAltman

		with tempfile.TemporaryDirectory() as tmpdirname:

			with self.subTest(msg='With CIs'):
				outputPath = os.path.join(tmpdirname, 'save_plot')
				_drawBlandAltman(numpy.array([1,2,3,4,5,6]),
								 numpy.array([1.1,1.9,2.5,4.2,5.1,5.6]),
								 0,
								 1,
								 False,
								 1.96,
								 {'mean':[-1,1],'upperLoA':[2,2.5], 'lowerLoA':[-2.5, 2]},
								 ('detrending method', 12.2, 243.2),
								 'a title',
								 None,
								 (10, 7),
								 72,
								 outputPath,
								 'png',
								 'red',
								 'green',
								 'blue')

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='No CIs'):
				outputPath = os.path.join(tmpdirname, 'save_plot_no_CI')
				_drawBlandAltman(numpy.array([1,2,3,4,5,6]),
								 numpy.array([1.1,1.9,2.5,4.2,5.1,5.6]),
								 0,
								 1,
								 False,
								 2,
								 {},
								 (None, None, None),
								 'a title',
								 None,
								 (10, 7),
								 72,
								 outputPath,
								 'png',
								 'red',
								 'green',
								 'blue')

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='Percentages, with CIs'):
				outputPath = os.path.join(tmpdirname, 'save_plot_percentage')
				_drawBlandAltman(numpy.array([1,2,3,4,5,6]),
								 numpy.array([1.1,1.9,2.5,4.2,5.1,5.6]),
								 0,
								 1,
								 True,
								 1.96,
								 {'mean':[-1,1],'upperLoA':[2,2.5], 'lowerLoA':[-2.5, 2]},
								 ('detrending method', 12.2, 243.2),
								 'a title',
								 None,
								 (10, 7),
								 72,
								 outputPath,
								 'png',
								 'red',
								 'green',
								 'blue')

				self.assertTrue(os.path.exists(outputPath))

			with self.subTest(msg='Percentages, no CIs'):
				outputPath = os.path.join(tmpdirname, 'save_plot_percentag_no_CI')
				_drawBlandAltman(numpy.array([1,2,3,4,5,6]),
								 numpy.array([1.1,1.9,2.5,4.2,5.1,5.6]),
								 0,
								 1,
								 True,
								 2,
								 {},
								 (None, None, None),
								 'a title',
								 None,
								 (10, 7),
								 72,
								 outputPath,
								 'png',
								 'red',
								 'green',
								 'blue')

				self.assertTrue(os.path.exists(outputPath))
