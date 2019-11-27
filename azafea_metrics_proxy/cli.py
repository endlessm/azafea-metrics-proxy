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


import argparse
from enum import IntEnum
import logging
from typing import List
import sys

from aiohttp.web import run_app

from .app import get_app
from .config import Config, InvalidConfigurationError
from .logging import setup_logging
from . import redis


log = logging.getLogger(__name__)


class ExitCode(IntEnum):
    OK = 0
    INVALID_CONFIG = -1
    CONNECTION_ERROR = -2
    UNKNOWN_ERROR = -3


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='azafea-metrics-proxy',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c', '--config', default='/etc/azafea-metrics-proxy/config.toml',
                        help='Optional path to a configuration file, if needed')

    subs = parser.add_subparsers(title='subcommands', dest='subcommand', required=True)

    print_config = subs.add_parser('print-config',
                                   help='Print the loaded configuration then exit')
    print_config.set_defaults(subcommand=do_print_config)

    run = subs.add_parser('run', help='Run azafea-metrics-proxy')
    run.set_defaults(subcommand=do_run)

    return parser


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = get_parser()

    return parser.parse_args(args)


def do_print_config(args: argparse.Namespace) -> int:
    try:
        config = Config.from_file(args.config)

    except InvalidConfigurationError as e:
        print(str(e), file=sys.stderr)
        return ExitCode.INVALID_CONFIG

    setup_logging(verbose=config.main.verbose)

    print(config)

    return ExitCode.OK


def do_run(args: argparse.Namespace) -> int:
    try:
        config = Config.from_file(args.config)

    except InvalidConfigurationError as e:
        print(str(e), file=sys.stderr)
        return ExitCode.INVALID_CONFIG

    setup_logging(verbose=config.main.verbose)

    try:
        run_app(get_app(config))

    except redis.ConnectionError as e:
        log.error('Could not connect to Redis: %s', e)
        return ExitCode.CONNECTION_ERROR

    return ExitCode.OK
