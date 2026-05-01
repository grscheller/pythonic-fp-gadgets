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

from collections.abc import Callable, Iterator
from typing import cast, Final, overload

__all__ = ['Box']

type _Sentinel = object
_sentinel: Final[_Sentinel] = object()


class Box[T]:
    """
    .. admonition:: Box

        Container holding at most one item of a given type.

        .. tip::

            Objects of the ``Box`` type

            - Are truthy if not empty.
            - Can be combined with other iterators before being filled.
            - Can be used like a promise.
            - Threadsafe
            - Can be used in Python match statements.

    """
    __slots__ = ('_item',)
    __match_args__ = ('_item',)

    @overload
    def __init__(self, item: T) -> None: ...
    @overload
    def __init__(self) -> None: ...

    def __init__(self, item: T | _Sentinel = _sentinel) -> None:
        """
        :param item: An optional initial ``item`` for the ``Box``.

        """
        self._item = item

    def __bool__(self) -> bool:
        return self._item is not _sentinel

    def __iter__(self) -> Iterator[T]:
        if self:
            yield cast(T, self._item)

    def __repr__(self) -> str:
        if self:
            return 'Box(' + repr(self._item) + ')'
        return 'Box()'

    def __len__(self) -> int:
        return 1 if self else 0

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            Efficiently compare ``Box`` to another object.

        :param other: The object to be compared.
        :returns: ``True`` if ``other`` is another ``Box`` and contains
                  an object which compares as equal to the object
                  contained in the ``Box``, otherwise ``False``.

        """
        if not isinstance(other, type(self)):
            return False

        if self._item is other._item:
            return True
        if self._item == other._item:
            return True
        return False

    @overload
    def get(self) -> T: ...
    @overload
    def get(self, alt: T) -> T: ...

    def get(self, alt: T | _Sentinel = _sentinel) -> T:
        """
        .. admonition:: Get

            Return the boxed item, if it exists, otherwise
            an alternate item, if given.

        :param alt: An optional item of type ``T`` to return
                    if the ``Box`` is empty.
        :returns: Contents of ``Box`` or an alternate item, if given,
                  when the ``Box`` is empty.
        :raises ValueError: When the ``alt`` item is not provided
                            but needed.

        """
        if self._item is not _sentinel:
            return cast(T, self._item)
        if alt is _sentinel:
            msg = 'Box: get from empty Box with no alternate return item provided'
            raise ValueError(msg)
        return cast(T, alt)

    def pop(self) -> T:
        """
        .. admonition:: Pop

            Pop item from ``Box`` if not empty.

        :returns: The item contained in the ``Box``.
        :raises ValueError: If Box is empty.

        """
        if self._item is _sentinel:
            msg = 'Box: Trying to pop an item from an empty Box'
            raise ValueError(msg)
        popped = cast(T, self._item)
        self._item = _sentinel
        return popped

    def push(self, item: T) -> None:
        """
        .. admonition:: Push

            Push an item into ``Box`` if empty.

        :param item: Item to push into the empty ``Box``.
        :raises ValueError: If ``Box`` is not empty.

        """
        if self._item is _sentinel:
            self._item = item
        else:
            msg = 'Box: Trying to push an item in a non-empty Box'
            raise ValueError(msg)
        return None

    def put(self, item: T) -> None:
        """
        .. admonition:: Put

            Put an item in the Box. Discard any previous contents.

        """
        self._item = item

    def exchange(self, new_item: T) -> T:
        """
        .. admonition:: Exchange

            Exchange an item with what is in the Box.

        :param ``new_item``: New item to exchange for current item.
        :returns: Original contents of the ``Box``.
        :raises ValueError: If Box is empty.

        """
        if self._item is _sentinel:
            msg = 'Box: Trying to exchange items from an empty Box'
            raise ValueError(msg)
        popped = cast(T, self._item)
        self._item = new_item
        return popped

    def map[U](self, f: Callable[[T], U]) -> 'Box[U]':
        """
        .. admonition:: Map

            Map function ``f`` over contents. We need to return a new
            instance since the type of Box can change.

        :param f: Mapping function.
        :returns: New instance.

        """
        if self._item is _sentinel:
            return Box()
        return Box(f(cast(T, self._item)))

    def bind[U](self, f: Callable[[T], 'Box[U]']) -> 'Box[U]':
        """
        .. admonition:: Bind

            Flatmap ``Box`` with function ``f``.

        :param f: Binding function.
        :returns: New instance.

        """
        if self._item is _sentinel:
            return Box()
        return f(cast(T, self._item))
