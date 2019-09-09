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


from datetime import datetime, timezone

from freezegun import freeze_time

import pytest

from eos_metrics_proxy.utils import get_timestamp, utcnow


@pytest.mark.parametrize('dt, expected', [
    pytest.param(datetime(1970, 1, 1, tzinfo=timezone.utc),
                 b'\x00\x00\x00\x00\x00\x00\x00\x00',
                 id='epoch'),
    pytest.param(datetime(2019, 9, 9, 15, 38, tzinfo=timezone.utc),
                 b'\x00&\x9e\x92 \x92\x05\x00',
                 id='right-now'),
])
def test_get_timestamp(dt, expected):
    assert get_timestamp(dt) == expected


@pytest.mark.parametrize('expected', [
    pytest.param(datetime(1970, 1, 1, tzinfo=timezone.utc),
                 id='epoch'),
    pytest.param(datetime(2019, 9, 9, 15, 38, tzinfo=timezone.utc),
                 id='right-now'),
])
def test_utcnow(expected):
    with freeze_time(expected):
        now = utcnow()

    assert now == expected
