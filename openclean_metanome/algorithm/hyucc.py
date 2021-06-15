# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Wrapper to run the HyUCC algorithm (A Hybrid Approach for Efficient Unique
Column Combination Discovery) from the Metanome data profiling library. HyUCC
is a unique column combination doscovery algorithm.
"""

from typing import Dict, List, Optional

import pandas as pd

from flowserv.controller.serial.workflow.base import SerialWorkflow
from flowserv.controller.worker.manager import WORKER_ID
from openclean.data.types import Columns
from openclean.profiling.constraints.ucc import UniqueColumnCombinationFinder

from openclean_metanome.algorithm.base import run_workflow, DATA_FILE, RESULT_FILE
from openclean_metanome.converter import read_json, write_dataframe

import openclean_metanome.config as config


def hyucc(
    df: pd.DataFrame, max_ucc_size: int = -1, input_row_limit: int = -1,
    validate_parallel: bool = False, memory_guardian: bool = True,
    null_equals_null: bool = True, env: Optional[Dict] = None,
    verbose: Optional[bool] = True
) -> List[Columns]:
    """Run the HyUCC algorithm on a given data frame. HyUCC is a hybrid
    discovery algorithm for unique column combinations. The algorithm returns a
    list of discovered column combinations.

    Parameters
    ----------
    df: pd.DataFrame
        Input data frame.
    max_ucc_size: int, default=-1
        Defines the maximum size of discovered column sets. Use -1 to
        return all discovered unique column combinations.
    input_row_limit: int, default=-1
        Limit the number of rows from the input file that are being used
        for column combination discovery. Use -1 for all columns.
    validate_parallel: bool, default=False
        If true the algorithm will use multiple threads (one thread per
        available CPU core).
    memory_guardian: bool, default=True
        Activate the memory guarding to prevent out of memory errors,
    null_equals_null: bool, default=True
        Result value when comparing two NULL values.
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings, default=None
    verbose: bool, default=True
        Output run logs if True.

    Returns
    -------
    list of columns
    """
    return HyUCC(
        max_ucc_size=max_ucc_size,
        input_row_limit=input_row_limit,
        validate_parallel=validate_parallel,
        memory_guardian=memory_guardian,
        null_equals_null=null_equals_null,
        env=env,
        verbose=verbose
    ).run(df)


class HyUCC(UniqueColumnCombinationFinder):
    """HyUCC is a hybrid discovery algorithm for unique column combinations.
    The HyUCC algorithm uses the same discovery techniques as the hybrid
    functional dependency discovery algorithm HyFD. HyUCC discovers all
    minimal unique column combinationsin a given dataset:

    Thorsten Papenbrock and Felix Naumann,
    A Hybrid Approach for Efficient Unique Column Combination Discovery,
    Datenbanksysteme fuer Business, Technologie und Web (BTW 2017),
    """
    def __init__(
        self, max_ucc_size: int = -1, input_row_limit: int = -1,
        validate_parallel: bool = False, memory_guardian: bool = True,
        null_equals_null: bool = True, env: Optional[Dict] = None,
        verbose: Optional[bool] = True
    ):
        """Initialize the algorithm parameters.

        Parameters
        ----------
        max_ucc_size: int, default=-1
            Defines the maximum size of discovered column sets. Use -1 to
            return all discovered unique column combinations.
        input_row_limit: int, default=-1
            Limit the number of rows from the input file that are being used
            for column combination discovery. Use -1 for all columns.
        validate_parallel: bool, default=False
            If true the algorithm will use multiple threads (one thread per
            available CPU core).
        memory_guardian: bool, default=True
            Activate the memory guarding to prevent out of memory errors,
        null_equals_null: bool, default=True
            Result value when comparing two NULL values.
        env: dict, default=None
            Optional environment variables that override the system-wide
            settings, default=None
        verbose: bool, default=True
            Output run logs if True.
        """
        # Create argument dictionary for running the HyUCC workflow. The workflow
        # expects the following arguments:
        #
        # - df: Input data frame
        # - jar: Path to the Metanome.jar file
        # - inputfile: Path (relative to run directory) to materialize the data frame
        # - outputfile: Path (relative to run directory) for the algorithm results
        # - max_ucc_size: Max. size of discovered column sets
        # - input_row_limit: Limit number of input rows that are used for FD discovery
        # - validate_parallel: Switch on/off parallel execution
        # - memory_guardian: Swith on/off memory guardian
        # - null_equals_null: Control interpretation of null values
        self.args = {
            'jar': config.JARFILE(env=env),
            'max_ucc_size': max_ucc_size,
            'input_row_limit': input_row_limit,
            'validate_parallel': '--validate-parallel' if validate_parallel else '',
            'memory_guardian': '--memory-guardian' if memory_guardian else '',
            'null_equals_null': '--null-equals-null' if null_equals_null else ''
        }
        self.env = env
        self.verbose = verbose

    def run(self, df: pd.DataFrame) -> List[Columns]:
        """Run the HyUCC algorithm on the given data frame. Returns a list of
        all discovered unique column sets.

        If execution of the Metanome algorithm fails a RuntimeError will be
        raised.

        Parameters
        ----------
        df: pd.DataFrame
            Input data frame.

        Returns
        -------
        list of columns
        """
        # Get values for specific worker and volume from the environment.
        volume = config.VOLUME(env=self.env)
        worker = config.WORKER(env=self.env)
        # Define the serial workflow for running the HyUCC algorithm.
        command = (
            '${java} -jar "${jar}" hyucc '
            '--input "${inputfile}" --output "${outputfile}" '
            '--max-ucc-size ${max_ucc_size} --input-row-limit ${input_row_limit} '
            '${validate_parallel} ${memory_guardian} ${null_equals_null}'
        )
        workflow = SerialWorkflow()
        workflow.add_code_step(
            identifier='__s1__',
            func=write_dataframe,
            arg='colmap',
            varnames={'filename': 'inputfile'},
            outputs=[DATA_FILE]
        )
        workflow.add_container_step(
            identifier='__s2__',
            image=config.CONTAINER(env=self.env),
            commands=[command],
            inputs=[DATA_FILE],
            outputs=[RESULT_FILE]
        )
        workflow.add_code_step(
            identifier='__s3__',
            func=parse_result,
            arg='uccs',
            inputs=[RESULT_FILE]
        )
        r = run_workflow(
            workflow=workflow,
            arguments=self.args,
            df=df,
            worker=worker,
            volume=volume,
            managers={'__s2__': worker[WORKER_ID]} if worker else None,
            verbose=self.verbose
        )
        return r.context['uccs']


# -- Result Function ----------------------------------------------------------

def parse_result(outputfile: str, colmap: Dict) -> List[Columns]:
    """Parse the result file of the UCC discovery run to generate a list of
    discovered unique column sets.

    Parameters
    ----------
    outputfile: string
        Path to the output file containing the discovered UCCs.
    colmap: dict
        Mapping of column names from surrogate names to column names in the
        input data frame schema.

    Returns
    -------
    list of columns
    """
    result = list()
    for columns in read_json(outputfile)['columnCombinations']:
        ucc = [colmap[c] for c in columns]
        result.append(ucc)
    return result
