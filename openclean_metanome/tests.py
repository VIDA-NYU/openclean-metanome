# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Helper funcitons for unit testing."""

from typing import Tuple

import os


def input_output(rundir: str, cmd: str) -> Tuple[str, str]:
    """Extract name of input file and output file from commands that are used
    to run the Metanome algorithms from the command line.

    Returns the path to the input and output files.

    Parameters
    ----------
    rundir: string
        Path to the run directory. The input and output file references in the
        command string are relative to this directory.
    cmd: string
        Command to run the Metanome algorithms from the command line.

    Returns
    -------
    tuple of (string, string)
    """
    pos = cmd.find('--input "')
    in_file = os.path.join(rundir, cmd[pos + 9: cmd.find('"', pos + 10)])
    pos = cmd.find('--output "')
    out_file = os.path.join(rundir, cmd[pos + 10: cmd.find('"', pos + 11)])
    return in_file, out_file
