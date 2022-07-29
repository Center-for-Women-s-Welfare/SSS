from setuptools_scm import get_version

from .sss import SSS, HealthCare, Miscellaneous, ARPA
from .preprocess import std_col_names

__version__ = get_version()

