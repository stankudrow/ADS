import random
from collections.abc import Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from adspy.algorithms.searching import linear_search
from adspy.algorithms.sorting import merge_sort, quick_sort
from adspy.data_structures.linked_lists import DoublyLinkedList


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


def test_from_iterable():
    it = (1, "2", [3])

    assert DoublyLinkedList.from_iterable(it) == DoublyLinkedList(it)


def test_comparisons():
    assert DoublyLinkedList([]) == DoublyLinkedList([])
    assert DoublyLinkedList([1]) == DoublyLinkedList([1])

    assert DoublyLinkedList([2]) != DoublyLinkedList([1])

    assert DoublyLinkedList([2]) > DoublyLinkedList([1])
    assert DoublyLinkedList([1]) < DoublyLinkedList([2])
    assert DoublyLinkedList([1, 2]) < DoublyLinkedList([2])
    assert DoublyLinkedList([2, 1]) > DoublyLinkedList([-1, 0, 1])

    assert DoublyLinkedList([2, 1]) <= DoublyLinkedList([2, 1])
    assert DoublyLinkedList([1, 2]) >= DoublyLinkedList([1, 2])


@pytest.mark.parametrize(
    ("it", "value", "answer"), [([], 1, False), ([1], 1, True), ([1], 0, False)]
)
def test_contains(it: list[int], value: int, answer: bool):
    assert bool(value in DoublyLinkedList(it=it)) == answer


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
    lst = DoublyLinkedList(it=it)

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
    lst = DoublyLinkedList(it=it)

    while lst:
        item = random.choice(it)

        lst.remove(value=item)
        it.remove(item)

        assert lst == it


def test_pop():
    it = random.sample(range(100), 10)
    lst = DoublyLinkedList(it=it)

    while lst:
        idx = random.choice(range(len(lst)))

        lst.pop(index=idx)
        it.pop(idx)

        assert lst == it

    with pytest.raises(IndexError):
        lst.pop()

    with pytest.raises(IndexError):
        lst.pop(100)


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
    lst = DoublyLinkedList(it=it)

    with expectation:
        it[key] = value

    with expectation:
        lst[key] = value

    assert lst == it


def test_searchability():
    sample = (-1, 0, 1, -2, 2)
    lst = DoublyLinkedList(it=sample)

    value = random.choice(sample)

    assert linear_search(it=lst, value=value) == sample.index(value)


def test_sortability():
    sample = random.sample(range(1, 100, 2), 20)
    lst = DoublyLinkedList(it=sample)

    answer = sorted(sample)

    assert merge_sort(seq=lst) == answer
    assert quick_sort(seq=lst) == answer


def test_insert():
    lst: list[int] = []
    dlist = DoublyLinkedList()

    idx, val = 0, 21
    lst.insert(idx, val)
    dlist.insert(index=idx, value=val)
    assert lst == dlist

    lst.clear()
    dlist.clear()

    idx = -1
    lst.insert(idx, val)
    dlist.insert(index=idx, value=val)
    assert lst == dlist

    for i in (0, -1, 2, -2, -3, 4):
        new_val = val * i

        lst.insert(i, new_val)
        dlist.insert(index=i, value=new_val)

        assert dlist == lst


@pytest.mark.parametrize("it", [[], [0], [1, 2], [1, -1, 0]])
def test_reversed(it: list[int]):
    icopy = it.copy()
    lst = DoublyLinkedList(it=icopy)

    assert tuple(reversed(lst)) == tuple(reversed(icopy))
