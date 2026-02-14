from collections.abc import Iterable

import pytest

from adspy.algorithms.sorting.common import merge


@pytest.mark.parametrize(
    ("it1", "it2", "reverse", "ans"),
    [
        ([4, 1], [3, 2], False, [3, 2, 4, 1]),
        ([], [3, 2], False, [3, 2]),
        ([4, 1], [], False, [4, 1]),
        ([1], [2], False, [1, 2]),
        ([], [], False, []),
        ([], [], True, []),
        ([1, 2], [], True, [1, 2]),
        ([], [3, 4], True, [3, 4]),
        ([1], [2], True, [2, 1]),
        ([2, 4], [3, 1], True, [3, 2, 4, 1]),
    ],
)
def test_merge(it1: Iterable, it2: Iterable, reverse: bool, ans: list) -> None:
    assert merge(it1, it2, reverse=reverse) == ans
