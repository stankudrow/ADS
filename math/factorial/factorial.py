#!/usr/bin/env python3
"""Factoral problem."""


from functools import lru_cache


@lru_cache
def factorial_recursive(nbr: int) -> int:
    """factorial_recursive

    Parameters
    ----------
    nbr : int

    Returns
    -------
    int

    Raises
    ------
    ValueError
        if nbr < 0
    """
    if nbr < 0:
        raise ValueError(f"{nbr} is negative.")
    if nbr < 2:
        return 1
    return nbr * factorial_recursive(nbr - 1)


def factorial_iterative(nbr: int) -> int:
    """factorial_iterative

    Parameters
    ----------
    nbr : int

    Returns
    -------
    int

    Raises
    ------
    ValueError
        if nbr < 0
    """
    if nbr < 0:
        raise ValueError(f"{nbr} is negative.")
    if nbr < 2:
        return 1
    factorial: int = 2
    for factor in range(3, nbr + 1):
        factorial *= factor
    return factorial
