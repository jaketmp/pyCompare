from setuptools import setup, find_packages

setup(name='pyCompare',
	version='1.0.0',
	description='Bland-Altman plots for Python',
	url='https://github.com/jaketmp/pyCompare',
	author='Jake TM Pearce',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'numpy>=1.11.0',
		'scipy>=0.17.1',
		'matplotlib>=1.5.1',
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

		""",
		documentation='https://github.com/jaketmp/pyCompare',
		include_package_data=True,
		zip_safe=True
	)
