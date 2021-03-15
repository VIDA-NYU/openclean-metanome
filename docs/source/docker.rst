.. _docker-ref:

Docker Container for Metanome Algorithms
========================================

Build the container containing the Metanome.jar file:

.. code-block:: bash

    docker image build -t openclean-metanome:0.1.0 .


Push container image to DockerHub.

.. code-block:: bash

    docker image tag openclean-metanome:0.1.0 heikomueller/openclean-metanome:0.1.0
    docker image push heikomueller/openclean-metanome:0.1.0
