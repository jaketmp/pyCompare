from setuptools import setup, find_packages
import os

basepath = os.path.realpath(__file__)
basepath = os.path.dirname(basepath)
path = os.path.join(basepath, 'pyCompare', 'VERSION')

with open(path, 'r') as file:
	VERSION = file.readline().strip()

path = os.path.join(basepath, 'README.md')

with open(path, 'r') as file:
	README = file.read()

setup(name='pyCompare',
	version=VERSION,
	description='Bland-Altman plots for Python',
	url='https://github.com/jaketmp/pyCompare',
	author='Jake TM Pearce',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'numpy>=1.18.1',
		'scipy>=1.0.1',
		'matplotlib>=3.0.2',
	],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Visualization",
		],
	long_description_content_type='text/markdown',
	long_description = README,
	documentation='https://github.com/jaketmp/pyCompare',
	include_package_data=True,
	zip_safe=True
	)
