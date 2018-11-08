import numpy
from scipy import stats

def detrend(method, data1, data2):
	"""
	Model and remove a mutiplicative offset between data1 and data2 by method

	:param method: Detrending method to use 
	:type method: None or str
	:param numpy.array data1: Array of first measures
	:param numpy.array data2: Array of second measures
	"""

	slope = slopeErr = None

	if method is None:
		pass
	elif method.lower() == 'linear':
		reg = stats.linregress(data1, data2)

		slope = reg.slope
		slopeErr = reg.stderr

		data2 = data2 / slope

	elif method.lower() == 'odr':
		from scipy import odr

		def f(B, x):
			return B[0]*x + B[1]
		linear = odr.Model(f)

		odrData = odr.Data(data1, data2, wd=1./numpy.power(numpy.std(data1),2), we=1./numpy.power(numpy.std(data2),2))

		odrModel = odr.ODR(odrData, linear, beta0=[1., 2.])

		myoutput = odrModel.run()

		slope = myoutput.beta[0]
		slopeErr = myoutput.sd_beta[0]

		data2 = data2 / slope

	else:
		raise NotImplementedError(f"'{detrend}' is not a valid detrending method.")

	return data2, slope, slopeErr
