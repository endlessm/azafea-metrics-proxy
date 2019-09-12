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


import pytest


@pytest.mark.parametrize('path', [
    '/',
    '/something',
    '/something/else',
    '/something?key1=value1&key2=value2',
])
async def test_get(aiohttp_client, app, path):
    client = await aiohttp_client(app)

    response = await client.get(path)

    assert response.status == 200
    assert await response.text() == '<html>\n<body>\nOK\n</body>\n</html>\n'


@pytest.mark.parametrize('path', [
    '/',
    '/something',
    '/something/else',
])
@pytest.mark.parametrize('data', [
    None,
    b'',
    b'something',
])
async def test_post(aiohttp_client, app, path, data):
    client = await aiohttp_client(app)

    response = await client.post(path, data=data)

    assert response.status == 200
    assert await response.text() == ''
