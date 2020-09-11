# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Helper functions to prepare inputs and read outputs when running Metanome
algorithms on the contents of pandas data frames.
"""

import json
import os
import pandas as pd
import tempfile

from typing import Dict, List, Tuple, Union


def create_input(df: pd.DataFrame) -> Tuple[str, Dict]:
    """Create a temporary input CSV file from a given data frame. Writes the
    data frame to disk. The column names in the written CSV file are replaced
    by unique names (to account for possible duplicate columns in the input
    data frame).

    The created file is astandard CSV file with the default settings for
    delimiter, quote char and escape char.

    Returns the path to the created temporary CSV file and mapping of unique
    column names to the original columns in the given data frame.

    Parameters
    ----------
    df: pd.DataFrame
        Data frame that is written to disk.

    Returns
    -------
    (str, dict)
    """
    # Create a unique list of column names and a mapping from the new uniqye
    # names to the original columns in the given data frame.
    columns = list()
    column_mapping = dict()
    for colidx in range(len(df.columns)):
        colname = 'COL{}'.format(colidx)
        columns.append(colname)
        column_mapping[colname] = df.columns[colidx]
    # Write data frame to temporary CSV file.
    fh, filename = tempfile.mkstemp()
    df.to_csv(
        os.fdopen(fh, 'w', newline=''),
        header=columns,
        index=False,
        compression=None
    )
    # Return the created CSV file and the column mapping.
    return filename, column_mapping


def read_output(filename: str) -> Union[Dict, List]:
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
