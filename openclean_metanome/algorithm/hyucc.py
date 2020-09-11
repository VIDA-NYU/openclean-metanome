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

import json
import os
import pandas as pd
import tempfile

from typing import List, Tuple


from openclean.profiling.constraints.ucc import (
    UniqueColumnSet, UniqueColumnCombinationFinder
)

from openclean_metanome.engine.base import MetanomeEngine

import openclean_metanome.converter as convert


class HyUCC(UniqueColumnCombinationFinder):
    """HyUCC is a unique column combination doscovery algorithm. HyUCC is a
    hybrid discovery algorithm which uses the same discovery techniques as the
    hybrid functional dependency discovery algorithm HyFD. HyUCC discovers all
    minimal unique column combinationsin a given dataset:

    Thorsten Papenbrock and Felix Naumann,
    A Hybrid Approach for Efficient Unique Column Combination Discovery,
    Datenbanksysteme fuer Business, Technologie und Web (BTW 2017),
    """
    def __init__(
        self, max_ucc_size: int = -1, input_row_limit: int = -1,
        validate_parallel: bool = False, memory_guardian: bool = True,
        null_equals_null: bool = True, engine: MetanomeEngine = None
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
        engine: openclean_metanome.engine.base.MetanomeEngine
            Runtime engine for all Metanome algorithms. This parameter is
            primarily included for running unit tests.
        """
        self.max_ucc_size = max_ucc_size
        self.input_row_limit = input_row_limit
        self.validate_parallel = validate_parallel
        self.memory_guardian = memory_guardian
        self.null_equals_null = null_equals_null
        self.engine = engine if engine is not None else MetanomeEngine()

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
        UniqueColumnSet

        Raises
        ------
        RuntimeError
        """
        # Create temporary input CSV from given data frame and a temporary file
        # for algorithm outputs.
        infile, col_mapping = convert.create_input(df)
        fh, outfile = tempfile.mkstemp()
        # Close the output file handle.
        os.close(fh)
        # List of command line arguments based on the current parameters that
        # were provided by the user.
        args = [
            'hyucc',
            '--input', infile,
            '--output', outfile,
            '--max-ucc-size',
            str(self.max_ucc_size),
            '--input-row-limit',
            str(self.input_row_limit)
        ]
        if self.validate_parallel:
            args.append('--validate-parallel')
        if self.memory_guardian:
            args.append('--memory-guardian')
        if self.null_equals_null:
            args.append('--null-equals-null')
        try:
            # Run the algorithm. Raise a RunTime error if the returned exit
            # code is not 0.
            exitcode, outputs = self.engine.run(args)
            if exitcode != 0:
                raise RuntimeError(outputs)
            # Read results from the output file and convert them to unique
            # column sets for the original data frame columns..
            result = list()
            for columns in convert.read_output(outfile)['columnCombinations']:
                ucc = UniqueColumnSet([col_mapping[c] for c in columns])
                result.append(ucc)
            return result
        finally:
            # Remove the created temporary files.
            os.remove(infile)
            os.remove(outfile)


# -- Unit test engine ---------------------------------------------------------

class HyUCCEngine(object):
    """Fake Metanome engine to simulate run of the HyUCC algorithm. Initialize
    the engine with the expected result which will be written to file. If no
    result file is given the returned exit code will be 255 instead of 0.
    """
    def __init__(self, result: List = None):
        """Initialize the result list. The list will be written to disk into
        the output file that is identified by the '--output' parameter in the
        argument list when running the algorithm.

        Parameters
        ----------
        result: list, default=None
            Result list of unique column combinations.
        """
        self.result = result

    def run(self, args: List[str]) -> Tuple[int, str]:
        """Simulate running the HyUCC algorithm. If a result list was given it
        will be written to the output file. If no list was given 255 with an
        error message is returned.

        Parameters
        ----------
        args: list
            List of arguments for the HyUCC algorithm.

        Returns
        -------
        int, str
        """
        if self.result is None:
            return 255, 'There was an error'
        # Get the result file from the argument list.
        for i in range(len(args)):
            if args[i] == '--output':
                outfile = args[i+1]
                break
        with open(outfile, 'w') as f:
            json.dump({'columnCombinations': self.result}, f)
        return 0, 'Success'
