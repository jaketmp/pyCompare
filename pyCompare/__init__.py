"""
`pyCompare` implements functions for generating Bland-Altman plots of agreement between measurements.
"""
import os

from ._plotBlandAltman import blandAltman

path = os.path.realpath(__file__)
path = os.path.dirname(path)
path = os.path.join(path, 'VERSION')

with open(path, 'r') as file:
	__version__ = file.readline().strip()

__all__ = ['blandAltman']
