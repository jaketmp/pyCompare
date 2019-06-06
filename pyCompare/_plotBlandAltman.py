import numpy
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.ticker as ticker
import warnings

from ._rangeFrameLocator import rangeFrameLocator
from ._detrend import detrend as detrendFun
from ._calculateConfidenceIntervals import calculateConfidenceIntervals

def blandAltman(data1, data2, limitOfAgreement=1.96, confidenceInterval=95, confidenceIntervalMethod='approximate', detrend=None, title=None, figureSize=(10,7), dpi=72, savePath=None, figureFormat='png', meanColour='#6495ED', loaColour='coral', pointColour='#6495ED'):
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
	- 'ODR' attempt to model and remove a multiplicative offset between each assay by Orthogonal distance regression

	:param data1: First measurement
	:type data1: list like
	:param data1: Second measurement
	:type data1: list like
	:param float limitOfAgreement: Multiple of the standard deviation to plot limit of agreement bounds at (defaults to 1.96)
	:param confidenceInterval: If not ``None``, plot the specified percentage confidence interval on the mean and limits of agreement
	:param str confidenceIntervalMethod: Method used to calculated confidence interval on the limits of agreement
	:type confidenceInterval: None or float
	:param detrend: If not ``None`` attempt to detrend by the method specified
	:type detrend: None or str
	:param str title: Title text
	:param figureSize: Figure size as a tuple of (width, height) in inches
	:type figureSize: (float, float)
	:param int dpi: Figure resolution
	:param str savePath: If not ``None``, save figure at this path
	:param str figureFormat: When saving figure use this format
	:param str meanColour: Colour to use for plotting the mean difference
	:param str loaColour: Colour to use for plotting the limits of agreement
	:param str pointColour: Colour for plotting data points

	.. [#] Altman, D. G., and Bland, J. M. “Measurement in Medicine: The Analysis of Method Comparison Studies” Journal of the Royal Statistical Society. Series D (The Statistician), vol. 32, no. 3, 1983, pp. 307–317. `JSTOR <https://www.jstor.org/stable/2987937>`_.
	.. [#] Altman, D. G., and Bland, J. M. “Measuring agreement in method comparison studies” Statistical Methods in Medical Research, vol. 8, no. 2, 1999, pp. 135–160. `DOI <https://doi.org/10.1177/096228029900800204>`_.
	.. [#] Carkeet, A. "Exact Parametric Confidence Intervals for Bland-Altman Limits of Agreement" Optometry and Vision Science, vol. 92, no 3, 2015, pp. e71–e80 `DOI <https://doi.org/10.1097/OPX.0000000000000513>`_.
	"""
	if not limitOfAgreement > 0:
		raise ValueError('"limitOfAgreement" must be a number greater than zero.') 

	# Try to coerce variables to numpy arrays
	data1 = numpy.asarray(data1)
	data2 = numpy.asarray(data2)

	data2, slope, slopeErr = detrendFun(detrend, data1, data2)

	mean = numpy.mean([data1, data2], axis=0)
	diff = data1 - data2
	md = numpy.mean(diff)
	sd = numpy.std(diff, axis=0)

	if confidenceInterval:
		confidenceIntervals = calculateConfidenceIntervals(md, sd, len(diff), limitOfAgreement, confidenceInterval, confidenceIntervalMethod)

	else:
		confidenceIntervals = dict()

	_drawBlandAltman(mean, diff, md, sd,
					 limitOfAgreement,
					 confidenceIntervals,
					 (detrend, slope, slopeErr),
					 title,
					 figureSize,
					 dpi,
					 savePath,
					 figureFormat,
					 meanColour,
					 loaColour,
					 pointColour)


def _drawBlandAltman(mean, diff, md, sd, limitOfAgreement, confidenceIntervals, detrend, title, figureSize, dpi, savePath, figureFormat, meanColour, loaColour, pointColour):
	"""
	Sub function to draw the plot.
	"""
	fig, ax = plt.subplots(figsize=figureSize, dpi=dpi)

	##
	# Plot CIs if calculated
	##
	if 'mean' in confidenceIntervals.keys():
		ax.axhspan(confidenceIntervals['mean'][0],
				   confidenceIntervals['mean'][1],
				   facecolor=meanColour, alpha=0.2)

	if 'upperLoA' in confidenceIntervals.keys():
		ax.axhspan(confidenceIntervals['upperLoA'][0],
				   confidenceIntervals['upperLoA'][1],
				   facecolor=loaColour, alpha=0.2)

	if 'lowerLoA' in confidenceIntervals.keys():
		ax.axhspan(confidenceIntervals['lowerLoA'][0],
				   confidenceIntervals['lowerLoA'][1],
				   facecolor=loaColour, alpha=0.2)

	##
	# Plot the mean diff and LoA
	##
	ax.axhline(md, color=meanColour, linestyle='--')
	ax.axhline(md + limitOfAgreement*sd, color=loaColour, linestyle='--')
	ax.axhline(md - limitOfAgreement*sd, color=loaColour, linestyle='--')

	##
	# Plot the data points
	##
	ax.scatter(mean, diff, alpha=0.5, c=pointColour)

	trans = transforms.blended_transform_factory(
		ax.transAxes, ax.transData)

	limitOfAgreementRange = (md + (limitOfAgreement * sd)) - (md - limitOfAgreement*sd)
	offset = (limitOfAgreementRange / 100.0) * 1.5

	ax.text(0.98, md + offset, 'Mean', ha="right", va="bottom", transform=trans)
	ax.text(0.98, md - offset, f'{md:.2f}', ha="right", va="top", transform=trans)

	ax.text(0.98, md + (limitOfAgreement * sd) + offset, f'+{limitOfAgreement:.2f} SD', ha="right", va="bottom", transform=trans)
	ax.text(0.98, md + (limitOfAgreement * sd) - offset, f'{md + limitOfAgreement*sd:.2f}', ha="right", va="top", transform=trans)

	ax.text(0.98, md - (limitOfAgreement * sd) - offset, f'-{limitOfAgreement:.2f} SD', ha="right", va="top", transform=trans)
	ax.text(0.98, md - (limitOfAgreement * sd) + offset, f'{md - limitOfAgreement*sd:.2f}', ha="right", va="bottom", transform=trans)

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

	if detrend[0] is None:
		pass
	else:
		plt.text(1, -0.1, f'{detrend[0]} slope correction factor: {detrend[1]:.2f} ± {detrend[2]:.2f}', ha='right', transform=ax.transAxes)

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
