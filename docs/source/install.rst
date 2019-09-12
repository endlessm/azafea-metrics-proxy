==========
Deployment
==========


.. _pre-requisites:

Pre-requisites
==============

The Azafea metrics proxy pushes events to `Redis <https://redis.io>`_, which
needs to be installed and accessible.

Redis can be installed in multiple ways depending on your operating system. A
simple installation method is to use `Docker <https://www.docker.com>`_, which
we will detail below.

.. note::
    Some operating systems provide `Podman <https://podman.io>`_ instead of
    Docker. For the purpose of this guide, both should be entirely equivalent.
    If you use Podman, simply replace ``sudo docker`` by ``podman`` (no sudo
    required) in all the commands below.

Redis
-----

Installing and running Redis with Docker should be as simple as::

    $ sudo docker pull redis:latest
    $ sudo docker run --publish=6379:6379 redis:latest

If you want Redis to require a password, or for any other local configuration,
you can create the ``/etc/redis/redis.conf`` file with something like the
following:

.. code-block:: none

   requirepass S3cretRedisP@ssw0rd

Then instead of the command above, run Redis as follows::

    $ sudo docker run --publish=6379:6379 \
                      --volume=/etc/redis/redis.conf:/etc/redis/redis.conf:ro \
                      redis:latest redis-server /etc/redis/redis.conf

Azafea Metrics Proxy
--------------------

The easiest deployment method is also to use Docker.

You need to first get the sources and build the Docker image::

    $ git clone https://github.com/endlessm/azafea-metrics-proxy
    $ cd azafea-metrics-proxy
    $ sudo docker build --tag azafea-metrics-proxy .

At this point you will probably want to
:doc:`write a local configuration file <configuration>` before running the
Azafea metrics proxy.

In particular, you will at the very least want to:

* change the Redis host, to point them to the IP address of its container;
* change the Redis password.

We recommend saving the configuration file as
``/etc/azafea-metrics-proxy/config.toml`` on the production host.


Running
=======

.. note::
    The commands  below all assume that your config file is at
    ``/etc/azafea-metrics-proxy/config.toml``. If you saved it elsewhere, you
    will need to adapt the ``--volume`` argument.

Once you built the Docker image and wrote your configuration file, you can
ensure that the Azafea metrics proxy loads your configuration correctly with
the following command::

    $ sudo docker run --volume=/etc/azafea-metrics-proxy:/etc/azafea-metrics-proxy:ro proxy print-config

Finally, you can run the Azafea metrics proxy::

    $ sudo docker run --volume=/etc/azafea-metrics-proxy:/etc/azafea-metrics-proxy:ro proxy run
