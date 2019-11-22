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

import azafea_metrics_proxy.config
from azafea_metrics_proxy.logging import setup_logging


def test_defaults():
    config = azafea_metrics_proxy.config.Config()

    assert not config.main.verbose
    assert config.redis.host == 'localhost'
    assert config.redis.port == 6379

    assert str(config) == '\n'.join([
        '[main]',
        'verbose = false',
        '',
        '[redis]',
        'host = "localhost"',
        'port = 6379',
        'password = "** hidden **"',
    ])


def test_get_nonexistent_option():
    config = azafea_metrics_proxy.config.Config()

    with pytest.raises(azafea_metrics_proxy.config.NoSuchConfigurationError) as exc_info:
        config.main.gauche

    assert f"No such configuration option: 'gauche'" in str(exc_info.value)


def test_override(monkeypatch, make_config):
    config = make_config({
        'main': {'verbose': True},
        'redis': {'port': 42},
    })

    assert config.main.verbose
    assert config.redis.host == 'localhost'
    assert config.redis.port == 42

    assert str(config) == '\n'.join([
        '[main]',
        'verbose = true',
        '',
        '[redis]',
        'host = "localhost"',
        'port = 42',
        'password = "** hidden **"',
    ])


def test_override_with_nonexistent_file():
    config = azafea_metrics_proxy.config.Config.from_file('/no/such/file')

    # Ensure we got the defaults
    assert config == azafea_metrics_proxy.config.Config()


@pytest.mark.parametrize('value', [
    42,
    'true',
])
def test_override_verbose_invalid(make_config, value):
    with pytest.raises(azafea_metrics_proxy.config.InvalidConfigurationError) as exc_info:
        make_config({'main': {'verbose': value}})

    assert ('Invalid configuration:\n'
            f'* main.verbose: {value!r} is not a boolean') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_redis_host_invalid(make_config, value):
    with pytest.raises(azafea_metrics_proxy.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'host': value}})

    assert ('Invalid configuration:\n'
            f'* redis.host: {value!r} is not a string') in str(exc_info.value)


def test_override_redis_host_empty(make_config):
    with pytest.raises(azafea_metrics_proxy.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'host': ''}})

    assert ('Invalid configuration:\n'
            f"* redis.host: '' is empty") in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    'foo',
])
def test_override_redis_port_invalid(make_config, value):
    with pytest.raises(azafea_metrics_proxy.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'port': value}})

    assert ('Invalid configuration:\n'
            f'* redis.port: {value!r} is not an integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    -1,
    0,
])
def test_override_redis_port_not_positive(make_config, value):
    with pytest.raises(azafea_metrics_proxy.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'port': value}})

    assert ('Invalid configuration:\n'
            f'* redis.port: {value!r} is not a strictly positive integer') in str(exc_info.value)


def test_default_passwords(capfd):
    setup_logging(verbose=False)
    config = azafea_metrics_proxy.config.Config()
    config.warn_about_default_passwords()

    capture = capfd.readouterr()
    assert 'Did you forget to change the Redis password?' in capture.err


def test_non_default_passwords(capfd, make_config):
    setup_logging(verbose=False)
    config = make_config({
        'redis': {'password': 'not default'},
    })
    config.warn_about_default_passwords()

    capture = capfd.readouterr()
    assert 'Did you forget to change the Redis password?' not in capture.err
