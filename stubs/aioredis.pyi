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


from asyncio.events import AbstractEventLoop
import ssl
from typing import Callable, List, Optional, Tuple, Type, Union


# Address can be a URL string or a 2-tuple/2-list of host, port
# https://github.com/aio-libs/aioredis/blob/master/aioredis/connection.py#L53-L56
_Address = Union[Tuple, List, str]

# This is eventually passed to asyncio:
# https://github.com/python/typeshed/blob/master/stdlib/3/asyncio/base_events.pyi#L18
_SSLContext = Union[bool, None, ssl.SSLContext]

# https://github.com/ananthb/aioredis/blob/type-annotations/aioredis/util.py#L7
_NOTSET = object()
_Encoding = Union[str, object]


async def create_redis_pool(address: _Address,
                            *,
                            db: Optional[int] = None,
                            password: Optional[str] = None,
                            ssl: Optional[_SSLContext] = None,
                            encoding: Optional[str] = None,
                            # FIXME: This is not technically correct, but works for our purpose
                            commands_factory: Type[Redis] = Redis,
                            minsize: int = 1,
                            maxsize: int = 10,
                            parser: Optional[Callable] = None,
                            timeout: Optional[int] = None,
                            # FIXME: This is not technically correct, but works for our purpose
                            pool_cls: Optional[Type[ConnectionsPool]] = None,
                            # FIXME: This is not technically correct, but works for our purpose
                            connection_cls: Optional[Type[RedisConnection]] = None,
                            loop: Optional[AbstractEventLoop] = None,
                            # FIXME: This is not technically correct, but works for our purpose
                            ) -> Redis: ...


class ConnectionsPool: ...
class RedisConnection: ...


class Redis:
    async def lpush(self, key: Union[bytes, str], value: Union[bytes, str]) -> int: ...
    async def keys(self, pattern: Union[bytes, str]) -> List[bytes]: ...
    async def delete(self, key: Union[bytes, str], *keys: Union[bytes, str]) -> int: ...
