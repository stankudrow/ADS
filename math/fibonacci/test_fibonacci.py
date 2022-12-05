#!/usr/bin/env python3
"""Fibonacci sequence problem."""


from pytest import mark, param

from fibonacci import (
    fibonacci_recursive,
    fibonacci_iterative,
    fibonacci_generator_iterative,
)


@mark.parametrize(
    "nth_nbr, result",
    [
        param(0, ValueError, marks=mark.xfail(reason="nbr < 1")),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
    ],
)
def test_nth_fibonacci(nth_nbr: int, result: int):
    """test_nth_fibonacci

    Parameters
    ----------
    nth_nbr : int
        The nth Fibonacci number to compute.
    result : int

    Raises
    ------
    ValueError
        if nth_nbr < 1.
    """
    # TODO: how to check raise ValueError for both
    # is there any may_raise flag or smth like that?
    assert (
        fibonacci_recursive(nth_nbr)
        == fibonacci_iterative(nth_nbr)
        == result
    )


@mark.parametrize(
    "how_many, zero_start, result",
    [
        (0, False, []),
        (1, False, [1]),
        (1, True, [0]),
        (5, False, [1, 1, 2, 3, 5]),
        (5, True, [0, 1, 1, 2, 3]),
    ],
)
def test_fibonacci_generator(
    how_many: int, zero_start: bool, result: list[int]
):
    """test_fibonacci_generator

    Parameters
    ----------
    how_many : int
        the number of elements to emit.
    zero_start : bool
        start the sequence with 0
    result : list[int]
        after how many_times.
    """
    fibitergen = fibonacci_generator_iterative(
        start_with_zero=zero_start
    )
    iterseq = [next(fibitergen) for _ in range(how_many)]
    assert iterseq == result
