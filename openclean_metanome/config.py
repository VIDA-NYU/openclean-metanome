# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Configuration variables and helper methods for running Metanome algorihms in
openclean.
"""

from flowserv.controller.worker.factory import WorkerFactory

import os

import openclean.config as occ


"""Environment variables to configure the Metanome package."""
# Identifier of the Metanome container image.
METANOME_CONTAINER = 'METANOME_CONTAINER'
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'
# Path to the package specific worker configuration.
METANOME_WORKERS = 'METANOME_WORKERS'


def CONTAINER() -> str:
    """Get the identifier of the Metanome container image from the environment
    variable

    Returns
    -------
    string
    """
    return os.environ.get(METANOME_CONTAINER, 'heikomueller/openclean-metanome:0.1.0')


def JARFILE() -> str:
    """Get path to the Metanome.jar file from the environment.

    Returns
    -------
    string
    """
    return os.environ.get(METANOME_JARPATH, 'Metanome.jar')


def WORKERS() -> WorkerFactory:
    """Create a worker factory for serial workflow execution from
    the default configuration and the package-specific configuration
    file.


    Returns
    -------
    flowserv.controller.serial.worker.factory.WorkerFactory
    """
    return occ.WORKERS(var=METANOME_WORKERS)
