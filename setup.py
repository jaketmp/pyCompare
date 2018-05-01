from setuptools import setup, find_packages

setup(name='pyCompare',
	version='1.0.0',
	description='Bland-Altman plots for Python',
	url='https://github.com/jaketmp/pyCompare',
	author='Jake TM Pearce',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'numpy>=1.14.2',
		'scipy>=1.0.1',
		'matplotlib>=2.2.2',
	],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.6",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Visualization",
		],
	long_description = """\
		A Python module to generate `Bland-Altman <https://en.wikipedia.org/wiki/Bland–Altman_plot>`_ plots to compare two measurements.

		::
		    blandAltman(data1, data2, limitOfAgreement=1.96, confidenceInterval=None, confidenceIntervalMethod='exact paired', detrend=None, **kwargs)

		Generate a Bland-Altman [#]_ [#]_ plot to compare two sets of measurements of the same value.

		`data1` and `data2` should be 1D numpy arrays of equal length containing the paired measurements.

		Confidence intervals on the limit of agreement may be calculated using:
		- 'exact paired' uses the exact paired method described by Carkeet [#]_
		- 'approximate' uses the approximate method described by Bland & Altman

		The exact paired method will give more accurate results when the number of paired measurements is low (approx < 100), at the expense of much slower plotting time.

		The *detrend* option supports the following options:
		- ``None`` do not attempt to detrend data - plots raw values
		- 'Linear' attempt to model and remove a multiplicative offset between each assay by linear regression

		.. [#] Altman, D. G., and Bland, J. M. “Measurement in Medicine: The Analysis of Method Comparison Studies” Journal of the Royal Statistical Society. Series D (The Statistician), vol. 32, no. 3, 1983, pp. 307–317. `JSTOR <https://www.jstor.org/stable/2987937>`_.
		.. [#] Altman, D. G., and Bland, J. M. “Measuring agreement in method comparison studies” Statistical Methods in Medical Research, vol. 8, no. 2, 1999, pp. 135–160. `DOI <https://doi.org/10.1177/096228029900800204>`_.
		.. [#] Carkeet, A. "Exact Parametric Confidence Intervals for Bland-Altman Limits of Agreement" Optometry and Vision Science, vol. 92, no 3, 2015, pp. e71–e80 `DOI <https://doi.org/10.1097/OPX.0000000000000513>`_.
		
		""",
		documentation='https://github.com/jaketmp/pyCompare',
		include_package_data=True,
		zip_safe=True
	)
