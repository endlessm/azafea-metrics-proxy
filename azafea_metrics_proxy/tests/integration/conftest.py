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


from aioredis import Redis

import pytest

from azafea_metrics_proxy.app import get_app


@pytest.fixture()
async def app(make_config):
    config = make_config({})

    app = await get_app(config)
    redis: Redis = app['redis']

    async def clear_queues():
        queues = await redis.keys('*')

        if queues:
            await redis.delete(*queues)

    await clear_queues()

    yield app

    await clear_queues()
