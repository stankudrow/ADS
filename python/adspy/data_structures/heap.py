"""Heap data structure.

References:
- https://docs.python.org/3/library/heapq.html
- https://github.com/python/cpython/blob/3.13/Lib/heapq.py
- https://www.tutorialspoint.com/data_structures_algorithms/heap_data_structure.htm
"""

from collections.abc import Iterable
from functools import total_ordering
from operator import ge, le
from typing import Any

from adspy.data_structures.lists import DoublyLinkedList


@total_ordering
class Heap:
    """Heap data structure.

    Heap is a binary tree => parent-child relationship.
    There are two kinds of heap:
    - min heap - a parent is less than or equal to its children;
    - max heap - a parent is greater than or equal to its children.

    The traversal order is:
    - top-to-bottom across levels;
    - left-to-right within each level.

    A Heap can be used ad an implementation detail for priority queues:
    - accessing min-max is O(1)
    - inserting/deleting is O(log n)
    """

    __slots__ = ("_c", "_cmp")

    def __init__(
        self, it: None | Iterable = None, *, is_max: bool = False
    ) -> None:
        # comparator for `cmp(parent, child)`
        self._cmp = ge if is_max else le
        # for simplicity sake, list is OK (a dynamic array will also do)
        self._c = DoublyLinkedList()  # SinglyLinkedList - tests OK
        self.extend(list(it or []))

    def __bool__(self) -> bool:
        return bool(self._c)

    def __eq__(self, other: object) -> bool:
        return self._c == other

    def __hash__(self) -> int:
        return hash(self._c)

    def __len__(self) -> int:
        return len(self._c)

    def __lt__(self, other: object) -> bool:
        return self._c < other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self._c})"

    def _normalize_index(self, idx: int) -> int:
        if idx < 0:
            idx = len(self) + idx
        return idx

    def _parent_idx(self, child_idx: int) -> int:
        return (child_idx - 1) // 2

    def _left_child_idx(self, parent_idx: int) -> int:
        return 2 * parent_idx + 1

    def _right_child_idx(self, parent_idx: int) -> int:
        return 2 * parent_idx + 2

    def _swap(self, idx1: int, idx2: int) -> None:
        self._c[idx1], self._c[idx2] = self._c[idx2], self._c[idx1]

    def _sift_up(self, idx: int) -> None:
        idx = self._normalize_index(idx)
        while idx:
            pidx = self._parent_idx(idx)
            if self._cmp(self._c[pidx], self._c[idx]):
                break
            self._swap(pidx, idx)
            idx = pidx

    def _sift_down(self, idx: int, endpos: int) -> None:
        idx, endpos = map(self._normalize_index, (idx, endpos))
        while True:
            largest_idx = idx
            if (chidx := self._left_child_idx(idx)) < endpos and not self._cmp(
                self._c[largest_idx], self._c[chidx]
            ):
                largest_idx = chidx
            if (chidx := self._right_child_idx(idx)) < endpos and not self._cmp(
                self._c[largest_idx], self._c[chidx]
            ):
                largest_idx = chidx
            if largest_idx == idx:
                break
            self._swap(largest_idx, idx)
            idx = largest_idx

    def extend(self, values: Iterable) -> None:
        """Extend heap from the right with the values.

        Parameters
        ----------
        values : Iterable

        Returns
        -------
        None
        """
        for item in values:
            self.push(item)

    def peek(self) -> Any:
        """Return the root element without removing it.

        Returns
        -------
        Any
        """
        return self._c[0]

    def push(self, item: Any) -> None:
        """Push an `item` onto the heap.

        The item is sift up to maintain the heap property.

        Parameters
        ----------
        item : Any

        Returns
        -------
        None
        """
        self._c.append(item)
        self._sift_up(-1)

    def pop(self) -> Any:
        """Pop the first item from the heap.

        Returns
        -------
        Any
        """
        root = self._c[0]
        last = self._c.pop()
        if size := len(self):
            self._c[0] = last
            self._sift_down(0, size)
        return root
