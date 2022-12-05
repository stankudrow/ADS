#!/usr/bin/env python3
"""Summing the elements of a sequence."""


def sum_recursive(seq):
    """sum_recursive

    Parameters
    ----------
    seq : with __add__ protocol.

    Returns
    -------
    reversed sequence with __add__ protocol.
    """

    def _sumrec(seq_, index: int, length: int):
        """The recursive implementation."""
        if index < length:
            return seq_[index] + _sumrec(seq_, index + 1, length)
        return 0

    return _sumrec(seq, 0, len(seq))


def sum_iterative(seq):
    """sum_iterative

    Parameters
    ----------
    seq : with __add__ protocol.

    Returns
    -------
    reversed sequence with __add__ protocol.
    """
    summa: int = 0
    for elem in seq:
        summa += elem
    return summa
