import copy
import random
from collections.abc import Iterable, MutableSequence
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from sys import maxsize
from typing import Any

import pytest

from adspy.algorithms.searching import linear_search
from adspy.algorithms.sorting import merge_sort, quick_sort
from adspy.data_structures.linked_lists import DoublyLinkedList


def test_is_mutable_sequence():
    dlist = DoublyLinkedList()
    ms: MutableSequence
    for ms in ([], dlist):
        assert isinstance(ms, MutableSequence)
        assert issubclass(type(ms), MutableSequence)


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_prepend(elements: Iterable):
    lst = DoublyLinkedList()
    ans = list(elements)

    for value in elements:
        lst.prepend(value)

    assert lst == reversed(ans)
    assert len(lst) == len(ans)


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_append(elements: Iterable):
    lst = DoublyLinkedList()
    ans = list(elements)

    for value in elements:
        lst.append(value)

    assert lst == elements
    assert len(lst) == len(ans)


@pytest.mark.parametrize("it", [[], "123"])
def test_extend(it: Iterable):
    lst = DoublyLinkedList()
    seq = tuple(it)

    lst.extend(it)

    assert lst == it
    assert len(lst) == len(seq)


def test_comparisons():
    assert DoublyLinkedList([]) == DoublyLinkedList([])
    assert DoublyLinkedList([1]) == DoublyLinkedList([1])

    assert DoublyLinkedList([2]) != DoublyLinkedList([])
    assert DoublyLinkedList([2]) != DoublyLinkedList([1])

    assert DoublyLinkedList([1]) < DoublyLinkedList([2])
    assert DoublyLinkedList([]) < DoublyLinkedList([1])
    assert DoublyLinkedList([1, 2]) < DoublyLinkedList([2])

    assert DoublyLinkedList([2]) > DoublyLinkedList([1])
    assert DoublyLinkedList([2]) > DoublyLinkedList([])
    assert DoublyLinkedList([2, 1]) > DoublyLinkedList([-1, 0, 1])

    assert DoublyLinkedList([]) <= DoublyLinkedList([2, 1])
    assert DoublyLinkedList([2, 1]) <= DoublyLinkedList([2, 1])
    assert DoublyLinkedList([2, 1]) <= DoublyLinkedList([3])

    assert DoublyLinkedList([1, 2]) >= DoublyLinkedList([])
    assert DoublyLinkedList([1, 2]) >= DoublyLinkedList([1, 2])
    assert DoublyLinkedList([2]) >= DoublyLinkedList([1, 2])


@pytest.mark.parametrize(
    ("it", "value", "answer"), [([], 1, False), ([1], 1, True), ([1], 0, False)]
)
def test_contains(it: list[int], value: int, answer: bool):
    assert bool(value in DoublyLinkedList(it)) == answer


@pytest.mark.parametrize(
    ("it", "key", "expectation"),
    [
        ([], 0, pytest.raises(IndexError)),
        ([1], 0, does_not_raise()),
        ([1], -1, does_not_raise()),
        ([], slice(0, 3, 1), does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), does_not_raise()),
    ],
)
def test_get_items(
    it: list[int], key: int | slice, expectation: AbstractContextManager
):
    lst = DoublyLinkedList(it)

    lst_elems = None
    with expectation:
        lst_elems = lst[key]

    it_elems = None
    with expectation:
        it_elems = lst[key]

    assert it_elems == lst_elems


@pytest.mark.parametrize("it", [[], [1], [-1, 0, 1]])
def test_clear(it: list[int]):
    lst = DoublyLinkedList(it)

    lst.clear()

    assert len(lst) == 0
    assert not tuple(lst)

    with pytest.raises(IndexError):
        lst[0]


@pytest.mark.parametrize(
    ("it", "key", "expectation"),
    [
        ([], 0, pytest.raises(IndexError)),
        ([1], 0, does_not_raise()),
        ([1], -1, does_not_raise()),
        ([], slice(0, 3, 1), does_not_raise()),
        ([2], slice(0, 3, 1), does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), does_not_raise()),
        ([1, 1, 1, 1], slice(1, 3, 1), does_not_raise()),
        ([1, 3, 1, 1, 2], -3, does_not_raise()),
    ],
)
def test_delete_items(
    it: list[int], key: int | slice, expectation: AbstractContextManager
):
    lst = DoublyLinkedList(it)

    with expectation:
        del it[key]

    with expectation:
        del lst[key]

    assert lst == it


def test_remove():
    it = random.sample(range(100), 10)
    lst = DoublyLinkedList(it)

    while lst:
        item = random.choice(it)

        lst.remove(item)
        it.remove(item)

        assert lst == it


def test_pop():
    it = random.sample(range(100), 10)
    dlist = DoublyLinkedList(it)

    while dlist:
        idx = random.choice(range(len(dlist)))
        dlist.pop(idx)
        it.pop(idx)
        assert dlist == it

    with pytest.raises(IndexError):
        dlist.pop(0)

    with pytest.raises(IndexError):
        dlist.pop(-1)


@pytest.mark.parametrize(
    ("it", "key", "value", "expectation"),
    [
        ([], -1, 0, pytest.raises(IndexError)),
        ([], slice(-1, 0, 1), [3], does_not_raise()),
        ([], slice(1, 3, 1), [3], does_not_raise()),
        ([1], slice(0, 3, 1), [3], does_not_raise()),
        ([2], slice(1, 3, 1), [3], does_not_raise()),
        ([1], 0, "2", does_not_raise()),
        ([1, 2], -1, "a", does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), [-1, 1], does_not_raise()),
        ([1, 1, 1, 1], slice(1, 3, 1), [2, 3], does_not_raise()),
        ([1, 3, 1, 1, 2], 2, "T", does_not_raise()),
        ([1, 2, 3], 2, [2, 3], does_not_raise()),
        ([3, 2, 1], slice(0, 2, 1), 21, pytest.raises(TypeError)),
    ],
)
def test_set_items(
    it: list[int],
    key: int | slice,
    value: Any,
    expectation: AbstractContextManager,
):
    lst = DoublyLinkedList(it)

    with expectation:
        it[key] = value

    with expectation:
        lst[key] = value

    assert lst == it


def test_searchability():
    sample = (-1, 0, 1, -2, 2)
    lst = DoublyLinkedList(sample)

    value = random.choice(sample)

    assert linear_search(lst, value) == sample.index(value)


def test_sortability():
    sample = random.sample(range(1, 100, 2), 20)
    lst = DoublyLinkedList(sample)

    answer = sorted(sample)

    assert merge_sort(seq=lst) == answer
    assert quick_sort(seq=lst) == answer


def test_insert():
    lst: list[int] = []
    dlist = DoublyLinkedList()

    idx, val = 0, 21
    lst.insert(idx, val)
    dlist.insert(idx, val)
    assert dlist == lst

    lst.clear()
    dlist.clear()

    idx = -1
    lst.insert(idx, val)
    dlist.insert(idx, val)
    assert dlist == lst

    for i in (0, -1, 2, -2, -3, 4):
        new_val = val * i

        lst.insert(i, new_val)
        dlist.insert(i, new_val)

        assert dlist == lst


@pytest.mark.parametrize("it", [[], [0], [1, 2], [1, -1, 0]])
def test_reversing(it: list[int]):
    icopy = it.copy()
    lst = DoublyLinkedList(icopy)
    rev = tuple(reversed(icopy))

    assert tuple(reversed(lst)) == rev

    lst.reverse()
    assert lst == rev


@pytest.mark.parametrize("lst", [[], [1, "2", [3, [4, 5]]]])
def test_copy(lst: list):
    dlist = DoublyLinkedList(lst)

    copied = copy.copy(dlist)
    assert isinstance(copied, DoublyLinkedList)
    assert copied == lst

    copied = dlist.copy()
    assert isinstance(copied, DoublyLinkedList)
    assert copied == lst


@pytest.mark.parametrize(
    ("it1", "it2"),
    [
        ([], []),
        ([1], [2, 3]),
        ([4, 2], [1, 3, 5]),
    ],
)
def test_add(it1: list, it2: list):
    lst = DoublyLinkedList(it1)
    answer = it1 + it2

    assert (lst + it2) == answer

    lst += it2
    assert lst == answer


@pytest.mark.parametrize("lst", [[], [1, 2]])
@pytest.mark.parametrize("nbr", [-1, 0, 1, 2])
def test_mul(lst: list, nbr: int):
    dlist = DoublyLinkedList(lst)

    assert (dlist * nbr) == (lst * nbr)


@pytest.mark.parametrize("lst", [[], [8], [4, 1], [3, 5, 1, 2, 1, 6, 3, 4]])
def test_sort(lst: list):
    dlist = DoublyLinkedList(lst)

    dlist.sort()

    assert dlist == sorted(lst)


@pytest.mark.parametrize(
    ("lst", "value"),
    [
        ([], 1),
        ([1, 2, 1, 0, 1, 3], 1),
    ],
)
def test_count(lst: list, value: Any):
    dlist = DoublyLinkedList(lst)
    assert dlist.count(value) == lst.count(value)


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
    dlist = DoublyLinkedList(lst)

    lindex = 0
    with expectation:
        lindex = lst.index(value, start, stop)

    dindex = 0
    with expectation:
        dindex = dlist.index(value, start, stop)

    assert dindex == lindex


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
    dlist = DoublyLinkedList(list2)
    dlist.extendleft(list1)
    assert dlist == (list1 + list2)


def test_popleft():
    it = random.sample(range(100), 10)
    dlist = DoublyLinkedList(it)

    idx = 0
    while dlist:
        dlist.pop(idx)
        it.pop(idx)
        assert dlist == it

    with pytest.raises(IndexError):
        dlist.pop(idx)

    with pytest.raises(IndexError):
        dlist.pop(idx)


def test_popright():
    it = random.sample(range(100), 10)
    dlist = DoublyLinkedList(it)

    idx = -1
    while dlist:
        dlist.pop(idx)
        it.pop(idx)
        assert dlist == it

    with pytest.raises(IndexError):
        dlist.pop(idx)

    with pytest.raises(IndexError):
        dlist.pop(idx)
