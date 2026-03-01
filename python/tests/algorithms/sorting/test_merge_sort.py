"""Test the "Merge sort" implementation(s)."""

import random
from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from operator import itemgetter

import pytest

from adspy.algorithms.sorting.merge_sort import merge_sort

sort = merge_sort


@pytest.mark.parametrize(
    "seq",
    [
        [],
        [1],
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
def test_merge_sort(seq: Sequence, key: None | Callable, reverse: bool) -> None:
    lst = list(seq)

    result = merge_sort(lst, key=key, reverse=reverse)
    expected = sorted(lst, key=key, reverse=reverse)

    assert result == expected


@pytest.mark.parametrize(
    ("seq", "key", "expectation"),
    [
        ([0, 1, -1], None, does_not_raise()),
        ([0, -1, 2, -2], lambda x: x * x, does_not_raise()),
        (
            [(2, 1), (3, 4), (5, -5), (0, 2)],
            itemgetter(-1),
            does_not_raise(),
        ),
        # pytest.param(
        #     (0, 1, -1),
        #     abs,
        #     does_not_raise(),
        #     marks=pytest.mark.xfail(reason="sort is unstable"),
        # ),
        pytest.param(
            [0],
            5,
            pytest.raises(AssertionError),
            marks=pytest.mark.xfail(reason="key is not callable"),
        ),
    ],
)
def test_sort_key(
    seq: Sequence, key: None | Callable, expectation: AbstractContextManager
) -> None:
    lst = list(seq)
    with expectation:
        result = sort(lst, key=key)
        expected = sorted(lst, key=key)
        assert result == expected


def test_sort_key_reverse() -> None:
    seq = [4, -1, 0, -2, 2, 1, 3]
    key = abs
    assert sort(seq, key=key, reverse=True) == sorted(
        seq, key=key, reverse=True
    )


def test_sort_purity() -> None:
    sample = random.sample(range(1, 100, 2), 15)
    sample_dup = sample.copy()

    assert sort(sample) == sorted(sample)
    assert sample == sample_dup
