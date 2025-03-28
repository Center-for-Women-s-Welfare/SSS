"""Initialize the sss package."""

import contextlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from setuptools_scm import get_version

from .city import City
from .geoid import GeoID
from .puma import PUMA
from .report import Report
from .sss_table import ARPA, SSS, HealthCare, Miscellaneous

try:
    # get accurate version for developer installs
    # must point to folder that contains the .git file!
    version_str = get_version(Path(__file__).parent.parent.parent)

    __version__ = version_str

except (LookupError, ImportError):
    with contextlib.suppress(PackageNotFoundError):
        # Set the version automatically from the package details.
        __version__ = version("sss")

__all__ = [
    "SSS",
    "ARPA",
    "HealthCare",
    "Miscellaneous",
    "City",
    "GeoID",
    "PUMA",
    "Report",
]
