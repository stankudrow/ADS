#!/usr/bin/env python3
"""Tests for "The Towers of Hanoi" problem."""


import pytest

from hanoi_towers import hanoi_recursive


@pytest.mark.parametrize(
    "src, tmp, dst, result",
    [
        ([], [], [], []),
        ([1], [], [], [1]),
        ([1, 2], [], [], [1, 2]),
        pytest.param(
            [1],
            [2],
            [],
            [2, 1],
            marks=pytest.mark.xfail(
                reason="A bad setup: the aux rod has items."
            ),
        ),
        pytest.param(
            [-1, 0, 1],
            [],
            [2],
            [2, -1, 0, 1],
            marks=pytest.mark.xfail(
                reason="A bad setup: the dst rod has items."
            ),
        ),
    ],
)
def test_hanoi(src, tmp, dst, result):
    """Tests the implementations solving the Towers of Hanoi problem."""
    hanoi_recursive(src, tmp, dst)
    assert dst == result
    assert not (src or tmp)
