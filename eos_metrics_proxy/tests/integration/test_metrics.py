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


from eos_metrics_proxy.app import get_app


async def test_put_metrics_request(aiohttp_client):
    app = get_app()
    client = await aiohttp_client(app)

    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x945w\x00\x00\x00\x00\x00\xa5E\x04'
                       b'\xd2\xbc\xc2\x15\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff(((')
    response = await client.put(f'/{version}/{sha512}', data=metrics_request)

    assert response.status == 200
    assert await response.text() == 'OK'


async def test_put_metrics_request_empty_body(aiohttp_client):
    app = get_app()
    client = await aiohttp_client(app)

    version = 2
    sha512 = ('3eaab42c4ea4c201a726f44b82e51b52f0a587399a59c32f92b4634b60fef0c5f3fbaec705a8a6d7dad'
              '216d48b3a948ced2be27efb4547ea3bf657d437aec838')
    metrics_request = b''
    response = await client.put(f'/{version}/{sha512}', data=metrics_request)

    assert response.status == 400
    assert await response.text() == 'Invalid request: empty body'


async def test_put_metrics_request_invalid_hash(aiohttp_client):
    app = get_app()
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
