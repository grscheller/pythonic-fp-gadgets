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

"""Pickle tests for truthy_falsy booleans."""

import pickle
import subprocess
import sys
from copy import copy, deepcopy

from pythonic_fp.gadgets.sentinels.flavored import Sentinel

fl10_int = Sentinel(10)
fl42_int = Sentinel(42)
fl10_str = Sentinel('Ten')
fl42_str = Sentinel('Forty Two')


class TestNoValuePickle:
    def test_identity_survives_all_protocols(self) -> None:
        for item in fl10_int, fl42_int, fl10_str, fl42_str:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_identity_with_Sentinel(self) -> None:
        fl_42_int, fl_10_int, fl_00_int = Sentinel(42), Sentinel(10), Sentinel(0)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_fl_42_int, r_fl_10_int, r_fl_00_int = pickle.loads(
                pickle.dumps((fl_42_int, fl_10_int, fl_00_int), protocol=protocol)
            )
            assert r_fl_42_int is fl_42_int
            assert r_fl_10_int is fl_10_int
            assert r_fl_42_int is not r_fl_10_int
            assert r_fl_00_int is not r_fl_42_int
            assert r_fl_42_int is fl42_int
            assert r_fl_10_int is fl10_int
            assert r_fl_42_int is fl42_int
            assert r_fl_10_int is fl10_int

    def test_identity_inside_containers(self) -> None:
        payload = {'a': [fl42_str], 'b': (fl10_int, fl42_int), 'c': fl10_str}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is fl42_str
            assert restored['b'][0] is fl10_int
            assert restored['b'][1] is fl42_int
            assert restored['c'] is fl10_str

    def test_copy_and_deepcopy_return_the_singletons(self) -> None:
        type Fl_Tup1 = Sentinel[tuple[int, ...]]
        type Fl_Tup2 = Sentinel[tuple[int, Sentinel[str]]]
        fl_tup1: Fl_Tup1 = Sentinel((42, 10, 42))
        fl_tup2: Fl_Tup2 = Sentinel((42, fl42_str))
        assert copy(fl_tup1) is fl_tup1
        assert copy(fl_tup2) is fl_tup2
        assert copy(fl_tup2) is copy(fl_tup2)
        assert copy(fl_tup1) is not fl_tup2
        assert copy(fl_tup1) is not copy(fl_tup2)

        type ThingType = tuple[Fl_Tup1, list[dict[int, Fl_Tup1 | Fl_Tup2]]]
        thing1: ThingType = (fl_tup1, [{21: fl_tup1, 42: fl_tup2}, {7: fl_tup2}])
        thing2 = deepcopy(thing1)
        assert thing2[0] is fl_tup1
        assert thing2[1][0][21] is fl_tup1
        assert thing2[1][0][42] is fl_tup2
        assert thing2[1][1][7] is fl_tup2
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
        from pythonic_fp.gadgets.sentinels.flavored import Sentinel
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is Sentinel(10), 'Sentinel(10) came back as a duplicate'
        assert restored[1] is Sentinel(42), 'Sentinel(42) came back as a duplicate'
        assert restored[2] is Sentinel('Ten'), "Sentinel('Ten') came back as a duplicate"
        assert restored[3] is Sentinel('Forty Two'), "Sentinel('Forty Two') came back as a duplicate"
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    fl10_int,
                    fl42_int,
                    fl10_str,
                    fl42_str,
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'
