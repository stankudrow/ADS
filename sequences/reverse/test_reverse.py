#!/usr/bin/env python3
"""Reversing a sequence."""


from typing import Sequence

from pytest import mark

from reverse import (
    reverse_iterative,
    reverse_recursive,
)


@mark.parametrize(
    "seq",
    [
        "",
        "1",
        "12",
        "1a2b",
        (-2, -1, 0, 1, 2),
    ],
)
def test_reverse(seq: Sequence):
    """test_reverse

    Parameters
    ----------
    seq : Sequence
    """
    assert (
        reverse_iterative(seq)
        == reverse_recursive(seq)
        == seq[::-1]
    )
