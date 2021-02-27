# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for version string (for completeness)."""

from openclean_metanome.version import __version__


def test_version_string(tmpdir):
    """Ensure that version string is defined."""
    assert __version__ is not None
