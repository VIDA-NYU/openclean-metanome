# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

import logging
import os
import subprocess

from typing import List, Tuple

from openclean_metanome.engine.arguments import RunArg
from openclean_metanome.engine.base import MetanomeEngine


"""Environment variables to configure the Metanome engine."""
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'


class SubprocEngine(MetanomeEngine):
    """Implementation of the metanoe engine that runs all algorithms as
    sub-processes.
    """
    pass

    def __init__(self, jarfile: str = None):
        """Initialize the path to the Metanome.jar file. If no value is given
        an attempt is made to read the value from the respective environment
        variable.

        Parameters
        ----------
        jarfile: str
            Path to the Matenome.jar file on local disk.
        """
        if jarfile is None:
            jarfile = os.environ.get(METANOME_JARPATH, 'Metanome.jar')
        self.jarfile = jarfile

    def run(self, args: List[RunArg], rundir: str) -> Tuple[int, str]:
        """Run a Metanome algorithm using the Java wrapper with the given
        arguments. Returns a tuple of exit code and captured outputs. An exit
        code of 0 indicates success.

        Parameters
        ----------
        args: list of openclean_metanome.engine.arguments.RunArg
            List of arguments for the Java wrapper.

        Returns
        -------
        int, str
        """
        # Create run arguments. Make sure that all file arguments point to the
        # run directory.
        runargs = list()
        for arg in args:
            if arg.is_file():
                runargs.append(os.path.join(rundir, arg.value))
            else:
                runargs.append(arg.value)
        # Run the Metanome.jar file with the modified argument list.
        return run_algorithm(jarfile=self.jarfile, args=runargs)


# -- Helper Methods -----------------------------------------------------------

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
    # Get path to Java Runtime (if specified in the environment variable).
    jre = os.environ.get('JAVA_HOME')
    jre = os.path.join(jre, 'bin/java') if jre else 'java'
    cmd = '{java} -jar {jar} {args}'.format(
        java=jre,
        jar=jarfile,
        args=' '.join(args)
    )
    logging.debug('Run: {}'.format(cmd))
    proc = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return proc.returncode, proc.stdout.decode('utf-8')
