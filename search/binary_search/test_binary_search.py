#!/usr/bin/env python3
"""Tests binary search implementations."""


from typing import Any, Sequence

import pytest

from binary_search import (
    binsearch_iterative,
    binsearch_recursive,
)


@pytest.mark.parametrize(
    "seq, items_results",
    [
        pytest.param(
            None,
            [(None, None)],
            marks=pytest.mark.xfail(reason="None taken in."),
        ),
        pytest.param(
            5,
            [(5, 5)],
            marks=pytest.mark.xfail(reason="Not a sequence."),
        ),
        ("", [("", None)]),
        ("1", [("1", 0), ("2", None)]),
        ("abc", [("a", 0), ("b", 1), ("c", 2)]),
        ("defG", [("d", 0), ("e", 1), ("f", 2), ("g", None)]),
        pytest.param(
            [5, 2, 7],
            [
                (2, 1),  # OK
                (5, 0),  # Not OK
            ],
            marks=pytest.mark.xfail(reason="Not a sorted sequence."),
        ),
    ],
)
def test_binary_search(
    seq: Sequence[Any], items_results: list[tuple[Any, Any]]
):
    """Tests binary search implementations."""
    for item, result in items_results:
        assert (
            binsearch_iterative(seq, item)
            == binsearch_recursive(seq, item)
            == result
        )
