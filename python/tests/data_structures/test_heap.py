"""Test the Heap data structure.

Python heapification and Heap's one do differ,
however insert-remove operations are OK.
The reason is the Heap does not tend to place minimum items leftmost.

References:
- https://docs.python.org/3.13/library/heapq.html
- https://github.com/python/cpython/blob/3.13/Lib/heapq.py
"""

import heapq
from collections.abc import Iterable

import pytest

from adspy.data_structures import Heap


# Only Python3.14+
@pytest.fixture
def max_heap() -> Heap:
    return Heap(is_max=True)


@pytest.fixture
def min_heap() -> Heap:
    return Heap()


class TestMinHeap:
    @pytest.mark.parametrize(
        "items",
        [
            [],
            [1],
            (10, 5, 15, 1, 2, -1, 7, 2, 3, -2, 4, 9, 10, 5),
            (6, 3, 8, 2, 0, 10, 5, 3, 2, 6, 9, -1),
            (10, 5, 15, 1, 2, 7, 3, 4, 9, 10, 5),
        ],
    )
    def test_push(self, items: Iterable, min_heap: Heap) -> None:
        heapq_heap = []

        for item in items:
            min_heap.push(item)
            heapq.heappush(heapq_heap, item)

        assert min_heap == heapq_heap

    @pytest.mark.parametrize(
        "items",
        [
            [],
            [1],
            (10, 5, 15, 1, 2, -1, 7, 2, 3, -2, 4, 9, 10, 5),
            (6, 3, 8, 2, 0, 10, 5, 3, 2, 6, 9, -1),
            (10, 5, 15, 1, 2, 7, 3, 4, 9, 10, 5),
        ],
    )
    def test_extend(self, items: Iterable, min_heap: Heap) -> None:
        min_heap.extend(items)
        heapq_heap = []
        for item in items:
            heapq.heappush(heapq_heap, item)

        # heapq_heap = list(items)
        # heapq.heapify(heapq_heap)  # fails

        assert min_heap == heapq_heap

    @pytest.mark.parametrize(
        "items",
        [
            [],
            [1],
            (10, 5, 15, 1, 2, -1, 7, 2, 3, -2, 4, 9, 10, 5),
            (6, 3, 8, 2, 0, 10, 5, 3, 2, 6, 9, -1),
            (10, 5, 15, 1, 2, 7, 3, 4, 9, 10, 5),
        ],
    )
    def test_pop(self, items: Iterable, min_heap: Heap) -> None:
        min_heap.extend(items)

        heapq_heap = []
        for item in items:
            heapq.heappush(heapq_heap, item)

        for _ in range(len(min_heap)):
            assert min_heap.pop() == heapq.heappop(heapq_heap)
            # assert min_heap == heapq_heap  # fails

    def test_peak(self, min_heap: Heap) -> None:
        with pytest.raises(IndexError):
            min_heap.peek()

        min_heap.push(10)
        assert min_heap.peek() == 10

        min_heap.push(5)
        assert min_heap.peek() == 5
