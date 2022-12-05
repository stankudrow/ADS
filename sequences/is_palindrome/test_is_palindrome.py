#!/usr/bin/env python3
"""Palindrom detection problem."""


from typing import Sequence

from pytest import mark

from is_palindrome import is_palindrome_iterative
from is_palindrome import is_palindrome_recursive


@mark.parametrize(
    "iterable, result",
    [
        ("", True),
        ("1", True),
        ("11", True),
        ("121", True),
        ("32123", True),
        ("12", False),
        ("1234", False),
    ],
)
def test_is_palindrome(iterable: Sequence, result: bool):
    """test_is_palindrome.

    Parameters
    ----------
    iterable : Sequence
    """
    assert (
        is_palindrome_recursive(iterable)
        == is_palindrome_iterative(iterable)
        == result
    )
