# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Fixtures for Metanome algorithm unit tests."""

import pandas as pd
import pytest

from openclean.data.types import Column


@pytest.fixture
def dataset():
    """Simple pandas data frame with one row and three columns."""
    return pd.DataFrame(
        data=[[1, 2, 3]],
        columns=[
            Column(colid=1, name='A'),
            Column(colid=2, name='B'),
            Column(colid=3, name='C')
        ]
    )
