import copy
import random
from collections import deque
from collections.abc import Iterable, MutableSequence
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from sys import maxsize
from typing import Any

import pytest

from adspy.data_structures.queues import Deque


def test_is_mutable_sequence() -> None:
    dq = Deque()
    for ms in (deque(), dq):  # type: ignore [var-annotated]
        assert isinstance(ms, MutableSequence)
        assert issubclass(type(ms), MutableSequence)


class TestDequeSuite:
    @pytest.mark.parametrize(
        ("it", "maxlen", "answer"),
        [
            ([], -1, []),
            ([], 0, []),
            ([], 1, []),
            ([42, 21], -1, [42, 21]),
            ([42, 21], 0, []),
            ([42, 21], 1, [21]),
            ([42, 21], 2, [42, 21]),
        ],
    )
    def test_init_with_maxlen(
        self, it: Iterable, maxlen: int, answer: list
    ) -> None:
        assert Deque(it, maxlen=maxlen) == answer

    @pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
    def test_append(self, elements: Iterable) -> None:
        items = list(elements)
        dq = Deque()

        ans = items
        for value in items:
            dq.append(value)

        assert dq == ans
        assert len(dq) == len(ans)

    def test_append_with_maxlen_one(self) -> None:
        dq = Deque(maxlen=1)

        dq.append(1)
        dq.append(21)

        assert dq == [21]

        dq.append(42)
        assert dq == [42]

    @pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
    def test_extend(self, elements: Iterable) -> None:
        items = list(elements)
        dq = Deque()

        ans = items
        dq.extend(ans)

        assert dq == items
        assert len(dq) == len(ans)

    def test_extend_with_maxlen_one(self) -> None:
        items = [1, 21, 42]
        dq = Deque(maxlen=1)

        dq.extend(items)

        assert dq == [42]
        assert Deque(items, maxlen=1) == [42]

    @pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
    def test_appendleft(self, elements: Iterable) -> None:
        items = list(elements)
        dq = Deque()

        ans = items
        for value in items:
            dq.appendleft(value)

        assert dq == list(reversed(ans))
        assert len(dq) == len(ans)

    def test_appendleft_with_maxlen_one(self) -> None:
        dq = Deque(maxlen=1)

        dq.appendleft(1)
        dq.appendleft(21)

        assert dq == [21]

        dq.appendleft(42)
        assert dq == [42]

    @pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
    def test_extendleft(self, elements: Iterable) -> None:
        items = list(elements)
        dq = Deque()

        ans = items
        dq.extendleft(ans)

        assert dq == list(reversed(items))
        assert len(dq) == len(ans)

    def test_extendleft_with_maxlen_one(self) -> None:
        items = [1, 21, 42]
        dq = Deque(maxlen=1)

        dq.extendleft(items)

        assert dq == [42]
        assert Deque(items, maxlen=1) == [42]

    @pytest.mark.parametrize("it", [[], [1], [-1, 0, 1]])
    def test_clear(self, it: list[int]) -> None:
        dq = Deque(it)

        dq.clear()

        assert len(dq) == 0
        assert not tuple(dq)

        with pytest.raises(IndexError):
            dq[0]

    @pytest.mark.parametrize("lst", [[], [1, "2", [3, [4, 5]]]])
    def test_copy(self, lst: list) -> None:
        dq = Deque(lst)
        ans = deque(lst)

        copied = copy.copy(dq)
        assert isinstance(copied, Deque)
        assert copied == ans

        copied = dq.copy()
        assert isinstance(copied, Deque)
        assert copied == ans

    @pytest.mark.parametrize(
        ("lst", "value"),
        [
            ([], 1),
            ([1, 2, 1, 0, 1, 3], 1),
        ],
    )
    def test_count(self, lst: list, value: Any) -> None:
        dq = Deque(lst)
        assert dq.count(value) == deque(lst).count(value)

    @pytest.mark.parametrize(
        ("lst", "value", "start", "stop", "expectation"),
        [
            ([], 1, 0, maxsize, pytest.raises(ValueError)),  # noqa: PT011
            ([2, 1, 3], 1, 1, maxsize, does_not_raise()),
            ([2, 1, 3], 3, 2, maxsize, does_not_raise()),
            ([2, 1, 3], 2, 2, maxsize, pytest.raises(ValueError)),  # noqa: PT011
            ([2, 1, 3], 1, 2, maxsize, pytest.raises(ValueError)),  # noqa: PT011
            ([2, 1, 3], 1, 3, maxsize, pytest.raises(ValueError)),  # noqa: PT011
            ([2, 1, 3], 1, 0, 1, pytest.raises(ValueError)),  # noqa: PT011
            ([2, 1, 3], 3, 0, 1, pytest.raises(ValueError)),  # noqa: PT011
        ],
    )
    def test_index(
        self,
        lst: list,
        value: Any,
        start: int,
        stop: int,
        expectation: AbstractContextManager,
    ) -> None:
        dq = Deque(lst)
        ans = deque(lst)

        aindex = 0
        with expectation:
            aindex = ans.index(value, start, stop)

        dindex = 0
        with expectation:
            dindex = dq.index(value, start, stop)

        assert dindex == aindex

    def test_insert(self) -> None:
        ans: deque[int] = deque()
        dq = Deque()

        idx, val = 0, 21
        ans.insert(idx, val)
        dq.insert(idx, val)
        assert dq == ans

        ans.clear()
        dq.clear()

        idx = -1
        ans.insert(idx, val)
        dq.insert(idx, val)
        assert dq == ans

        for i in (0, -1, 2, -2, -3, 4):
            new_val = val * i

            ans.insert(i, new_val)
            dq.insert(i, new_val)

            assert dq == ans

    def test_insert_with_maxlen(self) -> None:
        dq = Deque([1, 2, 3], maxlen=3)

        dq.insert(1, 12)
        assert dq == [2, 12, 3]

        dq.insert(0, 21)
        assert dq == [21, 12, 3]

        dq.insert(-1, 42)
        assert dq == [12, 42, 3]

    def test_popleft(self) -> None:
        it = deque(random.sample(range(100), 10))
        dq = Deque(it)

        while dq:
            dq.popleft()
            it.popleft()
            assert dq == it

        with pytest.raises(IndexError):
            dq.popleft()

        with pytest.raises(IndexError):
            dq.popleft()

    def test_pop(self) -> None:
        it = deque(random.sample(range(100), 10))
        dq = Deque(it)

        while dq:
            dq.pop()
            it.pop()
            assert dq == it

        with pytest.raises(IndexError):
            dq.pop()

        with pytest.raises(IndexError):
            dq.pop()

    def test_remove(self) -> None:
        it = deque(random.sample(range(100), 10))
        dq = Deque(it)

        while dq:
            item = random.choice(it)

            dq.remove(item)
            it.remove(item)

            assert dq == it

    @pytest.mark.parametrize("it", [[], [0], [1, 2], [1, -1, 0]])
    def test_reversing(self, it: list[int]) -> None:
        icopy = deque(it)
        dq = Deque(icopy)
        rev = tuple(reversed(icopy))

        assert tuple(reversed(dq)) == rev

        dq.reverse()
        assert dq == rev
