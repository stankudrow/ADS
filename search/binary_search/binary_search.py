#!/usr/bin/env python3
"""Search binarily an item in a sorted sequence."""


from typing import Any, Sequence


def binsearch_iterative(
    seq: Sequence[Any], item: Any
) -> int | None:
    """binsearch_iterative.

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
    lind, rind = 0, len(seq) - 1
    while lind <= rind:
        mind = (lind + rind) // 2  # the integer division
        midelem = seq[mind]
        if midelem == item:
            return mind
        elif midelem < item:
            lind = mind + 1
        else:
            rind = mind - 1
    return None


def binsearch_recursive(
    seq: Sequence[Any], item: Any
) -> int | None:
    def _binserec(
        seq_: Sequence[Any], item_: Any, lind: int, rind: int
    ):
        """The recursive implementation of the binary search algorithm."""
        if lind <= rind:
            mind = (lind + rind) // 2
            midelem = seq_[mind]
            if midelem == item_:
                return mind
            elif midelem < item_:
                return _binserec(seq_, item_, mind + 1, rind)
            else:
                return _binserec(seq_, item_, lind, mind - 1)
        return None

    return _binserec(seq, item, 0, len(seq) - 1)
