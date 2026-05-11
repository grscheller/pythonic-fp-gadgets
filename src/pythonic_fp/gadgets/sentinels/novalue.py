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

import threading
from typing import ClassVar, final

__all__ = ['NoValue']


@final
class NoValue:
    """
    .. admonition:: missing value

        Singleton class representing an actual, not
        potential, missing value.

        While ``None`` and ``()`` are frequently used as sentinel values,
        I prefer to think of them as

        - ``None`` as returns, or returned, no values.
        - ``()`` as an empty, possibly typed, iterable collection.

        .. important::

            Given variables

            .. code:: python

                x: int | NoValue
                y: int | NoValue

            Equality between ``x`` and ``y`` means both values exist
            and compare as equal.

            .. table:: ``x == y``

                +-------------------+-------------------+------------+------------+
                |                   |                   |            |            |
                +===================+===================+============+============+
                |                   | ``y = NoValue()`` | ``y = 42`` | ``y = 57`` |
                +-------------------+-------------------+------------+------------+
                | ``x = NoValue()`` | ``False``         | ``False``  | ``False``  |
                +-------------------+-------------------+------------+------------+
                | ``x = 42``        | ``False``         | ``True``   | ``False``  |
                +-------------------+-------------------+------------+------------+
                | ``x = 57``        | ``False``         | ``False``  | ``True``   |
                +-------------------+-------------------+------------+------------+

            .. table:: ``x != y``

                +-------------------+-------------------+------------+------------+
                |                   |                   |            |            |
                +===================+===================+============+============+
                |                   | ``y = NoValue()`` | ``y = 42`` | ``y = 57`` |
                +-------------------+-------------------+------------+------------+
                | ``x = NoValue()`` | ``False``         | ``False``  | ``False``  |
                +-------------------+-------------------+------------+------------+
                | ``x = 42``        | ``False``         | ``False``  | ``True``   |
                +-------------------+-------------------+------------+------------+
                | ``x = 57``        | ``False``         | ``True``   | ``False``  |
                +-------------------+-------------------+------------+------------+

            .. warning::

                - use ``==`` or ``!=`` only in value comparisons
                - use ``is`` and ``is not`` to identity the ``NoValue()``
                  singleton itself

        .. tip::

            Use in a union type when creating "optional" arguments
            to functions and methods.

            To help ensure the abstraction stays a hidden implementation
            detail and does not leak out into user code,

            - Do not export the sentinel value.

              - A new reference can always be generated via ``NoValue()``.

            - Use ``@overload`` to keep the ``NoValue`` type out of
              documentation and IDEs.

    """

    __slots__ = ()

    _instance: 'ClassVar[NoValue | None]' = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _hash: ClassVar[int] = 0

    def __new__(cls) -> 'NoValue':
        """
        .. admonition:: new

            :returns: The ``NoValue()`` singleton instance.

        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._hash = id(cls)
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __hash__(self) -> int:
        """
        .. admonition:: hash

            :returns: The singleton's unique integer hash value.
        """
        return type(self)._hash

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            :returns: The string 'NoValue()'.

        """
        return 'NoValue()'

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            Always falsy.

            :returns: False

            .. tip

                Can be used to provide a fallback value when used
                with Python shortcut logic.

                .. code:: python

                    result: str | NoValue = NoValue()
                    if predicate(x):
                        result = 'some non-empty string'
                    value = result or 'fallback string'

        """
        return False

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            :param other: The object to be compared.
            :returns: ``False`` even if compared to itself.

            .. warning::

                - non-standard comparison semantics
                - always returns ``False``
                - if one or both values are missing,
                  then what is there to compare?

        """
        return False

    def __ne__(self, other: object) -> bool:
        """
        .. admonition:: not equal

            :returns: ``False``

            .. warning::

                - non-standard comparison semantics
                - always returns ``False``

        """
        return False
