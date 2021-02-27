# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the HyFD algorithm wrapper."""

from collections import namedtuple

import json
import os
import pytest
import subprocess

from openclean_metanome.algorithm.hyfd import hyfd


# -- Patching for subprocess step execution -----------------------------------

Proc = namedtuple('Proc', ['returncode', 'stdout', 'stderr'])


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Run container step for hyfd algorithm."""
    def mock_run(*args, **kwargs):
        rundir = kwargs['cwd']
        inputfile = os.path.join(rundir, args[0].split()[5][1:-1])
        if not os.path.isfile(inputfile):
            raise ValueError('file {} not found'.format(inputfile))
        outputfile = os.path.join(rundir, args[0].split()[7][1:-1])
        doc = {'functionalDependencies': [
            {'lhs': ['COL0', 'COL1'], 'rhs': 'COL2'},
            {'lhs': ['COL1'], 'rhs': 'COL0'}
        ]}
        with open(outputfile, 'w') as f:
            json.dump(doc, f)
        return Proc(returncode=0, stdout=b'', stderr=b'')

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_hyfd_algorithm_success(mock_subprocess, dataset):
    """Test the main functionality of the HyFD wrapper using the test
    engine.
    """
    fds = hyfd(df=dataset)
    assert len(fds) == 2
    results = list()
    for fd in fds:
        lhs = set([c.colid for c in fd.lhs])
        rhs = set([c.colid for c in fd.rhs])
        results.append([lhs, rhs])
    assert [{1, 2}, {3}] in results
    assert [{2}, {1}] in results
