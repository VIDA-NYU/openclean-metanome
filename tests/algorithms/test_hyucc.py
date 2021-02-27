# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the HyUCC algorithm wrapper."""

from collections import namedtuple

import json
import os
import pytest
import subprocess

from openclean_metanome.algorithm.hyucc import hyucc


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
        doc = {'columnCombinations': [['COL1'], ['COL0', 'COL2']]}
        with open(outputfile, 'w') as f:
            json.dump(doc, f)
        return Proc(returncode=0, stdout=b'', stderr=b'')

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_hyucc_algorithm_success(mock_subprocess, dataset):
    """Test the main functionality of the HyUCC wrapper using the test
    engine.
    """
    keys = hyucc(df=dataset)
    assert len(keys) == 2
    results = list()
    for ucc in keys:
        results.append(set([c.colid for c in ucc]))
    assert {2} in results
    assert {1, 3} in results
