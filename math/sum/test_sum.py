#!/usr/bin/env python3
"""Summing the elements of a sequence."""


from typing import Sequence

from pytest import mark

from sum_ import sum_recursive, sum_iterative


@mark.parametrize(
    "seq",
    [
        [],
        [0],
        [1],
        [0, 1],
        range(5),
        range(-10, 11),
    ],
)
def test_sum(seq: Sequence):
    """test_sum

    Parameters
    ----------
    seq : Sequence
    """
    assert sum_recursive(seq) == sum_iterative(seq) == sum(seq)
