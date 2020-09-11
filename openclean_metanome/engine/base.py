# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Engine for running Metanome data profiling algorithms using the Java
wrapper.
"""

import os

from typing import List, Tuple

import openclean_metanome.engine.proc as proc


"""Environment variables to configure the Metanome engine."""
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'


class MetanomeEngine(object):
    """The metanome engine is responsible for running algorithms that are
    supported by the Java wrapper. The engine may use different execution
    backends in the future. For now we executet the Matenome.jar file using
    subprocess.
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

    def run(self, args: List[str]) -> Tuple[int, str]:
        """Run a Metanome algorithm using the Java wrapper with the given
        arguments. Returns a tuple of exit code and captured outputs. An exit
        code of 0 indicates success.

        Parameters
        ----------
        args: list
            List of arguments for the Java wrapper.

        Returns
        -------
        int, str
        """
        return proc.run_algorithm(jarfile=self.jarfile, args=args)
