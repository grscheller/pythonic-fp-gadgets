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

"""Pickle tests for novalue sentinels."""

import pickle
import subprocess
import sys
from copy import copy, deepcopy

from pythonic_fp.gadgets.sentinels.novalue import NoValue

nada = NoValue()
nono = NoValue()


class TestNoValuePickle:
    def test_identity_survives_all_protocols(self) -> None:
        for item in nada, nono:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_identity_with_NoValue_constructor(self) -> None:
        no_no, na_da = NoValue(), NoValue()
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_no_no, r_na_da = pickle.loads(
                pickle.dumps((no_no, na_da), protocol=protocol)
            )
            assert r_no_no is no_no
            assert r_na_da is na_da
            assert r_no_no is r_na_da
            assert r_no_no is nono
            assert r_na_da is nada

    def test_identity_inside_containers(self) -> None:
        payload = {'a': [nada], 'b': (nono, nada), 'c': NoValue()}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is nada
            assert restored['b'][0] is nono
            assert restored['b'][1] is nada
            assert restored['b'][0] is nada
            assert restored['b'][1] is nono
            assert restored['c'] is nada
            assert restored['c'] is nono

    def test_copy_and_deepcopy_return_the_novalue_singletons(self) -> None:
        nada1 = NoValue()
        nada2 = NoValue()
        assert copy(nada1) is nada1
        assert copy(nada2) is nada2
        assert copy(nada1) is nada2
        assert copy(nada2) is nada1

        type ThingType = tuple[NoValue, list[dict[int, NoValue]]]
        thing1: ThingType = (nada1, [{21: nada1, 42: nada2}, {7: nada2}])
        thing2 = deepcopy(thing1)
        assert thing2[0] is nada1
        assert thing2[1][0][21] is nada1
        assert thing2[1][0][42] is nada2
        assert thing2[1][1][7] is nada2
        assert thing1 == thing2

    @staticmethod
    def _run(script: str, data: bytes) -> subprocess.CompletedProcess[bytes]:
        done = subprocess.run(
            [sys.executable, '-c', script],
            input=data,
            capture_output=True,
            check=False,
        )
        assert done.returncode == 0, (
            f'child process failed:\n{done.stderr.decode(errors="replace")}'
        )
        return done

    def test_identity_in_a_fresh_interpreter(self) -> None:
        # Remove additional whitespace below if tested on Python <3.14
        _SCRIPT = """
        import pickle, sys
        from pythonic_fp.gadgets.sentinels.novalue import NoValue
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is NoValue(), 'novalue came back as a duplicate'
        assert restored[1] is NoValue(), 'novalue came back as a duplicate'
        assert restored[2] is NoValue(), 'novalue came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    nada,
                    nono,
                    NoValue(),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'
