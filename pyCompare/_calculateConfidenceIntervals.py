import numpy
from scipy import stats
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import repeat

from ._carkeetCIest import carkeetCIest

def calculateConfidenceIntervals(md, sd, n, limitOfAgreement, confidenceInterval, confidenceIntervalMethod):

	confidenceIntervals = dict()

	if not (confidenceInterval < 99.9) & (confidenceInterval > 1):
		raise ValueError(f'"confidenceInterval" must be a number in the range 1 to 99, "{confidenceInterval}" provided.')

	confidenceInterval = confidenceInterval / 100.

	confidenceIntervals['mean'] = stats.norm.interval(confidenceInterval, loc=md, scale=sd/numpy.sqrt(n))

	if confidenceIntervalMethod.lower() == 'exact paired':

		coeffs = parallelCarkeetCIest(n, confidenceInterval, limitOfAgreement)

		coefInner = coeffs[0]
		coefOuter = coeffs[1]

		confidenceIntervals['upperLoA'] = (md + (coefInner * sd),
										   md + (coefOuter * sd))

		confidenceIntervals['lowerLoA'] = (md - (coefOuter * sd),
										   md - (coefInner * sd))

	elif confidenceIntervalMethod.lower() == 'approximate':

		seLoA = ((1/n) + (limitOfAgreement**2 / (2 * (n - 1)))) * (sd**2)
		loARange = numpy.sqrt(seLoA) * stats.t._ppf((1-confidenceInterval)/2., n-1)

		confidenceIntervals['upperLoA'] = ((md + limitOfAgreement*sd) + loARange,
										   (md + limitOfAgreement*sd) - loARange)

		confidenceIntervals['lowerLoA'] = ((md - limitOfAgreement*sd) + loARange,
										   (md - limitOfAgreement*sd) - loARange)

	else:
		raise NotImplementedError(f"'{confidenceIntervalMethod}' is not an valid method of calculating confidance intervals")
	
	return confidenceIntervals


##
# Split out so we can mock the return value in testing
# (and ProcessPoolExecutor & mock do not play well togther so we can't mock carkeetCIest)
##
def parallelCarkeetCIest(n, confidenceInterval, limitOfAgreement): # pragma: no cover
	coeffs = []
	with ProcessPoolExecutor(max_workers=2) as executor:
		for result in executor.map(carkeetCIest, repeat(n), [(1 - confidenceInterval) / 2., 1 - (1 - confidenceInterval) / 2.], repeat(limitOfAgreement)):
			coeffs.append(result)
	return coeffs
