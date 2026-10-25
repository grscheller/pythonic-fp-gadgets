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

"""Tests NoValue in a contrived situation."""

from typing import cast, overload

from pythonic_fp.gadgets.sentinels.novalue import NoValue

novalue1 = NoValue()
novalue2 = NoValue()


class TestStrRepr:
    def test_noValue_str(self) -> None:
        noValue: NoValue = NoValue()
        assert str(noValue) == 'NoValue()'
        assert repr(noValue) == 'NoValue()'


class TestSingleton:
    def test_singleton_instance(self) -> None:
        assert novalue1 is novalue2

    def test_nonstandard_equality_symmatrics(self) -> None:
        assert (novalue1 == novalue2) is False
        assert (novalue1 != novalue2) is False
        assert (novalue1 == 42) is False
        assert (42 != novalue2) is False


class Foo:
    @overload
    def __init__(self, /) -> None: ...
    @overload
    def __init__(self, repeat: None, /) -> None: ...

    def __init__(self, repeat: int | None | NoValue = novalue1, /) -> None:
        if repeat is None:
            self._repeat = 0
        else:
            self._repeat = 1

    def repeat(self) -> str:
        return 'foo' * self._repeat


class RepeatFoo(Foo):
    @overload
    def __init__(self, /) -> None: ...
    @overload
    def __init__(self, repeat: None, /) -> None: ...
    @overload
    def __init__(self, repeat: int, /) -> None: ...

    def __init__(self, repeat: int | None | NoValue = novalue2, /) -> None:
        if repeat is None:
            self._repeat = 1
        elif repeat is NoValue():
            self._repeat = 2
        else:
            ii: int = cast(int, repeat)
            self._repeat = ii if ii >= 0 else -ii


class TestNoValue:
    def test_foo(self) -> None:
        foo: Foo = Foo()
        foo_none: Foo = Foo(None)

        assert foo.repeat() == 'foo'
        assert foo_none.repeat() == ''

    def test_repeat_foo(self) -> None:
        foo: Foo = RepeatFoo()
        foo_none: Foo = RepeatFoo(None)
        foo_0: Foo = RepeatFoo(0)
        foo_1: Foo = RepeatFoo(1)
        foo_2: Foo = RepeatFoo(2)
        foo_3: Foo = RepeatFoo(3)
        foo_neg_4: Foo = RepeatFoo(-4)

        assert foo.repeat() == 'foofoo'
        assert foo_none.repeat() == 'foo'
        assert foo_0.repeat() == ''
        assert foo_1.repeat() == 'foo'
        assert foo_2.repeat() == 'foofoo'
        assert foo_3.repeat() == 'foofoofoo'
        assert foo_neg_4.repeat() == 'foofoofoofoo'
