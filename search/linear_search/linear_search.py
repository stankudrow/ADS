#!/usr/bin/env python3
"""Search linearly an item in a sequence."""


from typing import Any, Sequence


def linsearch_iterative(
    seq: Sequence[Any], item: Any
) -> int | None:
    """linsearch_iterative.

    Parameters
    ----------
    seq : Sequence[Any]
        where to search
    item : Any
        what to search

    Returns
    -------
    int | None
        the index of the item if found else None.
    """
    for index, elem in enumerate(seq):
        if elem == item:
            return index
    return None


def linsearch_recursive(
    seq: Sequence[Any], item: Any
) -> int | None:
    """linsearch_recursive.

    Parameters
    ----------
    seq : Sequence[Any]
        where to search
    item : Any
        what to search

    Returns
    -------
    int | None
        the index of the item if found else None.
    """

    def _linserec(
        seq_: Sequence[Any],
        item_: Any,
        current: int,
        length: int,
    ):
        """The recursive implementation of the linear search algorithm."""
        if current < length:
            if seq_[current] == item_:
                return current
            return _linserec(seq_, item_, current + 1, length)
        return None

    return _linserec(seq, item, 0, len(seq))
