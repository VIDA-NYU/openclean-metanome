# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Helper functions to prepare inputs and read outputs when running Metanome
algorithms on the contents of pandas data frames.
"""

import json
import os
import pandas as pd

from typing import Dict, List, Union


def read_json(filename: str) -> Union[Dict, List]:
    """Read a JSON object or list from the given output file. By convention,
    the Java wrapper for Metanome algorithms stores all algorithm as JSON
    seriaizations.

    Parameter
    ---------
    filename: string
        Path to the input file on disk.

    Returns
    -------
    dict or list
    """
    with open(filename, 'r') as f:
        return json.load(f)


def write_dataframe(df: pd.DataFrame, filename: str) -> Dict:
    """Write the given data frame to a CSV file. The column names in the
    resulting CSV file are replaced by unique names (to account for possible
    duplicate columns in the input data frame).

    The created file is a standard CSV file with the default settings for
    delimiter, quote char and escape char.

    Returns the pmapping of unique column names to the original columns in the
    given data frame.

    Parameters
    ----------
    df: pd.DataFrame
        Data frame that is written to disk.

    Returns
    -------
    dict
    """
    # Ensure that the parent directory for the output file exists.
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    # Create a unique list of column names and a mapping from the new uniqye
    # names to the original columns in the given data frame.
    columns = list()
    column_mapping = dict()
    for colidx in range(len(df.columns)):
        colname = 'COL{}'.format(colidx)
        columns.append(colname)
        column_mapping[colname] = df.columns[colidx]
    # Write data frame to temporary CSV file.
    df.to_csv(
        filename,
        header=columns,
        index=False,
        compression=None
    )
    # Return the created column mapping..
    return column_mapping
