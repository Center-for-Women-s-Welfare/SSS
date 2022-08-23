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
    install_requires= ["pandas", "numpy", "setuptools_scm", "sqlalchemy"],
    extras_require={
        "doc": ["sphinx", "pypandoc"],
        "dev": ["coverage", "sphinx", "pypandoc", "pytest", "pytest-cov"],
    }
)


if __name__ == "__main__":
    setup(**opts)