import numpy
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.ticker as ticker
from scipy import stats
import warnings

from ._rangeFrameLocator import rangeFrameLocator
from ._carkeetCIest import carkeetCIest


def blandAltman(data1, data2, limitOfAgreement=1.96, confidenceInterval=95, confidenceIntervalMethod='exact paired', detrend=None, title=None, figureSize=(10,7), dpi=72, savePath=None, figureFormat='png'):
	"""
	blandAltman(data1, data2, limitOfAgreement=1.96, confidenceInterval=None, **kwargs)

	Generate a Bland-Altman [#]_ [#]_ plot to compare two sets of measurements of the same value.

	Confidence intervals on the limit of agreement may be calculated using:
	- 'exact paired' uses the exact paired method described by Carkeet [#]_
	- 'approximate' uses the approximate method described by Bland & Altman

	The exact paired method will give more accurate results when the number of paired measurements is low (approx < 100), at the expense of much slower plotting time.

	The *detrend* option supports the following options:
	- ``None`` do not attempt to detrend data - plots raw values
	- 'Linear' attempt to model and remove a multiplicative offset between each assay by linear regression

	:param data1: First measurement
	:type data1: list like
	:param data1: Second measurement
	:type data1: list like
	:param float limitOfAgreement: Multiple of the standard deviation to plot limit of agreement bounds at (defaults to 1.96)
	:param confidenceInterval: If not ``None``, plot the specified percentage confidence interval on the mean and limits of agreement
	:param str confidenceIntervalMethod: Method used to calculated confidence interval on the limits of agreement
	:type confidenceInterval: None or float
	:param detrend: If not ``None`` attempt to 
	:type detrend: None or str

	.. [#] Altman, D. G., and Bland, J. M. “Measurement in Medicine: The Analysis of Method Comparison Studies” Journal of the Royal Statistical Society. Series D (The Statistician), vol. 32, no. 3, 1983, pp. 307–317. `JSTOR <https://www.jstor.org/stable/2987937>`_.
	.. [#] Altman, D. G., and Bland, J. M. “Measuring agreement in method comparison studies” Statistical Methods in Medical Research, vol. 8, no. 2, 1999, pp. 135–160. `DOI <https://doi.org/10.1177/096228029900800204>`_.
	.. [#] Carkeet, A. "Exact Parametric Confidence Intervals for Bland-Altman Limits of Agreement" Optometry and Vision Science, vol. 92, no 3, 2015, pp. e71–e80 `DOI <https://doi.org/10.1097/OPX.0000000000000513>`_.
	"""
	if not limitOfAgreement > 0:
		raise ValueError('"limitOfAgreement" must be a number greater than zero.') 

	fig, ax = plt.subplots(figsize=figureSize, dpi=dpi)

	if detrend is None:
		pass
	elif detrend.lower() == 'linear':
		reg = stats.linregress(data1, data2)

		data2 = data2 / reg.slope

	else:
		raise NotImplementedError("'%s' is not a valid detrending method." % (detrend))


	mean = numpy.mean([data1, data2], axis=0)
	diff = data1 - data2
	md = numpy.mean(diff)
	sd = numpy.std(diff, axis=0)

	if confidenceInterval:

		if (confidenceInterval > 99.9) | (confidenceInterval < 1):
			raise ValueError('"confidenceInterval" must be a number in the range 1 to 99.')

		n = len(diff)

		confidenceInterval = confidenceInterval / 100.
		
		confidenceIntervalMean = stats.norm.interval(confidenceInterval, loc=md, scale=sd/numpy.sqrt(n))

		ax.axhspan(confidenceIntervalMean[0],
				   confidenceIntervalMean[1],
				   facecolor='#6495ED', alpha=0.2)

		if confidenceIntervalMethod.lower() == 'exact paired':
			coefInner = carkeetCIest(n, (1 - confidenceInterval) / 2., limitOfAgreement)
			coefOuter = carkeetCIest(n, 1 - (1 - confidenceInterval) / 2., limitOfAgreement)

			upperLoAhigh = md + (coefOuter * sd)
			upperLoAlow = md + (coefInner * sd)

			lowerLoAhigh = md - (coefOuter * sd)
			lowerLoAlow = md - (coefInner * sd)

		elif confidenceIntervalMethod.lower() == 'approximate':

			seLoA = ((1/n) + (limitOfAgreement**2 / (2 * (n - 1)))) * (sd**2)
			loARange = numpy.sqrt(seLoA) * stats.t._ppf((1-confidenceInterval)/2., n-1)

			upperLoAhigh = (md + limitOfAgreement*sd) + loARange
			upperLoAlow = (md + limitOfAgreement*sd) - loARange

			lowerLoAhigh = (md - limitOfAgreement*sd) + loARange
			lowerLoAlow = (md - limitOfAgreement*sd) - loARange

		else:
			raise NotImplementedError("'%s' is not an implemented method of calculating confidance intervals")

		ax.axhspan(upperLoAhigh,
				   upperLoAlow,
				   facecolor='coral', alpha=0.2)

		ax.axhspan(lowerLoAhigh,
				   lowerLoAlow,
				   facecolor='coral', alpha=0.2)


	ax.scatter(mean, diff, alpha=0.5)

	ax.axhline(md, color='#6495ED', linestyle='--')
	ax.axhline(md + limitOfAgreement*sd, color='coral', linestyle='--')
	ax.axhline(md - limitOfAgreement*sd, color='coral', linestyle='--')

	trans = transforms.blended_transform_factory(
		ax.transAxes, ax.transData)

	limitOfAgreementRange = (md + (limitOfAgreement * sd)) - (md - limitOfAgreement*sd)
	offset = (limitOfAgreementRange / 100.0) * 1.5

	ax.text(0.98, md + offset, 'Mean', ha="right", va="bottom", transform=trans)
	ax.text(0.98, md - offset, '%.2f' % (md), ha="right", va="top", transform=trans)

	ax.text(0.98, md + (limitOfAgreement * sd) + offset, '+%.2f SD' % (limitOfAgreement), ha="right", va="bottom", transform=trans)
	ax.text(0.98, md + (limitOfAgreement * sd) - offset, '%.2f' % (md + limitOfAgreement*sd), ha="right", va="top", transform=trans)

	ax.text(0.98, md - (limitOfAgreement * sd) - offset, '-%.2f SD' % (limitOfAgreement), ha="right", va="top", transform=trans)
	ax.text(0.98, md - (limitOfAgreement * sd) + offset, '%.2f' % (md - limitOfAgreement*sd), ha="right", va="bottom", transform=trans)

	# Only draw spine between extent of the data
	ax.spines['left'].set_bounds(min(diff), max(diff))
	ax.spines['bottom'].set_bounds(min(mean), max(mean))

	# Hide the right and top spines
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	ax.set_ylabel('Difference between methods')
	ax.set_xlabel('Mean of methods')

	tickLocs = ax.xaxis.get_ticklocs()
	tickLocs = rangeFrameLocator(tickLocs, (min(mean), max(mean)))
	ax.xaxis.set_major_locator(ticker.FixedLocator(tickLocs))

	tickLocs = ax.yaxis.get_ticklocs()
	tickLocs = rangeFrameLocator(tickLocs, (min(diff), max(diff)))
	ax.yaxis.set_major_locator(ticker.FixedLocator(tickLocs))

	ax.patch.set_alpha(0)

	if detrend is None:
		pass
	elif detrend.lower() == 'linear':
		plt.text(1, -0.1, 'Slope correction factor: %.2f ± %.2f' % (reg.slope, reg.stderr), ha='right', transform=ax.transAxes)

	if title:
		ax.set_title(title)

	##
	# Save or draw
	##
	if savePath:
		fig.savefig(savePath, format=figureFormat, dpi=dpi)
		plt.close()
	else:
		plt.show()
