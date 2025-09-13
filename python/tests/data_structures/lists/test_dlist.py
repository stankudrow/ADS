from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from random import randint, randrange
from typing import Any

import pytest

from adspy.data_structures.lists import DoublyLinkedList


def test_append() -> None:
    dlist = DoublyLinkedList()

    dlist.append(21)
    assert len(dlist) == 1

    dlist.append(42)
    assert len(dlist) == 2

    assert dlist[0] == 21
    assert dlist[1] == 42


def test_prepend() -> None:
    dlist = DoublyLinkedList()

    dlist.prepend(21)
    assert len(dlist) == 1

    dlist.prepend(42)
    assert len(dlist) == 2

    assert dlist[1] == 21
    assert dlist[0] == 42


def test_prepend_and_append():
    dlist = DoublyLinkedList()

    dlist.prepend(1)
    assert dlist == [1]

    dlist.append(-2)
    assert dlist == [1, -2]

    dlist.append(3)
    assert dlist == [1, -2, 3]

    dlist.prepend(4)
    assert dlist == [4, 1, -2, 3]

    dlist.append(-5)
    assert dlist == [4, 1, -2, 3, -5]

    dlist.prepend(6)
    assert dlist == [6, 4, 1, -2, 3, -5]
    assert len(dlist) == 6


def test_getitem() -> None:
    dlist = DoublyLinkedList()

    with pytest.raises(IndexError):
        dlist[0]

    assert dlist[::] == []

    it = [1, 2, 3, 5, -3, 4]
    dlist = DoublyLinkedList(it)

    assert dlist[0] == it[0]
    assert dlist[0:] == it[0:]
    assert dlist[:3] == it[:3]
    assert dlist[:10] == it[:10]
    assert dlist[1:7:2] == it[1:7:2]
    assert dlist[::1] == it[::1]

    assert it[-1] == dlist[-1]
    with pytest.raises(IndexError):
        it[-100]
    with pytest.raises(IndexError):
        dlist[-100]

    assert dlist[5:0:-1] == it[5:0:-1]
    assert dlist[-1:-6:-1] == it[-1:-6:-1]
    assert dlist[100:-100:-1] == it[100:-100:-1]
    assert dlist[-100:100:-1] == it[-100:100:-1]
    assert dlist[100:-100:1] == it[100:-100:1]
    assert dlist[-100:100:1] == it[-100:100:1]

    with pytest.raises(ValueError):
        it[::0]
    with pytest.raises(ValueError):
        dlist[::0]

    assert dlist[-50:2:3] == it[-50:2:3]
    assert dlist[0:50:2] == it[0:50:2]

    assert dlist[::] == it


@pytest.mark.parametrize(
    ("it", "extendee"),
    [
        ([], []),
        ([], [1]),
        ([2], []),
        ([3], [4, 5]),
    ],
)
def test_extend(it: list[int], extendee: list[int]) -> None:
    dlist = DoublyLinkedList(it)
    dlist.extend(extendee)

    assert dlist == (it + extendee)


def test_clear() -> None:
    dlist = DoublyLinkedList([1, 4, 1, 0, 5])

    for _ in range(2):
        dlist.clear()
        assert dlist == []
        assert len(dlist) == 0
        assert bool(dlist) is False


def test_addition() -> None:
    dlist = DoublyLinkedList([1, 3])

    addendum = [2, 4]
    answer = [1, 3] + addendum

    assert dlist + addendum == answer

    dlist += addendum
    assert dlist == answer

    assert dlist + [] == answer


def test_multiplication() -> None:
    it = [-1, 0, 1]
    dlist = DoublyLinkedList(it)

    assert dlist * 0 == []
    assert dlist * 1 == dlist
    assert dlist * 2 == it * 2
    assert dlist * -1 == it * -1


@pytest.mark.parametrize(
    ("it", "val"),
    [
        ([], 0),
        ([1, 2], 3),
        ([1, 2, 2, 3], 2),
    ],
)
def test_count(it: Iterable, val: Any) -> None:
    lst = list(it)
    dlist = DoublyLinkedList(lst)

    assert lst.count(val) == dlist.count(val)


def test_extendleft() -> None:
    dlist = DoublyLinkedList()

    addendum = [1, 2, 3]
    dlist.extendleft(addendum)

    assert dlist == addendum

    rev = list(reversed(addendum))
    dlist.extendleft(rev)

    assert dlist == rev + addendum


def test_insert() -> None:
    dlist = DoublyLinkedList()
    lst: list[int] = []

    dlist.insert(0, -1)
    lst.insert(0, -1)
    assert dlist == lst

    dlist.insert(-1, 1)
    lst.insert(-1, 1)
    assert dlist == lst

    size = len(dlist)
    dlist.insert(size, 1)
    lst.insert(size, 1)
    assert dlist == lst

    size = len(dlist) + 3
    dlist.insert(size, 1)
    lst.insert(size, 1)
    assert dlist == lst

    idx = 0 - len(dlist)
    dlist.insert(idx, 1)
    lst.insert(idx, 1)
    assert dlist == lst

    idx = len(dlist) // 2
    dlist.insert(idx, 50)
    lst.insert(idx, 50)
    assert dlist == lst

    idx = -(len(dlist) // 2)
    dlist.insert(idx, 80)
    lst.insert(idx, 80)
    assert dlist == lst

    idx = len(dlist) - 1
    dlist.insert(idx, 90)
    lst.insert(idx, 90)
    assert dlist == lst

    idx = len(dlist) - 2
    dlist.insert(idx, -100)
    lst.insert(idx, -100)
    assert dlist == lst

    idx = -100
    dlist.insert(idx, 321)
    lst.insert(idx, 321)
    assert dlist == lst

    for _ in range(10):
        idx = randrange(0, len(dlist))
        value = randint(-100, 100)
        dlist.insert(idx, value)
        lst.insert(idx, value)


@pytest.mark.parametrize(
    ("it", "key", "value", "expectation"),
    [
        ([], 0, 0, pytest.raises(IndexError)),
        ([], -1, 0, pytest.raises(IndexError)),
        ([], slice(-1, 0, 1), [0], does_not_raise()),
        ([], slice(0, 3, 1), [1], does_not_raise()),
        ([], slice(1, 3, 1), [1], does_not_raise()),
        ([1], slice(0, 4, 1), [2], does_not_raise()),
        ([2], slice(1, 4, 1), [3], does_not_raise()),
        ([3], slice(2, 4, 1), [4, 5], does_not_raise()),
        ([1], 0, "2", does_not_raise()),
        ([1, 2], -1, "a", does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), [-1, 1], does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), [-1, [0, 1]], does_not_raise()),
        ([5, 6, 7], slice(0, 3, 2), [-1, 0, 1], pytest.raises(ValueError)),
        ([1, 1, 1, 1], slice(1, 3, 1), [2, 3], does_not_raise()),
        ([1, 3, 1, 1, 2], 2, "T", does_not_raise()),
        ([1, 2, 3], 2, [2, 3], does_not_raise()),
        ([3, 2, 1], slice(0, 2, 1), 21, pytest.raises(TypeError)),
    ],
)
def test_setitem(
    it: list,
    key: int | slice,
    value: Any,
    expectation: AbstractContextManager,
) -> None:
    lst = DoublyLinkedList(it)

    with expectation:
        it[key] = value

    with expectation:
        lst[key] = value

    assert lst == it


def test_index() -> None:
    dlist = DoublyLinkedList()

    with pytest.raises(ValueError):
        dlist.index(0)

    with pytest.raises(ValueError):
        dlist.index(0, start=10)

    with pytest.raises(ValueError):
        dlist.index(0, start=0, stop=-1)

    dlist.insert(0, 42)
    assert dlist.index(42) == 0

    dlist.insert(-1, 21)
    assert dlist.index(42) == 1

    assert dlist.index(21, start=0) == 0
    with pytest.raises(ValueError):
        dlist.index(21, start=1)

    assert dlist.index(42, start=0, stop=10) == 1
    with pytest.raises(ValueError):
        dlist.index(42, stop=1)


@pytest.mark.parametrize(
    ("it", "key", "expectation"),
    [
        ([], 0, pytest.raises(IndexError)),
        ([], -1, pytest.raises(IndexError)),
        ([], slice(0, 3, 1), does_not_raise()),
        ([1], 0, does_not_raise()),
        ([1], -1, does_not_raise()),
        ([1], slice(0, 3, 1), does_not_raise()),
        ([1], slice(3, 0, -1), does_not_raise()),
        ([3, 4, 5], slice(0, 3, 2), does_not_raise()),
        ([3, 4, 5], slice(4, -1, -1), does_not_raise()),
        ([3, 4, 5], slice(100, 200, 5), does_not_raise()),
        ([1, 1, 1, 1], slice(1, 3, 1), does_not_raise()),
        ([1, 3, 1, 1, 2], -3, does_not_raise()),
    ],
)
def test_delitem(
    it: list,
    key: int | slice,
    expectation: AbstractContextManager,
) -> None:
    lst = DoublyLinkedList(it)

    with expectation:
        del it[key]

    with expectation:
        del lst[key]

    assert lst == it


def test_remove() -> None:
    it = [-1, 0, -1, 2, 0, 5, 5]
    dlist = DoublyLinkedList(it)

    for item in it:
        it.remove(item)
        dlist.remove(item)
        assert it == dlist

    with pytest.raises(ValueError):
        it.remove(-100)
    with pytest.raises(ValueError):
        dlist.remove(-100)


def test_popleft() -> None:
    lst = [-1, 6, 3, 4, 4, 2]
    dlist = DoublyLinkedList(lst)

    while lst:
        lst_item = lst.pop(0)
        dlist_item = dlist.popleft()

        assert lst_item == dlist_item
        assert len(lst) == len(dlist)

    with pytest.raises(IndexError):
        dlist.popleft()


def test_popright() -> None:
    lst = [-1, 6, 3, 4, 4, 2]
    dlist = DoublyLinkedList(lst)

    while lst:
        lst_item = lst.pop(-1)
        dlist_item = dlist.popright()

        assert lst_item == dlist_item
        assert len(lst) == len(dlist)

    with pytest.raises(IndexError):
        dlist.popright()


def test_pop() -> None:
    lst = [-1, 6, 3, 4, 4, 2, -1, 0, 6, 5, 2]
    dlist = DoublyLinkedList(lst)

    assert dlist.pop(0) == lst.pop(0)
    assert dlist.pop() == lst.pop()
    assert dlist == lst

    while lst:
        idx = randrange(0, len(lst))
        assert dlist.pop(idx) == lst.pop(idx)
        assert dlist == lst

    assert not dlist

    with pytest.raises(IndexError):
        dlist.pop(100)


def test_reverse() -> None:
    it = [-1, -2, 0, 1, 3]
    dlist = DoublyLinkedList(it)
    rev = tuple(reversed(it))

    assert tuple(reversed(dlist)) == rev
    assert dlist == it

    dlist.reverse()
    assert dlist == rev


@pytest.mark.parametrize(
    ("it", "key", "reverse"),
    [
        ([], None, False),
        ([0], None, True),
        ([1, -1], None, True),
        ([1, -1], None, False),
        ({2, 5, -1}, lambda x: x, True),
        ((-2, 6, -2, 5, -1, 0, 0), None, True),
        (["abc", "DE", "fg7@"], lambda s: len(s), False),
    ],
)
def test_sort(it: Iterable, key: None | Callable, reverse: bool) -> None:
    tup = tuple(it)
    sit = sorted(tup, key=key, reverse=reverse)

    dlist = DoublyLinkedList(it)
    assert sorted(dlist, key=key, reverse=reverse) == sit
    assert dlist == tup

    dlist = DoublyLinkedList(it)
    dlist.sort(key=key, reverse=reverse)
    assert dlist == sit


def test_contains() -> None:
    dlist = DoublyLinkedList([1, 0, 1, -2, 0])

    assert 0 in dlist
    assert -2 in dlist
    assert -3 not in dlist
    assert [0, 1] not in dlist
