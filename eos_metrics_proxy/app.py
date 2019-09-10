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


from aiohttp.web import Application

import aioredis

from . import metrics


async def get_app() -> Application:
    app = Application()

    metrics.setup_routes(app)

    # TODO: Make this configurable
    redis_host = 'localhost'
    redis_port = 6379
    redis_password = 'CHANGE ME!!'

    app['redis'] = await aioredis.create_redis_pool(
        f'redis://:{redis_password}@{redis_host}:{redis_port}')

    return app
