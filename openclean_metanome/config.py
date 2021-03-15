# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Configuration variables and helper methods for running Metanome algorihms in
openclean.
"""

from appdirs import user_cache_dir
from flowserv.controller.worker.factory import WorkerFactory
from typing import Dict, Optional

import os

import openclean.config as occ


"""Environment variables to configure the Metanome package."""
# Identifier of the Metanome container image.
METANOME_CONTAINER = 'METANOME_CONTAINER'
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'
# Path to the package specific worker configuration.
METANOME_WORKERS = 'METANOME_WORKERS'


def CONTAINER(env: Optional[Dict] = None) -> str:
    """Get the identifier of the Metanome container image from the environment
    variable

    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings., defualt=None

    Returns
    -------
    string
    """
    default = os.environ.get(METANOME_CONTAINER, 'heikomueller/openclean-metanome:0.1.0')
    return env.get(METANOME_CONTAINER, default) if env else default


def JARFILE(env: Optional[Dict] = None) -> str:
    """Get path to the Metanome.jar file from the environment.

    By default, the jar file is expected to be in the OS-specific user
    cache directory.
    
    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings., defualt=None

    Returns
    -------
    string
    """
    default_dir = user_cache_dir(appname=__name__.split('.')[0])
    default = os.environ.get(METANOME_JARPATH, os.path.join(default_dir, 'Metanome.jar'))
    return env.get(METANOME_JARPATH, default) if env else default


def WORKERS(env: Optional[Dict] = None) -> WorkerFactory:
    """Create a worker factory for serial workflow execution from
    the default configuration and the package-specific configuration
    file.

    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings., defualt=None

    Returns
    -------
    flowserv.controller.serial.worker.factory.WorkerFactory
    """
    return occ.WORKERS(var=METANOME_WORKERS, env=env)
