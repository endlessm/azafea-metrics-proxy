# Azafea Metrics Proxy

The Azafea metrics proxy is part of the server backend for the Endless usage
metrics gathering and processing.

![Endless metrics pipeline diagram](docs/source/_static/metrics-pipeline.png "The Endless metrics pipeline")

The metrics proxy is responsible for receiving the metrics requests from the
clients and passing them for processing to Azafea through Redis.

For more details on other parts of the architecture, see:

* [eos-activation-server](https://github.com/endlessm/eos-activation-server/)
* [Azafea](https://github.com/endlessm/azafea/)

Find out more about the Azafea metrics proxy and how to use it
[in our documentation](docs/source/).


# Contributing

Please read our [contribution guidelines](CONTRIBUTING.md) for details.


# License

This project is offered under the terms of the
[Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html),
either version 3 of the License, or (at your option) any later version.
