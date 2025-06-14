# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Retry wrappers for OpenAI API calls."""

from __future__ import annotations

from typing import Callable, TypeVar
from tenacity import retry, stop_after_attempt, wait_exponential

T = TypeVar("T")


def retry_guard(fn: Callable[..., T]) -> Callable[..., T]:
    """Retry ``fn`` with exponential backoff on failure."""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
