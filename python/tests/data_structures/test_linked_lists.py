from collections.abc import Iterable

import pytest

from adspy.data_structures.linked_lists import LinkedList


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_prepend(elements: Iterable):
    lst = LinkedList()
    ans = list(elements)

    for value in elements:
        lst.prepend(value)

    assert lst == reversed(ans)
    assert len(lst) == len(ans)


@pytest.mark.parametrize("elements", [[1], (2, 3), "456"])
def test_append(elements: Iterable):
    lst = LinkedList()
    ans = list(elements)

    for value in elements:
        lst.append(value)

    assert lst == elements
    assert len(lst) == len(ans)


@pytest.mark.parametrize("it", [[], "123"])
def test_extend(it: Iterable):
    lst = LinkedList()
    seq = tuple(it)

    lst.extend(it)

    assert lst == it
    assert len(lst) == len(seq)


def test_from_iterable():
    it = (1, "2", [3])

    assert LinkedList.from_iterable(it) == LinkedList(it)


def test_comparisons():
    assert LinkedList([]) == LinkedList([])
    assert LinkedList([1]) == LinkedList([1])

    assert LinkedList([2]) != LinkedList([1])

    assert LinkedList([2]) > LinkedList([1])
    assert LinkedList([1]) < LinkedList([2])
    assert LinkedList([1, 2]) < LinkedList([2])
    assert LinkedList([2, 1]) > LinkedList([-1, 0, 1])

    assert LinkedList([2, 1]) <= LinkedList([2, 1])
    assert LinkedList([1, 2]) >= LinkedList([1, 2])


@pytest.mark.parametrize(
    ("it", "key"),
    [([1], 0), ([1, 2], -1), ([3, 4, 5], slice(0, 3, 2))],
)
def test_get_items(it: list[int], key: int | slice):
    lst = LinkedList(it=it)

    assert lst[key] == it[key]


@pytest.mark.parametrize("it", [[], [1], [-1, 0, 1]])
def test_clear(it: list[int]):
    lst = LinkedList(it)

    lst.clear()

    assert len(lst) == 0
    assert not tuple(lst)

    with pytest.raises(IndexError):
        lst[0]


@pytest.mark.parametrize(
    ("it", "key"),
    [([1], 0), ([1, 2], -1), ([3, 4, 5], slice(0, 3, 2))],
)
def test_delete_items(it: list[int], key: int | slice):
    lst = LinkedList(it)

    del lst[key]
    del it[key]

    assert lst == it
