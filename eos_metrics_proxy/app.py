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

from . import redis
from .config import Config
from .views import metrics
from .views import compat


async def on_shutdown(app: Application) -> None:
    app['redis'].close()
    await app['redis'].wait_closed()


async def get_app(config: Config) -> Application:
    app = Application()

    compat.setup_routes(app)
    metrics.setup_routes(app)

    app['redis'] = await redis.connect(config.redis.host, config.redis.port, config.redis.password)
    app.on_shutdown.append(on_shutdown)

    return app
