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
from flowserv.controller.worker.manager import Docker  # noqa: F401
from flowserv.util import read_object
from typing import Dict, Optional

import os


"""Environment variables to configure the Metanome package."""
# Identifier of the Metanome container image.
METANOME_CONTAINER = 'METANOME_CONTAINER'
# Path to the Metanome.jar file
METANOME_JARPATH = 'METANOME_JARPATH'
# Path to worker-specific storage volume.
METANOME_VOLUME = 'METANOME_VOLUME'
# Path to the package specific worker configuration.
METANOME_WORKER = 'METANOME_WORKER'


def CONTAINER(env: Optional[Dict] = None) -> str:
    """Get the identifier of the Metanome container image from the environment
    variable

    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings, default=None

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
        settings, default=None

    Returns
    -------
    string
    """
    default_dir = user_cache_dir(appname=__name__.split('.')[0])
    default = os.environ.get(METANOME_JARPATH, os.path.join(default_dir, 'Metanome.jar'))
    return env.get(METANOME_JARPATH, default) if env else default


def VOLUME(env: Optional[Dict] = None) -> Dict:
    """Get specification for the volume that is associated with the worker that
    is used to execute the main algorithm step.

    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings, default=None

    Returns
    -------
    dict
    """
    return read_config_obj(var=METANOME_VOLUME, env=env if env is not None else os.environ)


def WORKER(env: Optional[Dict] = None) -> Dict:
    """Get specification for the worker that is used to execute the main
    algorithm step using the metanome wrapper Jar-file.

    Parameters
    ----------
    env: dict, default=None
        Optional environment variables that override the system-wide
        settings, default=None

    Returns
    -------
    dict
    """
    return read_config_obj(var=METANOME_WORKER, env=env if env is not None else os.environ)


# -- Helper Methods -----------------------------------------------------------

def read_config_obj(var: str, env: Dict) -> Dict:
    """Read configuration object from a given environment variables.

    If the variable is set and contains a dictionary as value that value is
    returned. Otherwise, it is assumed that the variable references a Json or
    Yaml file that contains the configuration object.

    Parameters
    ----------
    var: string
        Name of the environment variable.
    env: dict
        Dictionary representing the current environment settings.

    Returns
    -------
    dict
    """
    obj = env.get(var)
    if not obj:
        return None
    if isinstance(obj, dict):
        return obj
    return read_object(filename=obj)
