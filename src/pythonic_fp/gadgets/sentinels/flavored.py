# Copyright 2023-2026 Geoffrey R. Scheller
#
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

from collections.abc import Hashable
from threading import Lock
from typing import Any, ClassVar, cast, final

__all__ = ['Sentinel']


@final
class Sentinel[H: Hashable]:
    """
    .. admonition:: Sentinel

        Sentinel values labeled by different (hashable) flavors.

        .. note::

            - Useful for union types.
            - A flavored ``Sentinel`` value always equals itself
              and never equals anything else, especially other
              flavored sentinel values.

    """

    __slots__ = ('_flavor',)

    _flavor: H

    _flavors: ClassVar[dict[Any, Sentinel[Any]]] = {}
    _lock: ClassVar[Lock] = Lock()

    def __new__(cls, flavor: H) -> Sentinel[H]:
        """
        .. admonition:: new

            :param flavor: Hashable value determining which
                           flavored Sentinel to return.
            :returns: The Sentinel(flavor) singleton instance.

        """
        if flavor not in cls._flavors:
            with cls._lock:
                if flavor not in cls._flavors:
                    sentinel = super().__new__(cls)
                    sentinel._flavor = flavor
                    cls._flavors[flavor] = sentinel
        return cast(Sentinel[H], cls._flavors[flavor])

    def __reduce__(self) -> tuple[Sentinel[H], tuple[H]]:
        """
        .. admonition:: reduce

            Tell ``pickle`` and ``copy`` how to reconstruct the
            sentinel: call ``Sentinel(flavor)`` rather than rebuilding
            the object directly.

            - reconstruction goes through ``__new__``, so the flavor
              cache is consulted
            - unpickling returns the existing singleton of that flavor,
              or creates and caches it in a fresh interpreter
            - ``copy`` and ``deepcopy`` use the same protocol, so they
              return the singleton unchanged

            :returns: The pair ``(Sentinel, (flavor,))``, which
                      ``pickle`` calls to rebuild the sentinel.

            .. important::

                Without this, ``pickle`` would construct a duplicate
                ``Sentinel`` outside the flavor cache, and ``is``
                comparisons against it would silently fail.

        """
        return (Sentinel, (self._flavor,))

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Construct string 'Sentinel(flavor)' where the flavor
            is displayed with ``repr()``.

            :returns: A string to reproduce the flavored sentinel.

        """
        return 'Sentinel(' + repr(self._flavor) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Construct string 'Sentinel(flavor)' where the flavor
            is displayed with ``str()``.

            :returns: A string meaningful to an end user.

        """
        return 'Sentinel(' + str(self._flavor) + ')'

    def flavor(self) -> H:
        """
        .. admonition:: get flavor

            :returns: The sentinel's flavor.

        """
        return self._flavor
