# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Wrapper to run the HyUCC algorithm (A Hybrid Approach for Efficient Unique
Column Combination Discovery) from the Metanome data profiling library. HyUCC
is a unique column combination doscovery algorithm.
"""

import os
import pandas as pd
import shutil
import tempfile

from typing import List


from openclean.profiling.constraints.ucc import (
    UniqueColumnSet, UniqueColumnCombinationFinder
)

from openclean_metanome.engine.arguments import File, String
from openclean_metanome.engine.base import MetanomeEngine
from openclean_metanome.engine.init import get_engine

import openclean_metanome.converter as convert


"""Names for input and output files for the HyUCC algorithm."""
IN_FILE = 'table.csv'
OUT_FILE = 'results.json'


def hyucc(
    df: pd.DataFrame, max_ucc_size: int = -1, input_row_limit: int = -1,
    validate_parallel: bool = False, memory_guardian: bool = True,
    null_equals_null: bool = True, verbose: bool = False,
    engine: MetanomeEngine = None
) -> List[UniqueColumnSet]:
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
    verbose: bool, default=False
        Print captured algorithm outputs to standard output (if True).
    engine: openclean_metanome.engine.base.MetanomeEngine
        Runtime engine for all Metanome algorithms. This parameter is
        primarily included for running unit tests.

    Returns
    -------
    list of UniqueColumnSet

    Raises
    ------
    openclean_metanome.error.MetanomeError
    """
    return HyUCC(
        max_ucc_size=max_ucc_size,
        input_row_limit=input_row_limit,
        validate_parallel=validate_parallel,
        memory_guardian=memory_guardian,
        null_equals_null=null_equals_null,
        verbose=verbose,
        engine=engine
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
        null_equals_null: bool = True, verbose: bool = False,
        engine: MetanomeEngine = None
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
        verbose: bool, default=False
            Print captured algorithm outputs to standard output (if True).
        engine: openclean_metanome.engine.base.MetanomeEngine
            Runtime engine for all Metanome algorithms. This parameter is
            primarily included for running unit tests.
        """
        self.max_ucc_size = max_ucc_size
        self.input_row_limit = input_row_limit
        self.validate_parallel = validate_parallel
        self.memory_guardian = memory_guardian
        self.null_equals_null = null_equals_null
        self.verbose = verbose
        self.engine = engine if engine is not None else get_engine()

    def run(self, df: pd.DataFrame) -> List[UniqueColumnSet]:
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
        list of UniqueColumnSet

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
            String('hyucc'),
            String('--input'),
            File(IN_FILE),
            String('--output'),
            File(OUT_FILE),
            String('--max-ucc-size'),
            String(self.max_ucc_size),
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
            for columns in convert.read_json(out_file)['columnCombinations']:
                ucc = UniqueColumnSet([col_mapping[c] for c in columns])
                result.append(ucc)
            return result
        finally:
            # Remove the created run directory.
            shutil.rmtree(rundir)
