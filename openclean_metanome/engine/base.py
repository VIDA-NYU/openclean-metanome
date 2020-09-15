# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Engine for running Metanome data profiling algorithms using the Java
wrapper.
"""

from abc import ABCMeta, abstractmethod

from typing import List, Tuple

from openclean_metanome.engine.arguments import RunArg


"""Environment variables to configure the Metanome engine."""
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'


class MetanomeEngine(metaclass=ABCMeta):
    """The metanome engine is responsible for running algorithms that are
    supported by the Java wrapper. The engine may use different execution
    backends.
    """
    @abstractmethod
    def run(self, args: List[RunArg], rundir: str, verbose: bool = False):
        """Run a Metanome algorithm using the Java wrapper with the given
        arguments. This method does not return a result value. The execution
        results are stored in the respective output files that are passed to
        Metanome algorithm. A MetanomeError is raised if if execution fails.

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
        raise NotImplementedError()  # pragma: noqa
