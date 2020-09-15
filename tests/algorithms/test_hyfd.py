# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the HyFD algorithm wrapper."""

import pytest

from openclean_metanome.algorithm.hyfd import hyfd, HyFD
from openclean_metanome.engine.tests import MetanomeTestEngine
from openclean_metanome.error import MetanomeError


def test_hyfd_algorithm_error(dataset):
    """Test error case for HyFD wrapper."""
    algo = HyFD(engine=MetanomeTestEngine())
    with pytest.raises(MetanomeError):
        algo.run(dataset)


def test_hyfd_algorithm_success(dataset):
    """Test the main functionality of the HyFD wrapper using the test
    engine.
    """
    result = {'functionalDependencies': [
        {'lhs': ['COL0', 'COL1'], 'rhs': ['COL2']},
        {'lhs': ['COL1'], 'rhs': ['COL2']}
    ]}
    algo = HyFD(engine=MetanomeTestEngine(result=result))
    fds = algo.run(dataset)
    assert len(fds) == 2
    results = list()
    for fd in fds:
        lhs = set([c.colid for c in fd.lhs])
        rhs = set([c.colid for c in fd.rhs])
        results.append([lhs, rhs])
    assert [{1, 2}, {3}] in results
    assert [{2}, {3}] in results


def test_hyfd_routine(dataset):
    """Test running the  HyFD wrapper using the single execution routine."""
    result = {'functionalDependencies': [{
        'rhs': ['COL1'],
        'lhs': ['COL0', 'COL2']
    }]}
    fds = hyfd(df=dataset, engine=MetanomeTestEngine(result=result))
    assert len(fds) == 1
    assert fds[0].lhs == {'A', 'C'}
    assert fds[0].rhs == {'B'}
