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


from aioredis import Redis

import pytest

from eos_metrics_proxy.app import get_app


@pytest.fixture()
async def app():
    app = await get_app()
    redis: Redis = app['redis']

    async def clear_queues():
        queues = await redis.keys('*')

        if queues:
            await redis.delete(*queues)

    await clear_queues()

    yield app

    await clear_queues()
