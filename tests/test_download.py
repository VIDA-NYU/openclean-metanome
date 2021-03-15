# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the jar-file download."""

from pathlib import Path

import os
import pytest

import openclean_metanome.download as download


@pytest.fixture
def mock_download(monkeypatch):
    """Mock file download."""
    def mock_download_file(*args, **kwargs):
        Path(kwargs['dst']).touch()

    monkeypatch.setattr(download, "download_file", mock_download_file)


@pytest.mark.parametrize('verbose', [True, False])
def test_download_jar(mock_download, tmpdir, verbose):
    """Test downloading the jar-file to a given destination folder. Mocks the
    actual download.
    """
    dstfile = os.path.join(tmpdir, 'file.txt')
    download.download_jar(dst=dstfile, verbose=verbose)
    download.download_jar(dst=dstfile, verbose=verbose)
