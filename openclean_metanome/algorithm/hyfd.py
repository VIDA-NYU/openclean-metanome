# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Wrapper to run the HyFD algorithm (A Hybrid Approach to Functional
Dependency Discovery) from the Metanome data profiling library. HyFD is a
functional dependency discovery algorithm.

Thorsten Papenbrock, Felix Naumann
A Hybrid Approach to Functional Dependency Discovery
ACM International Conference on Management of Data (SIGMOD '16)

From the abstract: [...] HyFD combines fast approximation techniques with
efficient validation techniques in order to findall minimal functional
dependencies in a given dataset. While operating on compact data structures,
HyFD not only outperforms all existing approaches, it also scales to much
larger datasets.
"""

from typing import Dict, List, Optional

import pandas as pd

from flowserv.controller.serial.workflow.base import SerialWorkflow
from flowserv.controller.worker.manager import WORKER_ID
from openclean.profiling.constraints.fd import FunctionalDependency, FunctionalDependencyFinder
from openclean_metanome.algorithm.base import run_workflow, DATA_FILE, RESULT_FILE
from openclean_metanome.converter import read_json, write_dataframe

import openclean_metanome.config as config


def hyfd(
    df: pd.DataFrame, max_lhs_size: int = -1, input_row_limit: int = -1,
    validate_parallel: bool = False, memory_guardian: bool = True,
    null_equals_null: bool = True, env: Optional[Dict] = None,
    verbose: Optional[bool] = True
) -> List[FunctionalDependency]:
    """Run the HyFD algorithm on a given data frame. HyFD is a hybrid
    discovery algorithm for functional dependencies.

    Parameters
    ----------
    df: pd.DataFrame
        Input data frame.
    max_lhs_size: int, default=-1
        Defines the maximum size of the left-hand-side for discovered FDs. Use
        -1 to ignore size limits on FDs.
    input_row_limit: int, default=-1
        Limit the number of rows from the input file that are being used
        for functional dependency discovery. Use -1 for all columns.
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
    list of FunctionalDependency
    """
    return HyFD(
        max_lhs_size=max_lhs_size,
        input_row_limit=input_row_limit,
        validate_parallel=validate_parallel,
        memory_guardian=memory_guardian,
        null_equals_null=null_equals_null,
        env=env,
        verbose=verbose
    ).run(df)


class HyFD(FunctionalDependencyFinder):
    """HyFD is a hybrid discovery algorithm for functional dependencies.
    HyFD combines fast approximation techniques with efficient validation
    techniques in order to findall minimal functional dependencies in a given
    dataset:

    Thorsten Papenbrock, Felix Naumann
    A Hybrid Approach to Functional Dependency Discovery
    ACM International Conference on Management of Data (SIGMOD '16)
    """
    def __init__(
        self, max_lhs_size: int = -1, input_row_limit: int = -1,
        validate_parallel: bool = False, memory_guardian: bool = True,
        null_equals_null: bool = True, env: Optional[Dict] = None,
        verbose: Optional[bool] = True
    ):
        """Initialize the algorithm parameters.

        Parameters
        ----------
        max_lhs_size: int, default=-1
            Defines the maximum size of the left-hand-side for discovered FDs
             Use -1 to ignore size limits on FDs.
        input_row_limit: int, default=-1
            Limit the number of rows from the input file that are being used
            for functional dependency discovery. Use -1 for all columns.
        validate_parallel: bool, default=False
            If true the algorithm will use multiple threads (one thread per
            available CPU core).
        memory_guardian: bool, default=True
            Activate the memory guarding to prevent out of memory errors,
        null_equals_null: bool, default=True
            Result value when comparing two NULL values.
        env: dict, default=None
            Optional environment variables that override the system-wide
            settings, default=None.
        verbose: bool, default=True
            Output run logs if True.
        """
        # Create argument dictionary for running the HyFD workflow. The workflow
        # expects the following arguments:
        #
        # - df: Input data frame
        # - jar: Path to the Metanome.jar file
        # - inputfile: Path (relative to run directory) to materialize the data frame
        # - outputfile: Path (relative to run directory) for the algorithm results
        # - max_lhs_size: Max. number of attributes in LHS for discovered FDs
        # - input_row_limit: Limit number of input rows that are used for FD discovery
        # - validate_parallel: Switch on/off parallel execution
        # - memory_guardian: Swith on/off memory guardian
        # - null_equals_null: Control interpretation of null values
        self.args = {
            'jar': config.JARFILE(env=env),
            'max_lhs_size': max_lhs_size,
            'input_row_limit': input_row_limit,
            'validate_parallel': '--validate-parallel' if validate_parallel else '',
            'memory_guardian': '--memory-guardian' if memory_guardian else '',
            'null_equals_null': '--null-equals-null' if null_equals_null else ''
        }
        self.env = env
        self.verbose = verbose

    def run(self, df: pd.DataFrame) -> List[FunctionalDependency]:
        """Run the HyFD algorithm on the given data frame.

        Returns a list of all discovered functional dependencies. If execution
        of the Metanome algorithm fails a RuntimeError will be raised.

        Parameters
        ----------
        df: pd.DataFrame
            Input data frame.

        Returns
        -------
        list of FunctionalDependency
        """
        # Get values for specific worker and volume from the environment.
        volume = config.VOLUME(env=self.env)
        worker = config.WORKER(env=self.env)
        # Define the serial workflow for running the HyFD algorithm.
        command = (
            '${java} -jar "${jar}" hyfd '
            '--input "${inputfile}" --output "${outputfile}" '
            '--max-lhs-size ${max_lhs_size} --input-row-limit ${input_row_limit} '
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
            arg='fds',
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
        return r.context['fds']


# -- Result Function ----------------------------------------------------------

def parse_result(outputfile: str, colmap: Dict) -> List[FunctionalDependency]:
    """Parse the result file of the FD discovery run to generate a list of
    discovered functional dependencies.

    Parameters
    ----------
    outputfile: string
        Path to the output file containing the discovered FDs.
    colmap: dict
        Mapping of column names from surrogate names to column names in the
        input data frame schema.

    Returns
    -------
    list of FunctionalDependency
    """
    result = list()
    for obj in read_json(filename=outputfile)['functionalDependencies']:
        fd = FunctionalDependency(
            lhs=[colmap[c] for c in obj['lhs']],
            rhs=[colmap[obj['rhs']]]
        )
        result.append(fd)
    return result
