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
    ],
)
def test_binary_search(it: Iterable, elem: Any, ans: None | int):
    lst = list(it)
    assert binary_search(lst, elem) == ans
