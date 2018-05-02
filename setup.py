from setuptools import setup, find_packages

setup(name='pyCompare',
	version='1.1.0',
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
		.. image:: https://travis-ci.org/jaketmp/pyCompare.svg?branch=master
		   :target: https://travis-ci.org/jaketmp/pyCompare
		   :alt: Travis CI build status

		.. image:: https://codecov.io/gh/jaketmp/pyCompare/branch/master/graph/badge.svg
		   :target: https://codecov.io/gh/jaketmp/pyCompare
		   :alt: Test coverage

		.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1238916.svg
		   :target: https://doi.org/10.5281/zenodo.1238916
		   :alt: Zenodo DOI

		A Python module for generating `Bland-Altman <https://en.wikipedia.org/wiki/Bland–Altman_plot>`_ plots to compare two sets of measurements.

		For documentation see the `project page <https://github.com/jaketmp/pyCompare>` on GitHub.
		""",
	documentation='https://github.com/jaketmp/pyCompare',
	include_package_data=True,
	zip_safe=True
	)
