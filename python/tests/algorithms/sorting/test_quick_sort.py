"""Test the "Quick sort" implementation(s)."""

from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from operator import itemgetter

import pytest

from adspy.algorithms.sorting.common import is_sorted
from adspy.algorithms.sorting.quick_sort import quick_sort


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
def test_quick_sort(seq: Sequence, key: None | Callable, reverse: bool):
    lst = list(seq)

    result = quick_sort(lst, key=key, reverse=reverse)
    expected = sorted(lst, key=key, reverse=reverse)

    assert result == expected


@pytest.mark.parametrize(
    ("seq, key, expectation"),
    [
        ([0, 1, -1], None, does_not_raise()),
        (
            [(2, 1), (3, 4), (5, -5), (0, 2)],
            itemgetter(-1),
            does_not_raise(),
        ),
        pytest.param(
            (0, 1, -1),
            abs,
            does_not_raise(),
            marks=pytest.mark.xfail(reason="key failed to sort"),
        ),
        pytest.param(
            [0],
            5,
            pytest.raises(AssertionError),
            marks=pytest.mark.xfail(reason="key is not callable"),
        ),
    ],
)
def test_quick_sort_key(
    seq: Sequence, key: None | Callable, expectation: AbstractContextManager
):
    lst = list(seq)

    result = quick_sort(lst, key=key)

    assert is_sorted(result, key=key)
    with expectation:
        expected = sorted(lst, key=key)
        assert result == expected
