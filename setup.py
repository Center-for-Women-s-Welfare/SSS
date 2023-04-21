import sys
import os
from setuptools import setup, find_namespace_packages

opts = dict(
    name="sss",
    description="Designing Self-Sufficiency Standard Database",
    #long_description=LONG_DESCRIPTION, 
    url="https://github.com/Center-for-Women-s-Welfare/SSS",
    license="CC0 1.0",
    #classifiers=CLASSIFIERS,
    author="Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton",
    package_dir={"sss": "sss"},
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires= [
        "numpy>=1.21",
        "openpyxl>=3.1.0,!=3.1.1",
        "pandas>=1.5.0",
        "pyxlsb>=1.0.8",
        "setuptools_scm>=7.0.3",
        "sqlalchemy>=1.4.16"
    ],
    extras_require={
        "doc": ["sphinx", "pypandoc"],
        "dev": ["coverage", "sphinx", "pypandoc", "pytest", "pytest-cov"],
    }
)


if __name__ == "__main__":
    setup(**opts)