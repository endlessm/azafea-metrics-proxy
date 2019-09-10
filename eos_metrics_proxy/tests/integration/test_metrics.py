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


import bz2
import gzip

from aioredis import Redis

from freezegun import freeze_time

import pytest

from eos_metrics_proxy.app import get_app
from eos_metrics_proxy.utils import get_timestamp, utcnow


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


async def test_put_metrics_request(aiohttp_client, app):
    client = await aiohttp_client(app)

    now = utcnow()
    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x945w\x00\x00\x00\x00\x00\xa5E\x04'
                       b'\xd2\xbc\xc2\x15\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff(((')

    with freeze_time(now):
        response = await client.put(f'/{version}/{sha512}', data=metrics_request)

    assert response.status == 200
    assert await response.text() == 'OK'

    assert await app['redis'].llen('metrics-2') == 1
    assert await app['redis'].rpop('metrics-2') == get_timestamp(now) + metrics_request


async def test_put_gzipped_metrics_request(aiohttp_client, app):
    client = await aiohttp_client(app)

    now = utcnow()
    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x945w\x00\x00\x00\x00\x00\xa5E\x04'
                       b'\xd2\xbc\xc2\x15\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff(((')
    compressed_request = gzip.compress(metrics_request)

    with freeze_time(now):
        response = await client.put(f'/{version}/{sha512}',
                                    headers={'X-Endless-Content-Encoding': 'gzip'},
                                    data=compressed_request)

    assert response.status == 200
    assert await response.text() == 'OK'

    assert await app['redis'].llen('metrics-2') == 1
    assert await app['redis'].rpop('metrics-2') == get_timestamp(now) + metrics_request


async def test_put_compressed_metrics_request_unknown_compression(aiohttp_client, app):
    client = await aiohttp_client(app)

    now = utcnow()
    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x945w\x00\x00\x00\x00\x00\xa5E\x04'
                       b'\xd2\xbc\xc2\x15\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff(((')
    compressed_request = bz2.compress(metrics_request)

    with freeze_time(now):
        response = await client.put(f'/{version}/{sha512}',
                                    headers={'X-Endless-Content-Encoding': 'bzip2'},
                                    data=compressed_request)

    assert response.status == 400
    assert await response.text() == 'Unknown request encoding: bzip2'

    assert await app['redis'].llen('metrics-2') == 0


async def test_put_metrics_request_empty_body(aiohttp_client, app):
    client = await aiohttp_client(app)

    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = b''
    response = await client.put(f'/{version}/{sha512}', data=metrics_request)

    assert response.status == 400
    assert await response.text() == 'Invalid request: empty body'

    assert await app['redis'].llen('metrics-2') == 0


async def test_put_metrics_request_invalid_hash(aiohttp_client, app):
    client = await aiohttp_client(app)

    version = 2
    bad_sha512 = ('0000000000000000000000000000000000000000000000000000000000000000000000000000000'
                  '0000000000000000000000000000000000000000000000000')
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x945w\x00\x00\x00\x00\x00\xa5E\x04'
                       b'\xd2\xbc\xc2\x15\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff(((')
    response = await client.put(f'/{version}/{bad_sha512}', data=metrics_request)

    assert response.status == 400
    assert await response.text() == f'SHA512 mismatch: expected {bad_sha512} but got {sha512}'

    assert await app['redis'].llen('metrics-2') == 0
