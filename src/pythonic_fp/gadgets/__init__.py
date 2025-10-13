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

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
