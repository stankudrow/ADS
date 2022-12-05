#!/usr/bin/env python3
"""Palindrom detection problem."""


from typing import Sequence


def is_palindrome_recursive(iterable: Sequence) -> bool:
    """is_palindrome_recursive

    Parameters
    ----------
    iterable : Sequence

    Returns
    -------
    bool
    """
    if len(iterable) < 2:
        return True
    if iterable[0] != iterable[-1]:
        return False
    return is_palindrome_recursive(iterable[1:-1])


def is_palindrome_iterative(iterable: Sequence) -> bool:
    """is_palindrome_iterative

    Parameters
    ----------
    iterable : Sequence

    Returns
    -------
    bool
    """
    length: int = len(iterable)
    if length < 2:
        return True
    for index in range(length // 2):
        if iterable[index] != iterable[-(index + 1)]:
            return False
    return True
