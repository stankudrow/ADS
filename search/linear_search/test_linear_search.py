#!/usr/bin/env python3
"""Tests linear search implementations."""


from typing import Any, Sequence

import pytest

from linear_search import (
    linsearch_iterative,
    linsearch_recursive,
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
    ],
)
def test_linear_search(
    seq: Sequence[Any], items_results: list[tuple[Any, Any]]
):
    """Tests linear search implementations."""
    for item, result in items_results:
        assert (
            linsearch_iterative(seq, item)
            == linsearch_recursive(seq, item)
            == result
        )
