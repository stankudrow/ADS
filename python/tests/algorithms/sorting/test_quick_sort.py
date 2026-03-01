"""Test the "Quick sort" implementation(s)."""

import random
from collections.abc import Callable, Sequence

import pytest

from adspy.algorithms.sorting.quick_sort import quick_sort

sort = quick_sort


@pytest.mark.parametrize(
    "seq",
    [
        [],
        [1],
        (2, 1),
        (2, 0, 1),
        {2, 4, 3, 1},
        [2, 3, 1, 1, 5],
    ],
)
@pytest.mark.parametrize(
    "key",
    [
        None,
        abs,
    ],
)
@pytest.mark.parametrize(
    "reverse",
    [
        False,
        True,
    ],
)
def test_quick_sort(seq: Sequence, key: None | Callable, reverse: bool) -> None:
    lst = list(seq)

    result = quick_sort(lst, key=key, reverse=reverse)
    expected = sorted(lst, key=key, reverse=reverse)

    assert result == expected


def test_sort_purity() -> None:
    sample = random.sample(range(1, 100, 2), 15)
    sample_dup = sample.copy()

    assert quick_sort(sample) == sorted(sample)
    assert sample == sample_dup
