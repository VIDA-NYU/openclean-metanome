# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2020 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Create instances of the metanome engine based on the configuration
settings in the environment.
"""

from openclean_metanome.engine.base import MetanomeEngine


def get_engine() -> MetanomeEngine:
    """Create an instance of the metanome engine based on the current values
    in the respective environment variables.

    Returns
    -------
    openclean_metanome.engine.base.MetanomeEngine
    """
    from openclean_metanome.engine.proc import SubprocEngine
    return SubprocEngine()
