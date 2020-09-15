# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
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

import os
import pandas as pd
import shutil
import tempfile

from typing import List


from openclean.profiling.constraints.fd import (
    FunctionalDependency, FunctionalDependencyFinder
)
from openclean.profiling.constraints.ucc import UniqueColumnSet

from openclean_metanome.algorithm.base import IN_FILE, OUT_FILE
from openclean_metanome.engine.arguments import File, String
from openclean_metanome.engine.base import MetanomeEngine
from openclean_metanome.engine.init import get_engine

import openclean_metanome.converter as convert


def hyfd(
    df: pd.DataFrame, max_lhs_size: int = -1, input_row_limit: int = -1,
    validate_parallel: bool = False, memory_guardian: bool = True,
    null_equals_null: bool = True, verbose: bool = False,
    engine: MetanomeEngine = None
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
    verbose: bool, default=False
        Print captured algorithm outputs to standard output (if True).
    engine: openclean_metanome.engine.base.MetanomeEngine
        Runtime engine for all Metanome algorithms. This parameter is
        primarily included for running unit tests.

    Returns
    -------
    list of FunctionalDependency

    Raises
    ------
    openclean_metanome.error.MetanomeError
    """
    return HyFD(
        max_lhs_size=max_lhs_size,
        input_row_limit=input_row_limit,
        validate_parallel=validate_parallel,
        memory_guardian=memory_guardian,
        null_equals_null=null_equals_null,
        verbose=verbose,
        engine=engine
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
        null_equals_null: bool = True, verbose: bool = False,
        engine: MetanomeEngine = None
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
        verbose: bool, default=False
            Print captured algorithm outputs to standard output (if True).
        engine: openclean_metanome.engine.base.MetanomeEngine
            Runtime engine for all Metanome algorithms. This parameter is
            primarily included for running unit tests.
        """
        self.max_lhs_size = max_lhs_size
        self.input_row_limit = input_row_limit
        self.validate_parallel = validate_parallel
        self.memory_guardian = memory_guardian
        self.null_equals_null = null_equals_null
        self.verbose = verbose
        self.engine = engine if engine is not None else get_engine()

    def run(self, df: pd.DataFrame) -> List[FunctionalDependency]:
        """Run the HyFD algorithm on the given data frame. Returns a list of
        all discovered functional dependencies.

        If execution of the Metanome algorithm fails a RuntimeError will be
        raised.

        Parameters
        ----------
        df: pd.DataFrame
            Input data frame.

        Returns
        -------
        list of FunctionalDependency

        Raises
        ------
        openclean_metanome.error.MetanomeError
        """
        # Create temporary run directory for input and output files.
        rundir = tempfile.mkdtemp()
        # Create input CSV from given data frame.
        in_file = os.path.join(rundir, IN_FILE)
        col_mapping = convert.write_dataframe(df=df, filename=in_file)
        # List of command line arguments based on the current parameters that
        # were provided by the user.
        args = [
            String('hyfdc'),
            String('--input'),
            File(IN_FILE),
            String('--output'),
            File(OUT_FILE),
            String('--max-lhs-size'),
            String(self.max_lhs_size),
            String('--input-row-limit'),
            String(self.input_row_limit)
        ]
        if self.validate_parallel:
            args.append(String('--validate-parallel'))
        if self.memory_guardian:
            args.append(String('--memory-guardian'))
        if self.null_equals_null:
            args.append(String('--null-equals-null'))
        try:
            # Run the algorithm. This will raise a MetanomeError if execution
            # fails.
            self.engine.run(args=args, rundir=rundir, verbose=self.verbose)
            # Read results from the output file and convert them to unique
            # column sets for the original data frame columns..
            out_file = os.path.join(rundir, OUT_FILE)
            result = list()
            for obj in convert.read_json(out_file)['functionalDependencies']:
                fd = FunctionalDependency(
                    lhs=UniqueColumnSet([col_mapping[c] for c in obj['lhs']]),
                    rhs=UniqueColumnSet([col_mapping[c] for c in obj['rhs']])
                )
                result.append(fd)
            return result
        finally:
            # Remove the created run directory.
            shutil.rmtree(rundir)
