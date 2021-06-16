=================================================
Integration of Metanome Algorithms into openclean
=================================================

.. image:: https://img.shields.io/pypi/pyversions/openclean-metanome.svg
    :target: https://pypi.org/pypi/openclean-metanome

.. image:: https://badge.fury.io/py/openclean-metanome.svg
    :target: https://badge.fury.io/py/openclean-metanome

.. image:: https://img.shields.io/badge/License-BSD-green.svg
    :target: https://github.com/VIDA-NYU/openclean-metanome/blob/master/LICENSE

.. image:: https://github.com/VIDA-NYU/openclean-metanome/workflows/build/badge.svg
    :target: https://github.com/VIDA-NYU/openclean-metanome/actions?query=workflow%3A%22build%22

.. image:: https://readthedocs.org/projects/openclean-metanome/badge/?version=latest
    :target: https://openclean-metanome.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/VIDA-NYU/openclean-metanome/branch/master/graph/badge.svg?token=VL43CKXZEF
    :target: https://codecov.io/gh/VIDA-NYU/openclean-metanome


.. figure:: https://github.com/VIDA-NYU/openclean-metanome/blob/master/docs/graphics/logo.png
    :align: center
    :alt: openclean Logo



About
=====

This package is an extension for the `openclean-core package <https://github.com/VIDA-NYU/openclean-core>`_. It provides access to data profiling algorithms from the `Metanome project <https://github.com/HPI-Information-Systems/Metanome>`_ in **openclean**. The algorithms themselves are executable via the `Metanome Wrapper <https://github.com/VIDA-NYU/openclean-metanome-algorithms>`_ that enables to run Metanome algorithms via the command line.


Installation & Configuration
============================

The package can be installed using ``pip``.

.. code-block:: bash

    pip install openclean-metanome


The **openclean-metanome** package uses `flowServ <https://github.com/scailfin/flowserv-core>`_ to run Metanome algorithms as serial workflows in **openclean**. **flowServ** supports two modes of execution: (1) using the Python sub-process package, and (2) using Docker.

Python Sub-Process
------------------

When running Metanome algorithms as Python sub-processes you need to have an installation of the *Jave Runtime Environment (Version 8 or higher)* on your local machine. You also need a local copy of the ``Metanome.jar`` wrapper. The file can be `downloaded from Zenodo <https://zenodo.org/record/4604964#.YE9tif4pBH4>`_`. The package also provides the option to download the file from within your Python scripts.

.. code-block:: python

    from openclean_metanome.download import download_jar

    download_jar(verbose=True)

The example will download the jar file into the default directory (defined via the *METANOME_JARPATH* environment variable). If the variable is not set, the users default cache folder is used. Note that the ``Metanome.jar`` is currently about 75 MB in size. Make sure that the environment variable *METANOME_JARPATH* contains a reference to the downloaded jar-file if you did not download the file into the default location.

Docker
------

If you have `Docker installed on your machine <https://docs.docker.com/get-docker/>`_ you can run Metanome using the provided Docker container image. To do so, make sure that the environment variable *METANOME_WORKER* references the configuration file ``docker_worker.yaml`` that is `included in the config folder of this repository <https://github.com/VIDA-NYU/openclean-metanome/blob/master/config/docker_worker.yaml>`_.


Algorithms
==========

The package currently supports two data profiling algorithms.


HyFD
----

The HyFD algorithm (A Hybrid Approach to Functional Dependency Discovery) is a functional dependency discovery algorithm. Details about the algorithm can be found in:


::

    Thorsten Papenbrock, Felix Naumann
    A Hybrid Approach to Functional Dependency Discovery
    ACM International Conference on Management of Data (SIGMOD '16)


For an example of how to use the algorithm in **openclean** have a look at the example notebook `Run HyFD Algorithm - Example <https://github.com/VIDA-NYU/openclean-metanome/blob/master/examples/notebooks/RunHyFD.ipynb>`_.


HyUCC
-----

The HyUCC algorithm (A Hybrid Approach for Efficient Unique Column Combination Discovery) is a unique column combination discovery. Details about the algorithm `can be found here <https://hpi.de/fileadmin/user_upload/fachgebiete/naumann/publications/2017/paper.pdf>`_.

For an example of how to use the algorithm in **openclean** have a look at the example notebook `Run HyUCC Algorithm - Example <https://github.com/VIDA-NYU/openclean-metanome/blob/master/examples/notebooks/Run%20HyUCC.ipynb>`_.
