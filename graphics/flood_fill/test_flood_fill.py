#!/usr/bin/env python3
"""Tests the Flood Fill algorithm."""


import pytest

from flood_fill import (
    flood_fill_recursive as ffrec,
)


@pytest.mark.parametrize(
    "screen, ycoord, xcoord, newval, result",
    [
        ([], 0, 0, "x", []),
        ([], 1, 1, "x", []),
        ([["x"]], 0, 0, "o", [["o"]]),
        ([["x", "x"]], 0, 1, "o", [["o", "o"]]),
        ([["x", "x"]], 0, 1, "x", [["x", "x"]]),
        ([["x", "o", "x"]], 0, 1, "t", [["x", "t", "x"]]),
        (
            [["x", "o"], ["o", "x"]],
            1,
            0,
            "?",
            [["x", "o"], ["?", "x"]],
        ),
        (
            [["x", "o", "x"], ["#", "o", "?"], ["o", "o", "o"]],
            2,
            1,
            "Z",
            [["x", "Z", "x"], ["#", "Z", "?"], ["Z", "Z", "Z"]],
        ),
        (
            [
                ["o", "x", "o", "o", "?"],
                ["x", "o", "o", "x", "?"],
                ["o", "x", "o", "o", ""],
            ],
            1,
            1,
            "?",
            [
                ["o", "x", "?", "?", "?"],
                ["x", "?", "?", "x", "?"],
                ["o", "x", "?", "?", ""],
            ],
        ),
    ],
)
def test_fllod_fill(screen, ycoord, xcoord, newval, result):
    """Tests the Flood Fill algorithm."""
    ffrec(screen, ycoord, xcoord, newval)
    assert screen == result
