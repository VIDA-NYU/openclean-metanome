# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Helper function to download the Metanome.jar file tha is hosted on Zenodo."""

from refdata.base import DatasetDescriptor
from refdata.store.base import download_file
from typing import Optional

import os

import openclean_metanome.config as config


# Information about the Metanome.jar download file.
JARFILE = DatasetDescriptor({
    'id': 'Metanome.jar',
    'url': 'https://zenodo.org/record/4604964/files/Metanome.jar?download=1',
    'checksum': 'a44ef142d1ac2d07c7f597990688a86e061d16b47d0c27f6b1389b6a197d9298'
})


def download_jar(dst: Optional[str] = None, verbose: Optional[bool] = True):
    """Download the Metanome.jar file.

    The file will be stored at the given destination. If no destination is
    specified, the file will be stored in the default location as defined by
    the ``config.JARFILE()`` method.

    The file will only be downloaded if the destination file does not exist.

    Parameters
    ----------
    dst: str, default=None
        Target pathname for the downloaded file.
    verbose: bool, default=True
        Print downloaded file target path if True.
    """
    dst = dst if dst else config.JARFILE()
    if verbose:
        print('download jar file as {}'.format(dst))
    if os.path.exists(dst):
        if verbose:
            print('file exists')
        return
    download_file(dataset=JARFILE, dst=dst)
