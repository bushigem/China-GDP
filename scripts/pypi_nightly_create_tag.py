#!/usr/bin/env python

# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create a tag for the PYPI nightly version

Increment the version number, add a dev suffix and add todays date
"""

from datetime import datetime

import packaging.version
import pytz
from packaging.version import Version

PYPI_STREAMLIT_URL = "https://pypi.org/pypi/streamlit/json"


def get_latest_streamlit_version() -> Version:
    """Request the latest streamlit version string from PyPI.

    NB: this involves a network call, so it could raise an error
    or take a long time.

    Parameters
    ----------
    timeout : float or None
        The request timeout.

    Returns
    -------
    str
        The version string for the latest version of streamlit
        on PyPI.

    """
    import requests

    rsp = requests.get(PYPI_STREAMLIT_URL)
    try:
        version_str = rsp.json()["info"]["version"]
    except Exception as e:
        raise RuntimeError("Got unexpected response from PyPI", e)
    return Version(version_str)


def create_tag():
    """Create tag with updated version, a suffix and date."""

    # Get latest version
    current_version = get_latest_streamlit_version()

    # Update micro
    version_with_inc_micro = (
        current_version.major,
        current_version.minor,
        current_version.micro + 1,
    )

    # Append todays date
    version_with_date = (
        ".".join([str(x) for x in version_with_inc_micro])
        + ".dev"
        + datetime.now(pytz.timezone("US/Pacific")).strftime("%Y%m%d")
    )

    # Verify if version is PEP440 compliant.
    packaging.version.Version(version_with_date)

    return version_with_date


if __name__ == "__main__":
    tag = create_tag()

    # Print so we can access the tag in the shell
    print(tag)
