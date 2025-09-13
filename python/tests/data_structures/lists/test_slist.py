from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from random import randint, randrange
from typing import Any

import pytest

from adspy.data_structures.lists import SinglyLinkedList


def test_append() -> None:
    slist = SinglyLinkedList()

    slist.append(21)
    assert len(slist) == 1

    slist.append(42)
    assert len(slist) == 2

    assert slist[0] == 21
    assert slist[1] == 42


def test_prepend() -> None:
    slist = SinglyLinkedList()

    slist.prepend(21)
    assert len(slist) == 1

    slist.prepend(42)
    assert len(slist) == 2

    assert slist[1] == 21
    assert slist[0] == 42


def test_prepend_and_append():
    slist = SinglyLinkedList()

    slist.prepend(1)
    assert slist == [1]

    slist.append(-2)
    assert slist == [1, -2]

    slist.append(3)
    assert slist == [1, -2, 3]

    slist.prepend(4)
    assert slist == [4, 1, -2, 3]

    slist.append(-5)
    assert slist == [4, 1, -2, 3, -5]

    slist.prepend(6)
    assert slist == [6, 4, 1, -2, 3, -5]
    assert len(slist) == 6


def test_getitem() -> None:
    slist = SinglyLinkedList()

    with pytest.raises(IndexError):
        slist[0]

    assert slist[::] == []

    it = [1, 2, 3, 5, -3, 4]
    slist = SinglyLinkedList(it)

    assert slist[0] == it[0]
    assert slist[0:] == it[0:]
    assert slist[:3] == it[:3]
    assert slist[:10] == it[:10]
    assert slist[1:7:2] == it[1:7:2]
    assert slist[::1] == it[::1]

    assert it[-1] == slist[-1]
    with pytest.raises(IndexError):
        it[-100]
    with pytest.raises(IndexError):
        slist[-100]

    assert slist[5:0:-1] == it[5:0:-1]
    assert slist[-1:-6:-1] == it[-1:-6:-1]
    assert slist[100:-100:-1] == it[100:-100:-1]
    assert slist[-100:100:-1] == it[-100:100:-1]
    assert slist[100:-100:1] == it[100:-100:1]
    assert slist[-100:100:1] == it[-100:100:1]

    with pytest.raises(ValueError):
        it[::0]
    with pytest.raises(ValueError):
        slist[::0]

    assert slist[-50:2:3] == it[-50:2:3]
    assert slist[0:50:2] == it[0:50:2]

    assert slist[::] == it


@pytest.mark.parametrize(
    ("it", "extendee"),
    [
        ([], []),
        ([], [1]),
        ([2], []),
        ([3], [4, 5]),
    ],
)
def test_extend(it: Iterable, extendee: Iterable) -> None:
    slist = SinglyLinkedList(it)
    slist.extend(extendee)

    assert slist == (it + extendee)


def test_clear() -> None:
    slist = SinglyLinkedList([1, 4, 1, 0, 1, 5])

    for _ in range(2):
        slist.clear()
        assert slist == []
        assert len(slist) == 0
        assert bool(slist) is False


def test_addition() -> None:
    slist = SinglyLinkedList([1, 3])

    addendum = [2, 4]
    answer = [1, 3] + addendum

    assert slist + addendum == answer

    slist += addendum
    assert slist == answer

    assert slist + [] == answer


def test_multiplication() -> None:
    it = [-1, 0, 1]
    slist = SinglyLinkedList(it)

    assert slist * 0 == []
    assert slist * 1 == slist
    assert slist * 2 == it * 2
    assert slist * -1 == it * -1


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
    slist = SinglyLinkedList(lst)

    assert lst.count(val) == slist.count(val)


def test_extendleft() -> None:
    slist = SinglyLinkedList()

    addendum = [1, 2, 3]
    slist.extendleft(addendum)

    assert slist == addendum

    rev = list(reversed(addendum))
    slist.extendleft(rev)

    assert slist == rev + addendum


def test_insert() -> None:
    slist = SinglyLinkedList()
    lst = []

    slist.insert(0, -1)
    lst.insert(0, -1)
    assert slist == lst

    slist.insert(-1, 1)
    lst.insert(-1, 1)
    assert slist == lst

    size = len(slist)
    slist.insert(size, 1)
    lst.insert(size, 1)
    assert slist == lst

    size = len(slist) + 3
    slist.insert(size, 1)
    lst.insert(size, 1)
    assert slist == lst

    idx = 0 - len(slist)
    slist.insert(idx, 1)
    lst.insert(idx, 1)
    assert slist == lst

    idx = len(slist) // 2
    slist.insert(idx, 50)
    lst.insert(idx, 50)
    assert slist == lst

    idx = -(len(slist) // 2)
    slist.insert(idx, 80)
    lst.insert(idx, 80)
    assert slist == lst

    idx = len(slist) - 1
    slist.insert(idx, 90)
    lst.insert(idx, 90)
    assert slist == lst

    idx = len(slist) - 2
    slist.insert(idx, -100)
    lst.insert(idx, -100)
    assert slist == lst

    for _ in range(10):
        idx = randrange(0, len(slist))
        value = randint(-100, 100)
        slist.insert(idx, value)
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
    lst = SinglyLinkedList(it)

    with expectation:
        it[key] = value

    with expectation:
        # import ipdb
        # ipdb.set_trace()
        lst[key] = value

    assert lst == it


def test_index() -> None:
    slist = SinglyLinkedList()

    with pytest.raises(ValueError):
        slist.index(0)

    with pytest.raises(ValueError):
        slist.index(0, start=10)

    with pytest.raises(ValueError):
        slist.index(0, start=0, stop=-1)

    slist.insert(0, 42)
    assert slist.index(42) == 0

    slist.insert(-1, 21)
    assert slist.index(42) == 1

    assert slist.index(21, start=0) == 0
    with pytest.raises(ValueError):
        slist.index(21, start=1)

    assert slist.index(42, start=0, stop=10) == 1
    with pytest.raises(ValueError):
        slist.index(42, stop=1)


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
    lst = SinglyLinkedList(it)

    with expectation:
        del it[key]

    with expectation:
        del lst[key]

    assert lst == it


def test_remove() -> None:
    it = [-1, 0, -1, 2, 0, 5, 5]
    slist = SinglyLinkedList(it)

    for item in set(it):
        it.remove(item)
        slist.remove(item)
        assert it == slist

    with pytest.raises(ValueError):
        it.remove(-100)
    with pytest.raises(ValueError):
        slist.remove(-100)


def test_popleft() -> None:
    lst = [-1, 6, 3, 4, 4, 2]
    slist = SinglyLinkedList(lst)

    while lst:
        lst_item = lst.pop(0)
        slist_item = slist.popleft()

        assert lst_item == slist_item
        assert len(lst) == len(slist)

    with pytest.raises(IndexError):
        slist.popleft()


def test_popright() -> None:
    lst = [-1, 6, 3, 4, 4, 2]
    slist = SinglyLinkedList(lst)

    while lst:
        lst_item = lst.pop(-1)
        slist_item = slist.popright()

        assert lst_item == slist_item
        assert len(lst) == len(slist)

    with pytest.raises(IndexError):
        slist.popright()


def test_pop() -> None:
    lst = [-1, 6, 3, 4, 4, 2, -1, 0, 6, 5, 2]
    slist = SinglyLinkedList(lst)

    assert slist.pop(0) == lst.pop(0)
    assert slist.pop() == lst.pop()
    assert slist == lst

    while lst:
        idx = randrange(0, len(lst))
        assert slist.pop(idx) == lst.pop(idx)
        assert slist == lst

    assert not slist

    with pytest.raises(IndexError):
        slist.pop(100)


def test_reverse() -> None:
    it = [-1, -2, 0, 1, 3]
    slist = SinglyLinkedList(it)
    rev = tuple(reversed(it))

    assert tuple(reversed(slist)) == rev
    assert slist == it

    slist.reverse()
    assert slist == rev


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

    slist = SinglyLinkedList(it)
    assert sorted(slist, key=key, reverse=reverse) == sit
    assert slist == tup

    slist = SinglyLinkedList(it)
    slist.sort(key=key, reverse=reverse)
    assert slist == sit


def test_contains() -> None:
    slist = SinglyLinkedList([1, 0, 1, -2, 0])

    assert 0 in slist
    assert -2 in slist
    assert -3 not in slist
    assert [0, 1] not in slist
