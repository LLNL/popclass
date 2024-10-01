===============
Developer Guide
===============

In order to help develop popclass, the library should be installed from source.
See `Installation`_ for installation steps.

Working in the Dev Container
----------------------------

For convenience, we include a Dockerfile for development within the container.
Instructions on installing Docker and its basic usage can be found on the `Docker Website <https://www.docker.com/>`_.

To build the container:

.. code-block:: console

    cd popclass
    docker build ./

This will build the Docker image.
To check that it has built correctly, run the test suite:

.. code-block:: console

    docker run popclass:latest pytest tests

