"""Test the "Bubble sort" implementation(s)."""

from collections.abc import Callable, Sequence
from operator import itemgetter

import pytest

from adspy.algorithms.sorting.bubble_sort import bubble_sort


@pytest.mark.parametrize(
    "seq, key, reverse",
    [
        ([], None, False),
        ([1], None, False),
        ([2, 1], None, False),
        pytest.param(
            (1, 0, -1),
            None,
            True,
            marks=pytest.mark.xfail(reason="unstable"),
        ),
        pytest.param(
            (-7, 5, 2, -5),
            None,
            False,
            marks=pytest.mark.xfail(reason="unstable"),
        ),
        (
            [(2, 1), (3, 4), (5, -5), (0, 2)],
            itemgetter(-1),
            True,
        ),
        pytest.param(
            [-2, 2, 1, 0, -1],
            abs,
            False,
            marks=pytest.mark.xfail(reason="mutual ambiguity"),
        ),
        pytest.param(
            [0],
            5,
            False,
            marks=pytest.mark.xfail(reason="key is not callable"),
        ),
    ],
)
def test_bubble_sort(seq: Sequence, key: None | Callable, reverse: bool):
    lst = list(seq)

    result = bubble_sort(lst, key=key, reverse=reverse)
    expected = sorted(lst, key=key, reverse=reverse)

    assert result == expected
