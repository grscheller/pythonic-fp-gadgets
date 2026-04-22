Usage
=====

How to install the package
--------------------------

Install the project into your Python environment:

.. code:: console

    $ pip install pythonic-fp.gadgets

Importing the package
---------------------

Import the gadgets where "gadgets" are simple objects with no external dependencies
other than the Python standard library.

.. code:: python

    from pythonic_fp.gadgets.iterate_arguments import ita
    from pythonic_fp.gadgets.latest_common_ancestor import lca
    from pythonic_fp.gadgets.box import Box
    from pythonic_fp.gadgets.wrap import Wrap
    from pythonic_fp.gadgets.wrap import HWrap
    from pythonic_fp.gadgets.sentinels.flavored import Sentinel
    from pythonic_fp.gadgets.sentinels.novalue import NoValue

Use case examples
-----------------

Flavored Sentinels
~~~~~~~~~~~~~~~~~~

Sentinel values of different (hashable) flavors. Can be used
with functions or classes.

**Some Use Cases**

Could be used like an Enum.

.. code:: python

    from pythonic_fp.gadgets.sentinels.flavored import Sentinel

    def calculate_something(n: int, x: float) -> tuple[Sentinel[int], float]:
        if n <= 0:
            return (Sentinel(0), x)
        return (Sentinel(n), x/n)

    def process_result(pair: tuple[Sentinel[int], float]) -> float:
        if pair[0] is Sentinel(0):
            return 0.0
        return pair[1]

    result = process_result(calculate_something(213, 15234.541))

Can be also be used as a private implementation detail for a class.
Here is an example of an class that can take an "optional" value
yet still be able to store ``None`` as a value.

.. code:: python

    from typing import cast, ClassVar, Final, overload
    from pythonic_fp.gadgets.sentinels.flavored import Sentinel


    class MyClass:
        _sentinel: Final[ClassVar[Sentinel[str]]] = Sentinel('_secret_str')

        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, value: float) -> None: ...
        @overload
        def __init__(self, value: None) -> None: ...
        @overload
        def __init__(self, value: float | None) -> None: ...

        def __init__(
            self, value: float | None | Sentinel[str] = Sentinel('_secret_str')
        ) -> None:
            if value is self._sentinel:
                self.value: float | None = 42.0
            else:
                self.value = cast(float | None, value)

        def get_value(self) -> float | None:
            return self.value

Sentinel NoValue
~~~~~~~~~~~~~~~~

This test from the test suite is a bit contrived, but I think
it illustrates the usage.

.. code:: python

    from typing import cast, Final, overload
    from pythonic_fp.gadgets.sentinels.novalue import NoValue


    class Foo:
        @overload
        def __init__(self, /) -> None: ...
        @overload
        def __init__(self, repeat: None, /) -> None: ...

        def __init__(self, repeat: int | None | NoValue = NoValue(), /) -> None:
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

        def __init__(self, repeat: int | None | NoValue = NoValue(), /) -> None:
            if repeat is None:
                self._repeat = 1
            elif repeat is NoValue():
                self._repeat = 2
            else:
                ii: int = cast(int, repeat)
                self._repeat = ii if ii >=0 else -ii


    def test_foo() -> None:
        foo: Foo = Foo()
        foo_none: Foo = Foo(None)

        assert foo.repeat() == 'foo'
        assert foo_none.repeat() == ''


    def test_repeat_foo() -> None:
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
