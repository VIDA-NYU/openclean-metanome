# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the converter library."""

import json
import os
import pandas as pd
import pytest

from openclean.data.column import Column
from openclean_metanome.converter import create_input, read_output


def test_create_input_file(tmpdir):
    """Test creating an input CSV file from a pandas data frame."""
    df = pd.DataFrame(
        data=[[1, None, 'a'], [2, '3', 'b,c']],
        columns=[Column(colid=1, name='A'), 'B', 'A']
    )
    filename, mapping = create_input(df)
    lines = list()
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    assert lines == ['COL0,COL1,COL2', '1,,a', '2,3,"b,c"']
    assert mapping['COL0'].colid == 1
    assert mapping['COL1'] == 'B'
    assert mapping['COL2'] == 'A'


@pytest.mark.parametrize('doc', [{'A': 1}, [1, 2, 3, 'D']])
def test_read_output(doc, tmpdir):
    """Simple test to ensure that JSON objects are read correctly by the
    read_output method.
    """
    filename = os.path.join(tmpdir, 'out.json')
    with open(filename, 'w') as f:
        json.dump(doc, f)
    assert read_output(filename) == doc
