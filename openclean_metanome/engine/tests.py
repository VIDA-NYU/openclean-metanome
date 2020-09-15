# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Fake Metanome engine for simple unit tests."""

import json
import os

from typing import Dict, List, Union

from openclean_metanome.engine.arguments import RunArg
from openclean_metanome.engine.base import MetanomeEngine
from openclean_metanome.error import MetanomeError


class MetanomeTestEngine(MetanomeEngine):
    """Test engine to simulate run of the Metanome algorithm. This engine takes
    advantage of the fact that all Metanome algorithms are run with the
    '--output' option that points to a single result file.

    The engine can be initialized with with the expected result. The result
    object will be written the file that is specified as the output parameter
    for the algorithm run. If no result is given the engine will raise a
    MetanomeError.
    """
    def __init__(self, result: Union[Dict, List] = None):
        """Initialize the result list or object. The result will be written to
        the output file that is identified by the '--output' parameter in the
        argument list when running the algorithm.

        Parameters
        ----------
        result: dict or list, default=None
            Result of algorithm run.
        """
        self.result = result

    def run(self, args: List[RunArg], rundir: str, verbose: bool = False):
        """Simulate running the HyUCC algorithm. If a result list was given it
        will be written to the output file. If no list was given 255 with an
        error message is returned.

        Parameters
        ----------
        args: list
            List of arguments for the HyUCC algorithm.
        rundir: string
            Path to local directory for run input and output files.
        verbose: bool, default=False
            Print captured algorithm outputs to standard output (if True).
        """
        if self.result is None:
            raise MetanomeError('There was an error')
        # Get the result file from the argument list.
        for i in range(len(args)):
            if args[i].value == '--output':
                outfile = os.path.join(rundir, args[i+1].value)
                break
        with open(outfile, 'w') as f:
            json.dump(self.result, f)
