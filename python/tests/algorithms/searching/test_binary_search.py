from collections.abc import Iterable
from typing import Any

import pytest

from adspy.algorithms.searching.binary_search import binary_search


@pytest.mark.parametrize(
    ("it", "elem", "ans"),
    [
        ([], 21, None),
        ([1, 2], 42, None),
        ((1, 2), 1, 0),
        ((1, 2), 2, 1),
        ((2, 1), 2, 0),
        ((1, 2, 2), 2, 1),
        ((1, 2, 2, 2), 2, 1),
        pytest.param(
            (2, 1, 3, 5, 4, 0),
            4,
            None,
            marks=pytest.mark.xfail(
                reason="an unsorted iterable for binary search"
            ),
        ),
    ],
)
def test_binary_search(it: Iterable, elem: Any, ans: None | int):
    lst = list(it)
    assert binary_search(lst, elem) == ans
