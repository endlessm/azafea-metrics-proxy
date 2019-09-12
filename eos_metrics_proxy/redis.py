# Copyright (c) 2019 - Endless
#
# This file is part of eos-metrics-proxy
#
# eos-metrics-proxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# eos-metrics-proxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with eos-metrics-proxy.  If not, see <http://www.gnu.org/licenses/>.


import socket

import aioredis


class ConnectionError(Exception):
    pass


async def connect(host: str, port: int, password: str) -> aioredis.Redis:
    try:
        return await aioredis.create_redis_pool(f'redis://:{password}@{host}:{port}')

    except socket.gaierror as e:
        raise ConnectionError(e)
