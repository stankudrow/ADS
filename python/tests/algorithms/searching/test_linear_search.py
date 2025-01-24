from collections.abc import Iterable
from typing import Any

import pytest

from adspy.algorithms.searching.linear_search import linear_search


@pytest.mark.parametrize(
    ("it", "elem", "ans"),
    [
        ([], 21, None),
        ([1, 2], 42, None),
        ((1, 2), 2, 1),
        ((2, 1), 2, 0),
    ],
)
def test_linear_search(it: Iterable, elem: Any, ans: None | int):
    lst = list(it)
    assert linear_search(lst, elem) == ans
