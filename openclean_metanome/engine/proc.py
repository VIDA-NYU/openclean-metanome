# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

import logging
import os
import subprocess

from typing import List

from openclean_metanome.engine.arguments import RunArg
from openclean_metanome.engine.base import MetanomeEngine
from openclean_metanome.error import MetanomeError


logger = logging.getLogger(__name__)


"""Environment variables to configure the Metanome engine."""
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'


class SubprocEngine(MetanomeEngine):
    """Implementation of the metanoe engine that runs all algorithms as
    sub-processes.
    """
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

    def run(self, args: List[RunArg], rundir: str, verbose: bool = False):
        """Run a Metanome algorithm using the Java wrapper as a subprocess. If
        the verbose flag is True the captured outputs are printed. If execution
        fails a MetanomeError is raised.

        Parameters
        ----------
        args: list of openclean_metanome.engine.arguments.RunArg
            List of arguments for the Java wrapper.
        rundir: string
            Path to local directory for run input and output files.
        verbose: bool, default=False
            Print captured algorithm outputs to standard output (if True).

        Raises
        ------
        openclean_metanome.error.MetanomeError
        """
        # Create run arguments. Make sure that all file arguments point to the
        # run directory.
        runargs = list()
        for arg in args:
            if arg.is_file():
                runargs.append(os.path.join(rundir, arg.value))
            else:
                runargs.append(arg.value)
        # Get path to Java Runtime (if specified in the environment variable).
        jre = os.environ.get('JAVA_HOME')
        jre = os.path.join(jre, 'bin/java') if jre else 'java'
        cmd = '{java} -jar {jar} {args}'.format(
            java=jre,
            jar=self.jarfile,
            args=' '.join(runargs)
        )
        if verbose:
            logger.info('Run {}'.format(cmd))
        proc = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        is_error = proc.returncode != 0
        # Get captured outputs only if the verbose flag is set or the return
        # code indicates an error. Otherwise we are done.
        if not verbose and not is_error:
            return
        outputs = proc.stdout.decode('utf-8')
        if is_error:
            raise MetanomeError(outputs)
        else:
            print(outputs)
