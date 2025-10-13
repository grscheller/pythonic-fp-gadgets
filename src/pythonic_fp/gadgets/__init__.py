# Copyright 2023-2025 Geoffrey R. Scheller
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
Simple Gadgets
==============

Library of simple, but useful, functions and classes with no external
dependencies besides the those from the Python standard Library. This
includes other Pythonic Functional Programming dependencies.

+----------------------+------------------------------+------------------------------------+
| Gadget               | Description                  | Module                             |
+======================+==============================+====================================+
| function ``ita``     | Return Iterator of arguments | ``gadgets.iterate_arguments``      |
+----------------------+------------------------------+------------------------------------+
| function ``lca``     | Find least common base class | ``gadgets.latest_common_ancestor`` |
+----------------------+------------------------------+------------------------------------+
| class ``Box``        | Single item box              | ``gadgets.box``                    |
+----------------------+------------------------------+------------------------------------+
| class ``Wrap``       | Wrapped item                 | ``gadgets.wrap``                   |
+----------------------+------------------------------+------------------------------------+
| class ``HWrap``      | Wrapped hashable item        | ``gadgets.wrap``                   |
+----------------------+------------------------------+------------------------------------+
| module ``sentinels`` | Sentinels values with extras | ``gadgets.sentinels``              |
+----------------------+------------------------------+------------------------------------+

"""

from collections.abc import Iterator
from inspect import getmro

__all__ = ['iterate_over_arguments', 'first_common_ancestor']

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'


def iterate_over_arguments[A](*args: A) -> Iterator[A]:
    """Function returning an iterator of its arguments.

    .. note::

        Does not create an object to iterate over.

        - well, not in the Python world
        - maybe in the C world

    :param args: Objects to iterate over.
    :returns: An iterator of the arguments.

    """
    yield from args
    

def first_common_ancestor(cls1: type, cls2: type) -> type:
    """Find the least upper bound in the inheritance graph
    of two classes.

    .. warning::

        This function can fail with a TypeError. Some error messages
        seen are

        - multiple bases have instance lay-out conflict
        - type 'bool' is not an acceptable base type

        This happens frequently when the function is given
        Python builtin types.

    :param cls1: A class in the inheritance hierarchy.
    :param cls2: A class in the inheritance hierarchy.
    :returns: First common ancestor based on getmro order.
    :raises TypeError: Raised by ``inspect.getmto``.

    """
    if issubclass(cls1, cls2):
        return cls2
    if issubclass(cls2, cls1):
        return cls1

    for common_ancestor in getmro(type('LcaDiamondClass', (cls1, cls2), {})):
        if issubclass(cls1, common_ancestor) and issubclass(cls2, common_ancestor):
            return common_ancestor
    raise TypeError("latest_common_ancestor: no common ancestor found!!!") 
