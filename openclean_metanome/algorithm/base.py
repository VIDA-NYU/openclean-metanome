# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

from typing import Dict

import os
import pandas as pd
import shutil
import tempfile

from flowserv.controller.serial.workflow.base import SerialWorkflow
from flowserv.controller.serial.workflow.result import RunResult

import openclean_metanome.config as config


"""Names for input and output files for the Metanome algorithms."""
IN_FILE = 'table.csv'
OUT_FILE = 'results.json'


# -- Helper Methods -----------------------------------------------------------

def run_workflow(workflow: SerialWorkflow, arguments: Dict, df: pd.DataFrame) -> RunResult:
    """Run a given workflow representing a Metanome profiling algorithm on the
    given data frame.

    Returns the run result. If execution of the Metanome algorithm fails a
    RuntimeError will be raised.

    This implementation assumes that all algorithms operate on a single input
    file that contains a serializatio of the data frame and that they all
    produce a single output file in Json format.

    Parameters
    ----------
    workflow: flowserv.controller.serial.workflow.base.SerialWorkflow
        Serial workflow to run a Metanome profiling algorithm on a given data
        frame.
    arguments: dict
        Dictionary of algorithm-specific input arguments.
    df: pd.DataFrame
        Input data frame.

    Returns
    -------
    flowserv.controller.serial.workflow.result.RunResult
    """
    # Create a temporary run directory for input and output files.
    rundir = tempfile.mkdtemp()
    # Create a subfolder for input and output files. This is important when
    # running the workflow in a Docker container since these folders will
    # be mounted automatically as volumes into the container to provide
    # access to the files.
    os.makedirs(os.path.join(rundir, 'data'))
    # Create a copy of the static arguments and add the data frame and the input
    # and output files.
    args = dict(arguments)
    args['df'] = df
    args['inputfile'] = os.path.join('data', IN_FILE)
    args['outputfile'] = os.path.join('data', OUT_FILE)
    try:
        r = workflow.run(arguments=args, workers=config.WORKERS(), rundir=rundir)
        r.raise_for_status()
        return r
    finally:
        # Remove the created run directory.
        shutil.rmtree(rundir)
