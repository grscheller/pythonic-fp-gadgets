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

__all__ = ['Wrap', 'HWrap']

from collections.abc import Callable, Iterator, Hashable


class Wrap[T]():
    """
    .. admonition:: Wrap

        Immutablely wrap exactly one item.

        .. tip::

            ``Wrap`` objects are matchable.

    """
    __slots__ = ('_item',)
    __match_args__ = ('_item',)

    def __init__(self, item: T) -> None:
        """
        .. admonition:: init

            Initialize ``Wrap`` with 1 required item.

            :param item: Item to be wrapped.

        """
        self._item = item

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            Truthiness same as wrapped object.

        """
        return bool(self._item)

    def __len__(self) -> int:
        """
        .. admonition:: len

            Wrapped items always contain just one item.

            :returns: 1

        """
        return 1

    def __iter__(self) -> Iterator[T]:
        """
        .. admonition:: iter

            :yields: A reference to the wrapped item.

        """
        if self:
            yield self._item

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: equality comparison

            Compare ``Wrap`` to another object.

            :param other: Object to be compared.
            :returns: ``True`` if ``other`` is of type Wrap and wraps
                      an item which compares as equal to the wrapped
                      item, otherwise ``False``.

        """
        if not isinstance(other, type(self)):
            return False

        if self._item is other._item:
            return True
        return self._item == other._item

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Construct string 'Wrap(item_str)'
            where ``item_str = repr(item)`` for the contained item. 

            :returns: A string to reproduce of the wrapped item. 

        """
        return 'Wrap(' + repr(self._item) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Construct string 'Wrap(item_str)'
            where ``item_str = str(item)`` for the contained item. 

            :returns: A string meaningful to an end user.

        """
        return 'Wrap(' + str(self._item) + ')'

    def map[U](self, f: Callable[[T], U]) -> 'Wrap[U]':
        """
        .. admonition:: map

            Map function ``f`` over contents.

            :param f: Mapping function.
            :returns: New instance.

        """
        return Wrap(f(self._item))

    def bind[U](self, f: Callable[[T], 'Wrap[U]']) -> 'Wrap[U]':
        """
        .. admonition:: bind

            Flatmap wrapped object with function ``f``.

            :param f: Binding function.
            :returns: New instance.

        """
        return f(self._item)


class HWrap[T: Hashable](Hashable):
    """
    .. admonition:: HWrap

        Immutablely wrap exactly one hashable item.

        .. tip::

            ``HWrap`` objects are hashable and matchable.

    """

    __slots__ = ('_item', '_hash')
    __match_args__ = ('_item',)

    def __init__(self, item: T) -> None:
        """
        .. admonition:: init

            Initialize ``HWrap`` with 1 required item.

            :param item: Item to be wrapped.

        """
        self._item, self._hash = item, hash(item)

    def __hash__(self) -> int:
        return self._hash

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            Truthiness same as wrapped object.

        """
        return bool(self._item)

    def __len__(self) -> int:
        """
        .. admonition:: len

            HWrapped items always contain just one item.

            :returns: 1

        """
        return 1

    def __iter__(self) -> Iterator[T]:
        """
        .. admonition:: iter

            :yields: A reference to the wrapped item.

        """
        if self:
            yield self._item

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: equality comparison

            Compare ``HWrap`` to another object.

            :param other: Object to be compared.
            :returns: ``True`` if ``other`` is of type HWrap and wraps
                      an item which compares as equal to the wrapped
                      item, otherwise ``False``.

        """
        if not isinstance(other, type(self)):
            return False

        if self._hash != other._hash:
            return False
        if self._item is other._item:
            return True
        return self._item == other._item

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Construct string 'HWrap(item_str)'
            where ``item_str = repr(item)`` for the contained item. 

            :returns: A string to reproduce of the wrapped object. 

        """
        return 'Wrap(' + repr(self._item) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Construct string 'HWrap(item_str)'
            where ``item_str = str(item)`` for the contained item. 

            :returns: A string meaningful to an end user.

        """
        return 'Wrap(' + str(self._item) + ')'

    def map[U](self, f: Callable[[T], U]) -> 'HWrap[U]':
        """
        .. admonition:: map

            Map function ``f`` over wrapped the wrapped object
            returning a new ``HWrap`` instance.

            :param f: Mapping function.
            :returns: New instance.

        """
        return HWrap(f(self._item))

    def bind[U](self, f: Callable[[T], 'HWrap[U]']) -> 'HWrap[U]':
        """
        .. admonition:: bind

            Flatmap ``Box`` with function ``f``.

            :param f: Binding function.
            :returns: New instance.

        """
        return f(self._item)
