# Copyright (c) 2019 - Endless
#
# This file is part of Azafea
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import eos_metrics_proxy.cli
import eos_metrics_proxy.config


def test_print_config(capfd, make_config_file):
    config_file = make_config_file({
        'redis': {'host': 'redis-server'},
    })

    args = eos_metrics_proxy.cli.parse_args([
        '-c', str(config_file),
        'print-config',
    ])

    result = args.subcommand(args)

    assert result == eos_metrics_proxy.cli.ExitCode.OK

    capture = capfd.readouterr()
    assert capture.out.strip() == '\n'.join([
        '[main]',
        'verbose = false',
        '',
        '[redis]',
        'host = "redis-server"',
        'port = 6379',
        'password = "** hidden **"',
    ])


def test_print_invalid_config(capfd, make_config_file):
    # Make a wrong config file
    config_file = make_config_file({'main': {'verbose': 'blah'}})

    args = eos_metrics_proxy.cli.parse_args([
        '-c', str(config_file),
        'print-config',
    ])

    result = args.subcommand(args)

    assert result == eos_metrics_proxy.cli.ExitCode.INVALID_CONFIG

    capture = capfd.readouterr()
    assert "Invalid [main] configuration:\n* verbose: 'blah' is not a boolean" in capture.err


def test_run(capfd, monkeypatch, make_config_file):
    def mock_run_app(app):
        print('Running the mock app…')

        # This is a coroutine, close it
        app.close()

    config_file = make_config_file({})

    args = eos_metrics_proxy.cli.parse_args([
        '-c', str(config_file),
        'run',
    ])

    with monkeypatch.context() as m:
        m.setattr(eos_metrics_proxy.cli, 'run_app', mock_run_app)
        result = args.subcommand(args)

    assert result == eos_metrics_proxy.cli.ExitCode.OK

    capture = capfd.readouterr()
    assert 'Running the mock app…' in capture.out


def test_run_invalid_config(capfd, make_config_file):
    # Make a wrong config file
    config_file = make_config_file({'main': {'verbose': 'blah'}})

    args = eos_metrics_proxy.cli.parse_args([
        '-c', str(config_file),
        'run',
    ])

    result = args.subcommand(args)

    assert result == eos_metrics_proxy.cli.ExitCode.INVALID_CONFIG

    capture = capfd.readouterr()
    assert "Invalid [main] configuration:\n* verbose: 'blah' is not a boolean" in capture.err


def test_run_redis_connection_error(capfd, make_config_file):
    # Hopefully nobody will ever run the tests with a Redis server accessible at this host:port
    config_file = make_config_file({
        'redis': {'host': 'no-such-host', 'port': 1},
    })

    args = eos_metrics_proxy.cli.parse_args([
        '-c', str(config_file),
        'run',
    ])

    result = args.subcommand(args)

    assert result == eos_metrics_proxy.cli.ExitCode.CONNECTION_ERROR

    capture = capfd.readouterr()
    assert 'Could not connect to Redis:' in capture.err
    assert 'Name or service not known' in capture.err
