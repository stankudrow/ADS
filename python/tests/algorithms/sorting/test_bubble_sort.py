"""Test the "Bubble sort" implementation(s)."""

from collections.abc import Callable, Sequence

import pytest

from adspy.algorithms.sorting import bubble_sort

sort = bubble_sort


@pytest.mark.parametrize(
    "seq",
    [
        [],
        [1],
        (2, 0, 1),
        {2, 4, 3, 1},
        [-5, 4, 6, 3, 0],
        (3, 4, 2, 1, 1, 0, 2, 3),
    ],
)
@pytest.mark.parametrize(
    "key",
    [
        None,
        abs,
        lambda x: x * x,
    ],
)
@pytest.mark.parametrize(
    "reverse",
    [
        False,
        True,
    ],
)
def test_sort(seq: Sequence, key: None | Callable, reverse: bool) -> None:
    lst = list(seq)

    result = sort(lst, key=key, reverse=reverse)
    expected = sorted(lst, key=key, reverse=reverse)

    assert result == expected
