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


def test_is_mutable_sequence():
    dq = Deque()
    for ms in (deque(), dq):  # type: ignore [var-annotated]
        assert isinstance(ms, MutableSequence)
        assert issubclass(type(ms), MutableSequence)


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_append(elements: Iterable):
    dq = Deque()
    ans = list(elements)

    for value in elements:
        dq.append(value)

    assert dq == elements
    assert len(dq) == len(ans)


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_appendleft(elements: Iterable):
    dq = Deque()
    ans = list(elements)

    for value in elements:
        dq.appendleft(value)

    assert dq == reversed(ans)
    assert len(dq) == len(ans)


@pytest.mark.parametrize("it", [[], [1], [-1, 0, 1]])
def test_clear(it: list[int]):
    dq = Deque(it)

    dq.clear()

    assert len(dq) == 0
    assert not tuple(dq)

    with pytest.raises(IndexError):
        dq[0]


@pytest.mark.parametrize("lst", [[], [1, "2", [3, [4, 5]]]])
def test_copy(lst: list):
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
def test_count(lst: list, value: Any):
    dq = Deque(lst)
    assert dq.count(value) == deque(lst).count(value)


@pytest.mark.parametrize("it", [[], "123"])
def test_extend(it: Iterable):
    dq = Deque()
    seq = tuple(it)

    dq.extend(it)

    assert dq == it
    assert len(dq) == len(seq)


@pytest.mark.parametrize(
    ("list1", "list2"),
    [
        ([], []),
        ([], [1, 2]),
        ([2, 3], []),
        ([2, 1], [3, 4]),
    ],
)
def test_extendleft(list1: list, list2: list):
    dq = Deque(list2)
    dq.extendleft(list1)
    assert dq == (list1 + list2)


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
    lst: list,
    value: Any,
    start: int,
    stop: int,
    expectation: AbstractContextManager,
):
    dq = Deque(lst)
    ans = deque(lst)

    aindex = 0
    with expectation:
        aindex = ans.index(value, start, stop)

    dindex = 0
    with expectation:
        dindex = dq.index(value, start, stop)

    assert dindex == aindex


def test_insert():
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


def test_popleft():
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


def test_pop():
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


def test_remove():
    it = deque(random.sample(range(100), 10))
    dq = Deque(it)

    while dq:
        item = random.choice(it)

        dq.remove(item)
        it.remove(item)

        assert dq == it


@pytest.mark.parametrize("it", [[], [0], [1, 2], [1, -1, 0]])
def test_reversing(it: list[int]):
    icopy = deque(it)
    dq = Deque(icopy)
    rev = tuple(reversed(icopy))

    assert tuple(reversed(dq)) == rev

    dq.reverse()
    assert dq == rev
