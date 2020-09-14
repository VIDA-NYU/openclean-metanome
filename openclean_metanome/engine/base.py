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
    def run(self, args: List[RunArg], rundir: str) -> Tuple[int, str]:
        """Run a Metanome algorithm using the Java wrapper with the given
        arguments. Returns a tuple of exit code and captured outputs. An exit
        code of 0 indicates success.

        Parameters
        ----------
        args: list of openclean_metanome.engine.arguments.RunArg
            List of arguments for the Java wrapper.
        rundir: string
            Path to local directory for run input and output files.

        Returns
        -------
        int, str
        """
        raise NotImplementedError()  # pragma: noqa
