import sys
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(
    name='sss',
    description='Designing Self-Sufficiency Standard Database',
    #long_description=LONG_DESCRIPTION, 
    url='https://github.com/Center-for-Women-s-Welfare/SSS',
    license='CC0 1.0',
    #classifiers=CLASSIFIERS,
    author='Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton',
    use_scm_version=True,
    packages=PACKAGES,
    include_package_data=True,
    install_requires= ['sqlalchemy', 'pandas', 'numpy', "setuptools_scm"]
)


if __name__ == '__main__':
    setup(**opts)