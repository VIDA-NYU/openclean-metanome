# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.


"""Simple helper classes that allow the engine to distinguish between file
arguments and string. This distinction is necessary th generate references
to input and output files for different engine.
"""

from enum import Enum


class ArgType(Enum):
    """Unique argument type identifier."""
    FILE = 1
    STRING = 2


class RunArg(object):
    """Wrapper around input arguments for Metanome algorithms. Maintains the
    argument value and the unique type identifier. We currently distinguish
    only between file arguments and strings.
    """
    def __init__(self, arg_type: ArgType, arg_value: str):
        """Initialize the argument type and the argument value.

        Parameters
        ----------
        arg_type: openclean_metadata.engine.arguments.ArgType
            Unique argument type identifier.
        arg_value: string
            Argument value (as string).
        """
        self.arg_type = arg_type
        self.arg_value = arg_value

    def __str__(self):
        """Get string representation of the argument value."""
        return self.arg_value

    def is_file(self) -> bool:
        """Test if an argument is of type FILE.

        Returns
        -------
        bool
        """
        return self.arg_type == ArgType.FILE

    def is_string(self) -> bool:
        """Test if an argument is of type STRING.

        Returns
        -------
        bool
        """
        return self.arg_type == ArgType.STRING

    @property
    def value(self) -> str:
        """Synonym for arg_value.

        Returns
        -------
        string
        """
        return self.arg_value


class File(RunArg):
    """Argument of type FILE. File argument are expected to contain a relative
    path to a file. The path is relative to the run directory.
    """
    def __init__(self, value: str):
        """Initialize the relative file path.

        Parameters
        ----------
        value: string
            Path to file (relative to the run directory).
        """
        super(File, self).__init__(arg_type=ArgType.FILE, arg_value=value)


class String(RunArg):
    """Argument of type STRING. Any argument that is not of type FILE is
    represented as a STRING argument.
    """
    def __init__(self, value):
        """Initialize the argument value. Expects a scalar value that can be
        converted to string.

        Parameters
        ----------
        value: string, int, or float
            Argument value.
        """
        super(String, self).__init__(
            arg_type=ArgType.STRING,
            arg_value=str(value)
        )
