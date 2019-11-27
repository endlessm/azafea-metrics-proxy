# Copyright (c) 2019 - Endless
#
# This file is part of azafea-metrics-proxy
#
# azafea-metrics-proxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# azafea-metrics-proxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with azafea-metrics-proxy.  If not, see <http://www.gnu.org/licenses/>.


import pytest

import azafea_metrics_proxy.cli
import azafea_metrics_proxy.config


def test_print_config(capfd, make_config_file):
    config_file = make_config_file({
        'redis': {'host': 'redis-server'},
    })
    azafea_metrics_proxy.cli.run_command('-c', str(config_file), 'print-config')

    capture = capfd.readouterr()
    assert capture.out.strip() == '\n'.join([
        '----- BEGIN -----',
        '[main]',
        'verbose = false',
        '',
        '[redis]',
        'host = "redis-server"',
        'port = 6379',
        'password = "** hidden **"',
        '------ END ------',
    ])


def test_print_invalid_config(capfd, make_config_file):
    # Make a wrong config file
    config_file = make_config_file({'main': {'verbose': 'blah'}})

    with pytest.raises(azafea_metrics_proxy.cli.InvalidConfigExit):
        azafea_metrics_proxy.cli.run_command('-c', str(config_file), 'print-config')

    capture = capfd.readouterr()
    assert "Invalid configuration:\n* main.verbose: 'blah' is not a boolean" in capture.err


def test_run(capfd, monkeypatch, make_config_file):
    def mock_run_app(app):
        print('Running the mock app…')

        # This is a coroutine, close it
        app.close()

    config_file = make_config_file({})

    with monkeypatch.context() as m:
        m.setattr(azafea_metrics_proxy.cli, 'run_app', mock_run_app)
        azafea_metrics_proxy.cli.run_command('-c', str(config_file), 'run')

    capture = capfd.readouterr()
    assert 'Running the mock app…' in capture.out


def test_run_invalid_config(capfd, make_config_file):
    # Make a wrong config file
    config_file = make_config_file({'main': {'verbose': 'blah'}})

    with pytest.raises(azafea_metrics_proxy.cli.InvalidConfigExit):
        azafea_metrics_proxy.cli.run_command('-c', str(config_file), 'run')

    capture = capfd.readouterr()
    assert "Invalid configuration:\n* main.verbose: 'blah' is not a boolean" in capture.err


def test_run_redis_invalid_host(capfd, make_config_file):
    # Hopefully nobody will ever run the tests with a Redis server accessible at this host:port
    config_file = make_config_file({
        'redis': {'host': 'no-such-host', 'port': 1},
    })

    with pytest.raises(azafea_metrics_proxy.cli.ConnectionErrorExit):
        azafea_metrics_proxy.cli.run_command('-c', str(config_file), 'run')

    capture = capfd.readouterr()
    assert 'Could not connect to Redis:' in capture.err
    assert 'Name or service not known' in capture.err
