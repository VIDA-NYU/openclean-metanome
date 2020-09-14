# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for run argument wrappers."""

from openclean_metanome.engine.arguments import File, String


def test_file_arguments():
    """Test the wrapper classes for file arguments."""
    f = File('abc')
    assert f.is_file()
    assert not f.is_string()
    assert f.value == 'abc'
    assert str(f) == 'abc'


def test_string_arguments():
    """Test the wrapper classes for string arguments."""
    f = String('xyz')
    assert not f.is_file()
    assert f.is_string()
    assert f.value == 'xyz'
    assert str(f) == 'xyz'
