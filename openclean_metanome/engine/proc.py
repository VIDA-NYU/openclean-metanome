# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

import logging
import subprocess

from typing import List, Tuple


def run_algorithm(jarfile: str, args: List[str]) -> Tuple[int, List[str]]:
    """Run the Metanome command-line wrapper for the given list of arguments.
    Returns the exit code (0 for success) and the captured output for the
    algorithm execution.

    Parameters
    ----------
    jarfile: string
        Path to the Matenome.jar file
    args: list
        List of arguments for the Metanome command-line wrapper.

    Returns
    -------
    int, list
    """
    cmd = 'java -jar {jar} {args}'.format(jar=jarfile, args=' '.join(args))
    logging.debug('Run: {}'.format(cmd))
    proc = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return proc.returncode, proc.stdout.decode('utf-8')
