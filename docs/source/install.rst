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

The easiest deployment method is also to use Docker. The image is published on
`Docker Hub`_ and can be downloaded by running ``sudo docker pull
docker.io/endlessm/azafea-metrics-proxy``.

.. _Docker Hub: https://hub.docker.com/r/endlessm/azafea-metrics-proxy

If you prefer, you can first get the sources and build the Docker image
locally::

    $ git clone https://github.com/endlessm/azafea-metrics-proxy
    $ cd azafea-metrics-proxy
    $ sudo docker build --tag azafea-metrics-proxy .

At this point you need to configure the Azafea metrics proxy. In particular,
you will at the very least want to:

* change the Redis host, to point them to the IP address of its container;
* change the Redis password.

The container will automatically generate a :doc:`configuration file
<configuration>` from environment variables. The supported environment
variables are:

* ``VERBOSE``: Sets the ``main.verbose`` value. (Default: ``false``)
* ``REDIS_HOST``: Sets the ``redis.host`` value. (Default: ``localhost``)
* ``REDIS_PORT``: Sets the ``redis.port`` value. (Default: ``6379``)
* ``REDIS_PASSWORD``: Sets the ``redis.password`` value. (Default: ``CHANGE
  ME!!``)
* ``REDIS_SSL``: Sets the ``redis.ssl`` value. (Default: ``false``)

Alternatively, you can :doc:`write a local configuration file <configuration>`
before running the Azafea metrics proxy. This requires running the Docker
container differently as described below.


Running
=======

.. note::

    The commands below all assume that you're using the Docker Hub image with
    environment variable configuration. If you're using a built image, adapt
    the ``docker.io/endlessm/azafea-metrics-proxy`` argument to use the tag you
    passed in ``--tag``. See the end of this section if you want to use a local
    configuration file.

Once you've pulled the Docker image and written your configuration file, you
can ensure that the Azafea metrics proxy loads your configuration correctly
with the following command::

    $ sudo docker run --env=REDIS_HOST=redis.example.com \
                      --env=REDIS_PASSWORD=mypassword \
                      --env=REDIS_SSL=false \
                      docker.io/endlessm/azafea-metrics-proxy \
                      print-config

Finally, you can run the Azafea metrics proxy::

    $ sudo docker run --env=REDIS_HOST=redis.example.com \
                      --env=REDIS_PASSWORD=mypassword \
                      --env=REDIS_SSL=false \
                      docker.io/endlessm/azafea-metrics-proxy \
                      run

If you're using a local configuration file, 2 changes are needed. First, rather
than passing ``--env`` to ``docker run``, the file needs to be mounted into the
container using the ``--volume`` option. For example,
``--volume=/path/to/config.toml:/config.toml:ro`` would mount the configuration
file at ``/path/to/config.toml`` to ``/config.toml`` within the container and
makes it read-only.

Second, Azafea metrics proxy needs to be told about the location of the
configuration within the container. This needs to be passed as the first
argument in the container command using the ``-c`` option. For example, ``-c
/config.toml print-config``.
