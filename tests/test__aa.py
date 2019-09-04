import pandas # pandas must be imported to intercept the subsequent failure.
import unittest
import warnings
import matplotlib
import os

##
# Handle undefined DISPLAY on Travis
##
matplotlib.use('Agg')

##
# Decoy warning to catch the `dictionary changed size during iteration` RuntimeError
# See https://bugs.python.org/issue29620
##
def raiseWarning():
	warnings.warn('You were warned', UserWarning)

class test__AA__decoy(unittest.TestCase):

	# @unittest.expectedFailure  # No longer fails, the bug above seems fixed
	def test__AA(self):
		csvFile = pandas.read_csv('referenceCIs.csv')
		self.assertWarnsRegex(UserWarning, 'You were warned', raiseWarning)
