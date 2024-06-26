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


# This whole file is almost copy-pasted from Azafea.
# TODO: Can we share most of this into its own module?


import dataclasses
import logging
import os
from typing import Any, List, MutableMapping

from pydantic import field_validator, ValidationError
from pydantic.dataclasses import dataclass
from pydantic_core import ErrorDetails

import toml

from ._validators import is_boolean, is_non_empty_string, is_strictly_positive_integer


log = logging.getLogger(__name__)

DEFAULT_PASSWORD = 'CHANGE ME!!'


class InvalidConfigurationError(Exception):
    def __init__(self, errors: List[ErrorDetails]) -> None:
        self.errors = errors

    def __str__(self) -> str:
        msg = ['Invalid configuration:']

        for e in self.errors:
            loc = self._loc_str(e)
            msg.append(f"* {loc}: {e['msg']}")

        return '\n'.join(msg)

    # The loc field in ErrorDetails is a tuple of strings and ints.
    # https://docs.pydantic.dev/latest/errors/errors/#customize-error-messages
    @staticmethod
    def _loc_str(details: ErrorDetails) -> str:
        path = ''
        for i, element in enumerate(details['loc']):
            if isinstance(element, str):
                if i > 0:
                    path += '.'
                path += element
            else:  # pragma: no cover (our config does not use lists)
                path += f'[{element}]'
        return path


class NoSuchConfigurationError(AttributeError):
    pass


class _Base:
    def __getattr__(self, name: str) -> Any:
        raise NoSuchConfigurationError(f'No such configuration option: {name!r}')


@dataclass(frozen=True)
class Main(_Base):
    verbose: bool = False

    @field_validator('verbose', mode='before')
    def verbose_is_boolean(cls, value: Any) -> bool:
        return is_boolean(value)


@dataclass(frozen=True)
class Redis(_Base):
    host: str = 'localhost'
    port: int = 6379
    password: str = DEFAULT_PASSWORD
    ssl: bool = False

    @field_validator('host', mode='before')
    def host_is_non_empty_string(cls, value: Any) -> str:
        return is_non_empty_string(value)

    @field_validator('port', mode='before')
    def port_is_strictly_positive_integer(cls, value: Any) -> int:
        return is_strictly_positive_integer(value)


@dataclass(frozen=True)
class Config(_Base):
    main: Main = dataclasses.field(default_factory=Main)
    redis: Redis = dataclasses.field(default_factory=Redis)

    def __post_init__(self) -> None:
        self.warn_about_default_passwords()

    @classmethod
    def from_file(cls, config_file_path: str) -> 'Config':
        overrides: MutableMapping[str, Any] = {}

        if os.path.exists(config_file_path):
            overrides = toml.load(config_file_path)

        try:
            return cls(**overrides)

        except ValidationError as e:
            raise InvalidConfigurationError(e.errors())

    def warn_about_default_passwords(self) -> None:
        if self.redis.password == DEFAULT_PASSWORD:
            log.warning('Did you forget to change the Redis password?')

    def __str__(self) -> str:
        redis_no_password = dataclasses.replace(self.redis, password='** hidden **')
        self_no_passwords = dataclasses.replace(self, redis=redis_no_password)

        return toml.dumps(dataclasses.asdict(self_no_passwords)).strip()
