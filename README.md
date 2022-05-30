# pyCompare <img src="https://github.com/jaketmp/pyCompare/raw/main/docs/_static/pyCompare.png" width="200" style="max-width: 30%;" align="right" />

[![Build Status](https://github.com/jaketmp/pyCompare/actions/workflows/python-test.yml/badge.svg)](https://github.com/jaketmp/pyCompare/actions) [![codecov](https://codecov.io/gh/jaketmp/pyCompare/branch/main/graph/badge.svg)](https://codecov.io/gh/jaketmp/pyCompare) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyCompare.svg) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1238915.svg)](https://doi.org/10.5281/zenodo.1238915) [![PyPI](https://img.shields.io/pypi/v/pyCompare.svg)](https://pypi.org/project/pyCompare/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jaketmp/pyCompare/main?filepath=pyCompare-Demo.ipynb)



A Python module for generating [Bland-Altman](https://en.wikipedia.org/wiki/Bland–Altman_plot) plots to compare two sets of measurements.

You can try out the code using [Binder](https://mybinder.org/v2/gh/jaketmp/pyCompare/main?filepath=pyCompare-Demo.ipynb).

<img src="https://github.com/jaketmp/pyCompare/raw/main/docs/_static/bland_altman.png" style="max-width: 60%;" align="center" />

## Installation

To install _via_ [pip](https://pypi.org/project/pyCompare/), run:

    pip install pyCompare

Installation with pip allows the usage of the uninstall command:

    pip uninstall pyCompare


## Documentation

See [the example notebook](pyCompare-Demo.ipynb) (or the interactive version on [Binder](https://mybinder.org/v2/gh/jaketmp/pyCompare/main?filepath=pyCompare-Demo.ipynb)) for detailed examples of all the options. 

    blandAltman(data1, data2,
                limitOfAgreement=1.96,
                confidenceInterval=95,
                confidenceIntervalMethod='approximate',
                detrend=None,
                percentage=False,
                **kwargs)

Generate a Bland-Altman plot to compare two sets of measurements of the same value.

Paired measurmentes from each set should be passed in `data1` and `data2` with each containing a list of values from one of the methods.

The range of the limits of agreement is 1.96 by default, and can be customised with the `limitOfAgreement=` argument.

By default confidance intervals are plotted over the 95% range, this can be customised to the *x*% range by passing the argument `confidenceInterval=x` or removed with `confidenceInterval=None`.

There are two options for plotting confidence intervals on the mean difference and limit of agreement:
- [default] 'approximate' uses the approximate method described by Bland & Altman
- 'exact paired' uses the exact paired method described by Carkeet

The 'exact paired' method will give more accurate confidence intervals on the limits of agreement when the number of paired measurements is low (approx < 100), at the expense of a much slower plotting time.

A multiplicative offset between the two measures can be modeled with the *detrend=* argument, which supports the following options:
- [default] `None` do not attempt to detrend data - plots the raw values
- 'Linear' attempt to model and remove a multiplicative offset between each assay by linear regression
- 'ODR' attempt to model and remove a multiplicative offset between each assay by orthogonal distance regression

'ODR' is the recommended method if you do not use `None`.

If passed as `True`, the `percentage=` argument plots the percentage difference between measures, instead of the units the methods were measured in.

Plots are displayed using the current matplotlib backend by default, or may be saved with the `savePath=` argument.

When saving, png format graphics are saved by default:

    blandAltman(data1, data2,
                savePath='SavedFigure.png')

The save format type can be chosen from those known by [matplotlib](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html) with the `figureFormat=` argument:

    blandAltman(data1, data2,
                savePath='SavedFigure.svg',
                figureFormat='svg)

### Full list of arguments

**blandAltman(data1, data2)**

* **data1** (*list like*) – List of values from the first method
* **data2** (*list like*) – List of paired values from the second method
* **limitOfAgreement** (*float*) – Multiple of the standard deviation to plot limit of agreement bounds at (defaults to 1.96)
* **confidenceInterval** (*None** or **float*) – If not `None`, plot the specified percentage confidence interval on the mean and limits of agreement
* **confidenceIntervalMethod** (*str*) – Method used to calculated confidence interval on the limits of agreement
* **detrend** (*None** or **str*) – If not `None` attempt to detrend by the method specified
* **percentage** (*bool*) – If `True`, plot differences as percentages (instead of in the units the data sources are in)
* **title** (*str*) – Title text for the figure
* **ax** (*matplotlib.axes._subplots.AxesSubplot*) – Matplotlib axis handle - if not None draw into this axis rather than creating a new figure
* **figureSize** (*(**float**, **float**)*) – Figure size as a tuple of (width, height) in inches
* **dpi** (*int*) – Figure resolution
* **savePath** (*str*) – If not `None`, save figure at this path
* **figureFormat** (*str*) – When saving figure use this format
* **meanColour** (*str*) – Colour to use for plotting the mean difference
* **loaColour** (*str*) – Colour to use for plotting the limits of agreement
* **pointColour** (*str*) – Colour for plotting data points


#### References

To cite `pyCompare`, use the Zendo DOI: [10.5281/zenodo.1238915](https://doi.org/10.5281/zenodo.1238915).

- Altman, D. G., and Bland, J. M. “Measurement in Medicine: The Analysis of Method Comparison Studies” Journal of the Royal Statistical Society. Series D (The Statistician), vol. 32, no. 3, 1983, pp. 307–317. [JSTOR](https://www.jstor.org/stable/2987937).
- Altman, D. G., and Bland, J. M. “Measuring agreement in method comparison studies” Statistical Methods in Medical Research, vol. 8, no. 2, 1999, pp. 135–160. [DOI](https://doi.org/10.1177/096228029900800204).
- Carkeet, A. "Exact Parametric Confidence Intervals for Bland-Altman Limits of Agreement" Optometry and Vision Science, vol. 92, no 3, 2015, pp. e71–e80 [DOI](https://doi.org/10.1097/OPX.0000000000000513).
