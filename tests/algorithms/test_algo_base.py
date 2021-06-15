# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the generic algorithm execution method."""

from flowserv.controller.serial.workflow.base import SerialWorkflow
from flowserv.controller.worker.manager import Subprocess
from flowserv.volume.fs import FStore

from openclean_metanome.algorithm.base import run_workflow


def test_base_algorithm_run(dataset, tmpdir):
    """Step through base algorithm execute method with an empty workflow."""
    workflow = SerialWorkflow()
    r = run_workflow(
        workflow=workflow,
        arguments={},
        df=dataset,
        worker=Subprocess(),
        volume=FStore(basedir=str(tmpdir))
    )
    assert r.returncode is None
