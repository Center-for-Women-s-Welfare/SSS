"""Initialize the sss package."""
from pathlib import Path

from importlib.metadata import version, PackageNotFoundError
from setuptools_scm import get_version

from .city import City
from .geoid import GeoID
from .sss_table import SSS, HealthCare, Miscellaneous, ARPA
from .puma import PUMA
from .report import Report
from .preprocess import std_col_names

try:
    # get accurate version for developer installs
    version_str = get_version(Path(__file__).parent.parent)

    __version__ = version_str

except (LookupError, ImportError):
    try:
        # Set the version automatically from the package details.
        __version__ = version("sss")
    except PackageNotFoundError:  # pragma: nocover
        # package is not installed
        pass
