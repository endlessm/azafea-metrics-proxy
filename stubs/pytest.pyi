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


from typing import Any, Callable, List, Optional


def fixture(scope: str = "function",
            params: Optional[List[Any]] = None,
            autouse: bool = False,
            ids: Optional[List[str]] = None,
            name: Optional[str] = None) -> Callable: ...

class mark:
    @staticmethod
    def parametrize(names: str, params: List[Any]) -> Callable: ...

def param(*values: Any, id: Optional[str] = None) -> Callable: ...
