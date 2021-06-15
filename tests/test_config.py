# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Unit tests for configuration helper methods."""

from flowserv.util import write_object

import os

import openclean_metanome.config as config


def test_env_container():
    """Test getting values for the METANOME_CONTAINER variable."""
    os.environ[config.METANOME_CONTAINER] = 'mycontainer'
    assert config.CONTAINER() == 'mycontainer'
    assert config.CONTAINER(env={config.METANOME_CONTAINER: 'x'}) == 'x'
    del os.environ[config.METANOME_CONTAINER]
    assert config.CONTAINER() == 'heikomueller/openclean-metanome:0.1.0'


def test_env_jarpath():
    """Test getting values for the METANOME_JARPATH variable."""
    os.environ[config.METANOME_JARPATH] = 'my.jar'
    assert config.JARFILE() == 'my.jar'
    assert config.JARFILE(env={config.METANOME_JARPATH: 'x'}) == 'x'
    del os.environ[config.METANOME_JARPATH]
    assert config.JARFILE().endswith('Metanome.jar')


def test_env_volume(tmpdir):
    """Test getting values for the METANOME_VOLUME variable."""
    # -- Setup ----------------------------------------------------------------
    filename = os.path.join(tmpdir, 'volume.json')
    write_object(obj={'x': 1}, filename=filename)
    # -- Unit tests -----------------------------------------------------------
    os.environ[config.METANOME_VOLUME] = filename
    assert config.VOLUME() == {'x': 1}
    del os.environ[config.METANOME_VOLUME]
    assert config.VOLUME() is None
    assert config.VOLUME(env={config.METANOME_VOLUME: {'y': 2}}) == {'y': 2}


def test_env_worker(tmpdir):
    """Test getting values for the METANOME_WORKER variable."""
    # -- Setup ----------------------------------------------------------------
    filename = os.path.join(tmpdir, 'worker.json')
    write_object(obj={'x': 1}, filename=filename)
    # -- Unit tests -----------------------------------------------------------
    os.environ[config.METANOME_WORKER] = filename
    assert config.WORKER() == {'x': 1}
    del os.environ[config.METANOME_WORKER]
    assert config.WORKER() is None
    assert config.WORKER(env={config.METANOME_WORKER: {'y': 2}}) == {'y': 2}
