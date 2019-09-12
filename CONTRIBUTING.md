# Contributing
  
Thank you for considering contributing to this project.

Following these guidelines helps to communicate that you respect the time of
the developers managing and developing this project.

In return, we will reciprocate that respect in addressing your issues,
assessing changes, and helping you finalize your contributions in a timely
manner.


## Filing Issues

Whenever you experience a problem with this software, please let us know so we
can make it better.

But first, take the time to search through the list of [existing issues] to see
whether it is already known.

Be sure to provide all the information you can, as that will really help us
fixing your issue as quickly as possible.

[existing issues]: https://github.com/endlessm/azafea-metrics-proxy/issues


## Pre-requisites

The tools required to work on the Azafea metrics proxy are the following:

*   Python >= 3.7, with Pip
*   [pipenv](https://docs.pipenv.org/)

Pipenv is not strictly mandatory to contribute to the Azafea metrics proxy, you
can use any way you prefer to manage the dependencies. We do recommend using it
though, as it makes it very easy to manage a virtual environment dedicated to
the Azafea metrics proxy. The rest of this documentation will assume you use
Pipenv.


## Getting the Sources

You can simply clone the Git repository:

```
$ git clone https://github.com/endlessm/azafea-metrics-proxy
```

At this point you will want to install the runtime and development
dependencies:

```
$ pipenv install --dev
```

Now try running the unit tests:

```
$ pipenv run test
```


## Coding Standards

In order to keep the code readable and avoid common mistakes, we use
[flake8](https://pypi.org/project/flake8/) a common linter in the Python
community.

We also use type checking with [mypy](http://www.mypy-lang.org/), which
prevents a lot of problems inherent to dynamically typed languages like Python.

Both are run automatically with the following command:

```
$ pipenv run lint
```


## Writing Unit Tests

Unit tests are simply files in the `azafea_metrics_proxy/tests/` directory.
They must be named `test_*.py`, and we use [Pytest](https://pytest.org/) to
help us write them.

Feel free to mock liberally as you need it with the
[`monkeypatch`](https://docs.pytest.org/en/latest/monkeypatch.html) fixture.
Unit tests should generally not require additional dependencies from what
the Azafea metrics proxy itself requires. They should specifically not require:

* access to an external service like Redis;
* any kind of network access.

You can run them with the following command:

```
$ pipenv run test
```


## Writing Integration Tests

Integration tests are a bit more involved and require more set up before they
can run. They have the same requirements as
[running the Azafea metrics proxy in production](docs/source/install.rst) so
see that documentation to install things like Redis.

Once you have everything set up, you can run all the tests, unit and
integration, with a single command:

```
$ pipenv run test-all
```

Integration tests consist of files under
`azafea_metrics_proxy/tests/integration/` named `test_*.py`, as that is how
Pytest finds the tests to run.

Look at existing integration tests for examples.


## Running a Local Instance

Running a local instance has the same requirement as running the Azafea metrics
proxy in production or running the integration tests (see above). If you
managed to have all the integration tests passing, then the local instance
should run properly.

One additional thing you will need to do is
[write a configuration file](docs/source/configuration.rst). In particular you
might want to:

* change the Redis host, to point it to the IP addresses of its container;
* change the Redis password.

Once you're ready, you can ensure that the Azafea metrics proxy loads your
configuration correctly with the following command:

```
$ pipenv run proxy -c config.toml print-config
```

Finally, you can run the Azafea metrics proxy itself:

```
$ pipenv run proxy -c config.toml run
```

