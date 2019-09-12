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


# TODO: Ask upstream whether they want type annotations in their code, or would be open to having
# stubs in typeshed


from datetime import date, timedelta
from typing import Callable, Generator, List, Optional, Union


# https://github.com/spulec/freezegun/blob/master/freezegun/api.py#L495
class _freeze_time: ...

def freeze_time(time_to_freeze: Optional[Union[str, date, timedelta, Callable, Generator]] = None,
                tz_offset: Union[int, timedelta] = 0,
                ignore: List = None,
                tick: bool = False,
                as_arg: bool = False,
                auto_tick_seconds: int = 0) -> _freeze_time: ...
