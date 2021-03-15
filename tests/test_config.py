# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for the worker configuration."""

import os

import openclean_metanome.config as config

DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
CONFIG_DIR = os.path.join(DIR, 'config')
DOCKER_WORKERS = os.path.join(CONFIG_DIR, 'docker_worker.yaml')


def test_config_workers():
    """Test getting the flowServ worker factory from files referenced by
    ennvironment variables.
    """
    os.environ[config.METANOME_WORKERS] = DOCKER_WORKERS
    factory = config.WORKERS()
    worker = factory.config['heikomueller/openclean-metanome:0.1.0']
    assert worker['worker'] == 'docker'
    assert worker['args'] == {'variables': {'jar': 'lib/Metanome.jar'}}
    # Get the default configuration.
    del os.environ[config.METANOME_WORKERS]
    factory = config.WORKERS()
    assert factory.config == dict()
