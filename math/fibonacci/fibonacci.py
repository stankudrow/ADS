#!/usr/bin/env python3
"""Fibonacci sequence problem."""


from functools import lru_cache, wraps
from typing import Generator


@lru_cache
def fibonacci_recursive(nth_nbr: int) -> int:
    """fibonacci_recursive

    Parameters
    ----------
    nth_nbr : int
        The nth Fibonacci number to compute.

    Returns
    -------
    int

    Raises
    ------
    ValueError
        if nth_nbr < 1.
    """

    @wraps(fibonacci_recursive)
    def _fibrec(nbr: int) -> int:
        """Actual recursive implementation."""
        if nbr in (1, 2):
            return 1
        return _fibrec(nbr - 2) + _fibrec(nbr - 1)

    if nth_nbr < 1:
        raise ValueError(f"{nth_nbr} < 1")
    return _fibrec(nth_nbr)


def fibonacci_iterative(nth_nbr: int) -> int:
    """fibonacci_iterative

    Parameters
    ----------
    nth_nbr : int
        The nth Fibonacci number to compute.

    Returns
    -------
    int

    Raises
    ------
    ValueError
        if nth_nbr < 1.
    """
    if nth_nbr < 1:
        raise ValueError(f"{nth_nbr} < 1")
    fibcurr, fibnext = 0, 1
    for _ in range(nth_nbr):
        fibcurr, fibnext = fibnext, fibcurr + fibnext
    return fibcurr


def fibonacci_generator_iterative(
    start_with_zero: bool = True,
) -> Generator[int, None, None]:
    """fibonacci_generator_iterative

    Parameters
    ----------
    start_with_zero : bool, optional
        The sequence starts with zero, by default True

    Yields
    ------
    Generator[int, None, None]
        A consecutive Fibonacci number.
    """
    fibcur: int = 0 if start_with_zero else 1
    fibnext: int = 1
    while True:
        yield fibcur
        fibcur, fibnext = fibnext, fibcur + fibnext
