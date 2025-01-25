"""The "Quick sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Quicksort
"""

from collections.abc import Callable, Sequence
from operator import gt, lt
from random import randint
from typing import Any


def _default_key(arg: Any) -> Any:
    return arg


def _compare(left: Any, right: Any, *, key=Callable, cmp: Callable) -> bool:
    return cmp(key(left), key(right))


def _quick_sort(
    lst: list,
    left: int,
    right: int,
    *,
    key: Callable,
    cmp: Callable,
) -> None:
    """The actual recursive implementation."""

    # special minor cases
    if left >= right:
        return
    if (right - left) == 1:
        if not _compare(lst[left], lst[right], key=key, cmp=cmp):
            lst[left], lst[right] = lst[right], lst[left]
        return

    # picking a pivot
    pidx = randint(left, right)
    pivot = lst[pidx]
    # partitioning
    l, r = left, right
    while l < r:
        while (l < r) and _compare(lst[l], pivot, key=key, cmp=cmp):
            l += 1
        while (l < r) and (not _compare(lst[r], pivot, key=key, cmp=cmp)):
            r -= 1
        if l != r:
            lst[l], lst[r] = lst[r], lst[l]
    _quick_sort(lst, left, r - 1, key=key, cmp=cmp)
    _quick_sort(lst, r, right, key=key, cmp=cmp)


def quick_sort(
    seq: Sequence,
    key: None | Callable = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the sorted list.

    Parameters
    ----------
    seq : Sequence
    key : None | Callable, default None
    reverse : bool, default False

    Returns
    -------
    list
    """

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

    lst = list(seq)
    if (size := len(lst)) > 1:
        cmp = gt if reverse else lt
        _quick_sort(lst, 0, size - 1, key=key, cmp=cmp)
    return lst
