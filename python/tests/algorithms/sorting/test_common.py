from collections.abc import Callable, Sequence
from operator import itemgetter

import pytest

from adspy.algorithms.sorting.common import (
    is_sorted,
    merge,
)


@pytest.mark.parametrize(
    ("seq, reverse, strict, ans"),
    [
        ([], False, False, True),
        ([], True, False, True),
        ([1, 2], False, False, True),
        ([1, 2], False, True, True),
        ([3, 3], False, False, True),
        ([3, 3], True, False, True),
        ([3, 3], False, True, False),
        ([3, 3], True, True, False),
        ([4, 5], True, False, False),
        ([4, 5], False, False, True),
    ],
)
def test_is_sorted(seq: Sequence, reverse: bool, strict: bool, ans: bool):
    assert is_sorted(tuple(seq), reverse=reverse, strict=strict) == ans


@pytest.mark.parametrize(
    ("seq, key, ans"),
    [
        ([], None, True),
        (
            [(2, 1), (3, 4)],
            itemgetter(-1),
            True,
        ),
        (
            [(2, 1), (3, 0)],
            itemgetter(-1),
            False,
        ),
    ],
)
def test_is_sorted_key(seq: Sequence, key: None | Callable, ans: bool):
    assert is_sorted(tuple(seq), key=key) == ans


@pytest.mark.parametrize(
    ("seq1", "seq2", "reverse", "ans"),
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
def test_merge(seq1: Sequence, seq2: Sequence, reverse: bool, ans: list):
    assert merge(seq1=seq1, seq2=seq2, reverse=reverse) == ans
