=============
Configuration
=============

The Azafea metrics proxy can run without any configuration, using reasonable
defaults for its options.

However many things can be configured in a
`TOML <https://github.com/toml-lang/toml>`_ configuration file, usually located
at ``/etc/azafea-metrics-proxy/config.toml``.

You don't need to write a full configuration file. The Azafea metrics proxy
will let you write only the sections and options you want to override.

Before detailing every option, here is an example configuration file showing
the default options:

.. code-block:: toml

   [main]
   verbose = false

   [redis]
   host = "localhost"
   port = 6379
   password = "CHANGE ME!!"


The ``main`` table
==================

This section controls the general behaviour of the Azafea metrics proxy.

``verbose`` (boolean)
  This option controls how verbose Azafea will be. If True, Azafea will log
  everything, including debug messages. Otherwise only informative, warning
  and error messages are logged.

  The default is ``false``


The ``redis`` table
===================

This section controls how Azafea connects to the Redis server holding the event
queues.

``host`` (string)
  The hostname on which the Redis server is accessible.

  The default is ``"localhost"``.

``port`` (strictly positive integer)
  The port on which the Redis server is listening.

  The default is ``6379``.

``password`` (string)
  The password Redis expects when connecting to it.

  The default is ``"CHANGE ME!!"``.
