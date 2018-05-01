import pandas # pandas must be imported to intercept the subsequent failure.
import unittest
import warnings
import os
import matplotlib


##
# Handle undefined DISPLAY on Travis
##
if os.environ.get('DISPLAY','') == '':
	print('no display found. Using non-interactive Agg backend')
	matplotlib.use('Agg')

##
# Decoy warning to catch the `dictionary changed size during iteration` RuntimeError
# See https://bugs.python.org/issue29620
##
def raiseWarning():
	warnings.warn('You were warned', UserWarning)

class test__AA__decoy(unittest.TestCase):

	@unittest.expectedFailure
	def test__AA(self):
		dilutionMap = pandas.read_csv(os.path.join('..', 'nPYc', 'StudyDesigns', 'DilutionSeries.csv'))
		self.assertWarnsRegex(UserWarning, 'You were warned', raiseWarning)
