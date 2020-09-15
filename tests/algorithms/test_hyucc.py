# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the HyUCC algorithm wrapper."""

import pandas as pd
import pytest

from openclean.data.column import Column
from openclean_metanome.algorithm.hyucc import HyUCC
from openclean_metanome.engine.tests import MetanomeTestEngine
from openclean_metanome.error import MetanomeError


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


def test_hyucc_algorithm_error(dataset):
    """Test error case for HyUCC wrapper."""
    hyucc = HyUCC(engine=MetanomeTestEngine())
    with pytest.raises(MetanomeError):
        hyucc.run(dataset)


def test_hyucc_algorithm_success(dataset):
    """Test the main functionality of the HyUCC wrapper using the test
    engine.
    """
    result = {'columnCombinations': [['COL1'], ['COL0', 'COL2']]}
    hyucc = HyUCC(engine=MetanomeTestEngine(result=result))
    keys = hyucc.run(dataset)
    assert len(keys) == 2
    results = list()
    for ucc in keys:
        results.append(set([c.colid for c in ucc]))
    assert {2} in results
    assert {1, 3} in results
