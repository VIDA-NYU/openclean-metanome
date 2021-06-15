# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

from typing import Dict, Optional

import os
import pandas as pd
import shutil
import tempfile

from flowserv.controller.serial.workflow.base import SerialWorkflow
from flowserv.controller.serial.workflow.result import RunResult
from flowserv.controller.worker.manager import WorkerPool
from flowserv.volume.fs import FStore
from flowserv.volume.manager import VolumeManager, DEFAULT_STORE


"""Names for input and output files for the Metanome algorithms."""
DATA_FILE = os.path.join('data', 'table.csv')
RESULT_FILE = os.path.join('data', 'results.json')


# -- Helper Methods -----------------------------------------------------------

def run_workflow(
    workflow: SerialWorkflow, arguments: Dict, df: pd.DataFrame,
    worker: Optional[Dict] = None, volume: Optional[Dict] = None,
    managers: Optional[Dict] = None, verbose: Optional[bool] = True
) -> RunResult:
    """Run a given workflow representing a Metanome profiling algorithm on the
    given data frame.

    Returns the run result. If execution of the Metanome algorithm fails a
    RuntimeError will be raised.

    This implementation assumes that all algorithms operate on a single input
    file that contains a serialization of the data frame and that they all
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
    worker: dict, default=None
        Optional configuration for the main worker.
    volume: dict, default=None
        Optional configuration for the volume that is associated with the main
        worker.
    managers: dict, default=None
        Mapping of workflow step identifier to the worker that is used to
        execute them.
    verbose: bool, default=True
        Output run logs if True.

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
    # Create a copy of the workflow-specific arguments and add the data frame
    # and the input and output files.
    args = dict(arguments)
    args['df'] = df
    args['inputfile'] = DATA_FILE
    args['outputfile'] = RESULT_FILE
    # Create factory objects for storage volumes.
    stores = [FStore(basedir=rundir, identifier=DEFAULT_STORE)]
    if volume:
        stores.append(volume)
    volumes = VolumeManager(stores=stores, files=[])
    # Create factory for workers. Include mapping of workflow steps to
    # the worker that are responsible for their execution.
    workers = WorkerPool(workers=[worker] if worker else [], managers=managers)
    # Run the workflow and return the result. Make sure to cleanup the temporary
    # run filder. This assumes that the workflow steps have read any output
    # file into main memory or copied it to a target destination.
    try:
        r = workflow.run(arguments=args, workers=workers, volumes=volumes)
        # Output STDOUT and STDERR before raising a potential error.
        if verbose:
            for line in r.log:
                print(line)
        # Raise error if run execution was not successful.
        r.raise_for_status()
        return r
    finally:
        # Remove the created run directory.
        shutil.rmtree(rundir)
