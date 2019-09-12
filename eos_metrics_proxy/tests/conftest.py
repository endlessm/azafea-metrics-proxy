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


from pathlib import Path
from typing import Mapping

import pytest

import toml

from eos_metrics_proxy.config import Config


def pytest_collection_modifyitems(items):
    for item in items:
        markers = [m for m in item.own_markers if m.name in ('flake8', 'mypy')]

        if markers:
            continue

        if item.nodeid.startswith('eos_metrics_proxy/tests/integration/'):
            item.add_marker(pytest.mark.integration)


@pytest.fixture()
def make_config_file(tmp_path):
    config_file_path = tmp_path.joinpath('eos_metrics_proxy.conf')

    def maker(d: Mapping) -> Path:
        with config_file_path.open('w') as f:
            toml.dump(d, f)

        return config_file_path

    return maker


@pytest.fixture()
def make_config(make_config_file):
    def maker(d: Mapping) -> Config:
        config_file_path = make_config_file(d)

        return Config.from_file(str(config_file_path))

    return maker
