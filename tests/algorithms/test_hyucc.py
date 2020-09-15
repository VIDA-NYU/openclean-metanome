# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the HyUCC algorithm wrapper."""

import pytest

from openclean_metanome.algorithm.hyucc import hyucc, HyUCC
from openclean_metanome.engine.tests import MetanomeTestEngine
from openclean_metanome.error import MetanomeError


def test_hyucc_algorithm_error(dataset):
    """Test error case for HyUCC wrapper."""
    algo = HyUCC(engine=MetanomeTestEngine())
    with pytest.raises(MetanomeError):
        algo.run(dataset)


def test_hyucc_algorithm_success(dataset):
    """Test the main functionality of the HyUCC wrapper using the test
    engine.
    """
    result = {'columnCombinations': [['COL1'], ['COL0', 'COL2']]}
    algo = HyUCC(engine=MetanomeTestEngine(result=result))
    keys = algo.run(dataset)
    assert len(keys) == 2
    results = list()
    for ucc in keys:
        results.append(set([c.colid for c in ucc]))
    assert {2} in results
    assert {1, 3} in results


def test_hyucc_routine(dataset):
    """Test running the  HyUCC wrapper using the single execution routine."""
    result = {'columnCombinations': [['COL1'], ['COL0', 'COL2']]}
    keys = hyucc(df=dataset, engine=MetanomeTestEngine(result=result))
    assert len(keys) == 2
