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


import hashlib

from aiohttp.web import Application, HTTPBadRequest, Request, Response


async def new_metrics_request(request: Request) -> Response:
    # This is safe as long as the route regexp mandates an integer
    version = int(request.match_info['version'])

    body = await request.read()

    if not body:
        raise HTTPBadRequest(text='Invalid request: empty body')

    provided_hash = request.match_info['provided_hash']
    hash = hashlib.sha512(body).hexdigest()

    if hash != provided_hash:
        raise HTTPBadRequest(text=f'SHA512 mismatch: expected {provided_hash} but got {hash}')

    # TODO: Send to Redis

    return Response(text='OK')


def setup_routes(app: Application) -> None:
    app.router.add_put(r'/{version:\d+}/{provided_hash:[0-9a-f]{128}}', new_metrics_request)