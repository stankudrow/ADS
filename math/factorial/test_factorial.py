#!/usr/bin/env python3
"""Factoral problem."""


from pytest import mark, param

from factorial import factorial_recursive, factorial_iterative


@mark.parametrize(
    "nbr, result",
    [
        param(
            -1, ValueError, marks=mark.xfail(reason="negative")
        ),
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
    ],
)
def test_factorial(nbr: int, result: int):
    """test_factorial

    Parameters
    ----------
    nbr : int
    result : int
    """
    assert (
        factorial_recursive(nbr)
        == factorial_iterative(nbr)
        == result
    )
