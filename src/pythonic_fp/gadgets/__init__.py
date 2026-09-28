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

"""
Gadgets
=======

.. admonition:: Collection of mostly self-contained functions and classes

    - Functions and classes which could go multiple places or have
      no good place to go.
    - Self-contained with minimal dependencies.

      - No pythonic_fp dependencies at all.

"""

from collections.abc import Iterator

__all__ = ['first_common_ancestor', 'iterate_over_arguments']

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2026 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'


def first_common_ancestor(cls1: type, cls2: type) -> type:
    """
    .. admonition:: First common ancestor

        Best effort to find the least upper bound in the inheritance
        graph of two classes.

        :param cls1: A class in the inheritance hierarchy.
        :param cls2: A class in the inheritance hierarchy.
        :returns: First common ancestor in ``cls1.__mro__`` order.
        :raises TypeError: Defensively raised when no common ancestor
                           is found.

        .. note::

            The function is not symmetric in its arguments. In genuine
            multiple inheritance graphs, swapping ``cls1`` and ``cls2``
            can yield a different ancestor. Also, a virtual ancestor
            registered with an ABC may be a tighter bound than anything
            in the actual MRO.

        .. note::

            Since ``object`` terminates all actual MRO's, ``TypeError``
            is unlikely to ever be thrown, except in the case of some
            exotic metaclass breaking this assumption. This exception
            is here mainly to let typing tools know that object ``None``
            is not a possible return type.


    """
    if issubclass(cls1, cls2):
        return cls2
    if issubclass(cls2, cls1):
        return cls1

    for ancestor in cls1.__mro__:
        if issubclass(cls2, ancestor):
            return ancestor
    raise TypeError("first_common_ancestor: no common ancestor found!")


def iterate_over_arguments[A](*args: A) -> Iterator[A]:
    """
    .. admonition:: Iterate over arguments.

        Function returning an iterator over its arguments.

        :param args: Objects to iterate over.
        :returns: An iterator of the function's arguments.

        .. note::

            Does not create a Python object to iterate over.

    """
    yield from args
