from collections.abc import Iterable

import pytest

from adspy.algorithms.sorting.misc import merge


@pytest.mark.parametrize(
    ("it1", "it2", "ans"),
    [
        ([], [], []),
        ([], [1], [1]),
        ([2], [], [2]),
        ([3, 7, 7, 9], [4], [3, 4, 7, 7, 9]),
        ([2], [1, 1, 3], [1, 1, 2, 3]),
        (
            [2, 3, 3, 5, 5],
            [1, 2, 2, 3, 4, 6],
            [1, 2, 2, 2, 3, 3, 3, 4, 5, 5, 6],
        ),
    ],
)
def test_merge(it1: Iterable, it2: Iterable, ans: list) -> None:
    assert merge(it1, it2) == ans


@pytest.mark.parametrize(
    ("it1", "it2", "ans"),
    [
        ([], [], []),
        ([], [1], [1]),
        ([2], [], [2]),
        ([6, 4, 2], [3], [6, 4, 3, 2]),
        ([5], [9, 5, 1], [9, 5, 5, 1]),
        (
            [4, 3, 3],
            [6, 4, 3, 1, 1],
            [6, 4, 4, 3, 3, 3, 1, 1],
        ),
    ],
)
def test_merge_reverse(it1: Iterable, it2: Iterable, ans: list) -> None:
    assert merge(it1, it2, desc=True) == ans
