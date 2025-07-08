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


class TestDoublyLinkedListSuite:
    @pytest.mark.parametrize("elements", [[], [1], (2, 3), "456"])
    def test_prepend(self, elements: Iterable) -> None:
        lst = DoublyLinkedList()
        ans = list(elements)

        for value in elements:
            lst.prepend(value)

        assert lst == reversed(ans)
        assert len(lst) == len(ans)

    @pytest.mark.parametrize("elements", [[], [1], (2, 3), "456"])
    def test_append(self, elements: Iterable) -> None:
        lst = DoublyLinkedList()
        ans = list(elements)

        for value in elements:
            lst.append(value)

        assert lst == elements
        assert len(lst) == len(ans)

    @pytest.mark.parametrize("it", [[], [1], (2, 3), "456"])
    def test_extend(self, it: Iterable) -> None:
        lst = DoublyLinkedList()
        seq = tuple(it)

        lst.extend(it)

        assert lst == it
        assert len(lst) == len(seq)

    def test_comparisons(self) -> None:
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
        ("it", "value", "answer"),
        [([], 1, False), ([1], 1, True), ([1], 0, False)],
    )
    def test_contains(self, it: Iterable, value: int, answer: bool) -> None:
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
        self,
        it: Iterable,
        key: int | slice,
        expectation: AbstractContextManager,
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
    def test_clear(self, it: Iterable) -> None:
        lst = DoublyLinkedList(it)

        lst.clear()

        assert not len(lst)
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
        self,
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

    def test_remove(self) -> None:
        it = random.sample(range(100), 10)
        lst = DoublyLinkedList(it)

        while lst:
            item = random.choice(it)

            lst.remove(item)
            it.remove(item)

            assert lst == it

    def test_pop(self) -> None:
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
        self,
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

    def test_searchability(self) -> None:
        sample = (-1, 0, 1, -2, 2)
        lst = DoublyLinkedList(sample)

        value = random.choice(sample)

        assert linear_search(lst, value) == sample.index(value)

    def test_sortability(self) -> None:
        sample = random.sample(range(1, 100, 2), 20)
        lst = DoublyLinkedList(sample)

        answer = sorted(sample)

        assert merge_sort(seq=lst) == answer
        assert quick_sort(seq=lst) == answer

    def test_insert(self) -> None:
        lst: list[int] = []
        dlist = DoublyLinkedList()

        for idx, val in [
            (10, -1),
            (0, 12),
            (0, 21),
            (1, 42),
            (-1, 84),
            (-2, 100),
            (3, 123),
            (100, 456),
            (-100, 789),
            (5, -321),
        ]:
            lst.insert(idx, val)
            dlist.insert(idx, val)
            assert dlist == lst

    @pytest.mark.parametrize("it", [[], [0], [1, 2], [1, -1, 0]])
    def test_reversing(self, it: list) -> None:
        icopy = it.copy()
        lst = DoublyLinkedList(icopy)
        rev = tuple(reversed(icopy))

        assert tuple(reversed(lst)) == rev

        lst.reverse()
        assert lst == rev

    @pytest.mark.parametrize("it", [[], [1, "2", [3, [4, 5]]]])
    def test_copy(self, it: Iterable) -> None:
        dlist = DoublyLinkedList(it)

        copied = copy.copy(dlist)
        assert isinstance(copied, DoublyLinkedList)
        assert copied == it

        copied = dlist.copy()
        assert isinstance(copied, DoublyLinkedList)
        assert copied == it

    @pytest.mark.parametrize(
        ("it1", "it2"),
        [
            ([], []),
            ([1], [2, 3]),
            ([4, 2], [1, 3, 5]),
        ],
    )
    def test_add(self, it1: list, it2: list) -> None:
        lst = DoublyLinkedList(it1)
        answer = it1 + it2

        assert (lst + it2) == answer

        lst += it2
        assert lst == answer

    @pytest.mark.parametrize("lst", [[], [1, 2]])
    @pytest.mark.parametrize("nbr", [-1, 0, 1, 2])
    def test_mul(self, lst: list, nbr: int) -> None:
        dlist = DoublyLinkedList(lst)

        assert (dlist * nbr) == (lst * nbr)

    @pytest.mark.parametrize("lst", [[], [8], [4, 1], [3, 5, 1, 2, 1, 6, 3, 4]])
    def test_sort(self, lst: list) -> None:
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
    def test_count(self, lst: list, value: Any) -> None:
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
        self,
        lst: list,
        value: Any,
        start: int,
        stop: int,
        expectation: AbstractContextManager,
    ) -> None:
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
    def test_extendleft(self, list1: list, list2: list) -> None:
        dlist = DoublyLinkedList(list2)
        dlist.extendleft(list1)
        assert dlist == (list1 + list2)

    def test_popleft(self) -> None:
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

    def test_popright(self) -> None:
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
