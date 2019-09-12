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


from aiohttp.web import Application, Request, Response


# Some old client machines run old versions of the metrics reporting code.
#
# Those old machines might keep retrying over and over until they succeed, potentially leading to
# a DDoS of our service.
#
# This file implement compatibility views just so those old clients have a response.
#
# We ignore the metrics though because those clients are so old they wouldn't be interesting.


async def get(request: Request) -> Response:
    return Response(text='<html>\n<body>\nOK\n</body>\n</html>\n')


async def post(request: Request) -> Response:
    return Response()


def setup_routes(app: Application) -> None:
    app.router.add_get(r'/{tail:.*}', get)
    app.router.add_post(r'/{tail:.*}', post)
