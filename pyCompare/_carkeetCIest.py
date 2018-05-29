import numpy
import warnings
from scipy import stats

def carkeetCIest(n, gamma, limitOfAgreement):
	"""
	Calculate  CI intervals on the paired LoA by the Carkeet method.

	Returns the coefficient determining the (gamma x 100)% confidence interval on the on the SD x limitOfAggreement.

	Position of the limit is calculated as :math:`mean difference + (coefficient * sd of differences)`

	:param int n: Number of paired observations
	:param float gamma: Calculate coefficient for this bound
	:param float limitOfAgreement: Multiples of SD being considered
	:return: Coefficient determining the (gamma x 100)% confidence interval on the on the SD x limitOfAggreement limit
	:rtype: float
	"""

	Degf = n - 1
	gammaest = 0
	Kest = 0
	Kstep = 4
	directK = 1

	threshold = 1e-8

	p = stats.norm.cdf(limitOfAgreement) - stats.norm.cdf(- limitOfAgreement)

	while numpy.abs(gammaest - gamma) > threshold:
		Kest = Kest + Kstep
		K = Kest
		stepper = 0.05 / n
		toprange = 8 / (n**0.5) + stepper
		xdist = numpy.arange(0, toprange, stepper)
		boxes = len(xdist)
		boxes = int(numpy.round(boxes / 2 + .1)) * 2 - 1
		Prchi = numpy.zeros(boxes)
		Combpdf = numpy.zeros(boxes)
		halfgauss = numpy.exp(-(n/2) * xdist **2)
		shrinkfactor = 2 * (n/(2 * numpy.pi)) **.5

		for s in range(boxes - 1):
			xtest = xdist[s]
			startp = (0.5 + p/2)
	
			resti = stats.norm.ppf(startp) + xtest - .1
			restiprior = resti
			phigh = stats.norm.cdf(xtest + resti)
			plow = stats.norm.cdf(xtest - resti)
			pesti = phigh - plow
	
			pestiprior = pesti
			resti = resti + .11
			phigh = stats.norm.cdf(xtest + resti)
			plow = stats.norm.cdf(xtest - resti)
			pesti = phigh - plow
			perror = pesti - p
			deltap = pesti - pestiprior

			deltaresti = resti - restiprior
			newresti = resti - perror / deltap * deltaresti
			restiprior = resti

			resti = newresti

			pestiprior = pesti
			phigh = stats.norm.cdf(xtest + resti)
			plow = stats.norm.cdf(xtest - resti)
			pesti = phigh - plow

			perror = pesti - p
			while numpy.abs(perror) > 2e-15:
				deltap = pesti - pestiprior

				deltaresti = resti - restiprior
				newresti = resti - perror / deltap * deltaresti
				restiprior = resti

				resti = newresti

				pestiprior = pesti
				phigh = stats.norm.cdf(xtest + resti)
				plow = stats.norm.cdf(xtest - resti)
				pesti = phigh - plow

				perror = pesti - p

			with warnings.catch_warnings():
				warnings.simplefilter('ignore', RuntimeWarning)
				chiprob = 1 - stats.chi2.cdf((Degf * resti**2) / (K**2), Degf)
			Prchi[s] = chiprob
			Combpdf[s] = chiprob * halfgauss[s]

		Integ = 0
		for s in range(0, boxes - 2, 2):
			M = Combpdf[s+1] * stepper * 2

			T = (Combpdf[s] + Combpdf[s+2]) * stepper
			Integ = Integ + (M*2+T)/ 3 * shrinkfactor

		gammaest = Integ
		if (gammaest * directK) > (gamma * directK):
			directK = directK * -1
			Kstep = - Kstep / 2

	return Kest
