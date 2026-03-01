"""The "Quick sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Quicksort
"""

from collections.abc import Callable, Iterable
from operator import gt, lt
from random import randint
from typing import Any

from adspy.algorithms.sorting.misc import validate_key_arg


def _compare(
    left: Any,
    right: Any,
    *,
    key: Callable[[Any], Any],
    cmp: Callable[[Any, Any], bool],
) -> bool:
    return cmp(key(left), key(right))


def _quick_sort(
    lst: list,
    lidx: int,
    ridx: int,
    *,
    key: Callable,
    cmp: Callable,
) -> None:
    """The actual recursive implementation."""
    # special minor cases
    if lidx >= ridx:
        return
    if (ridx - lidx) == 1:
        if not _compare(lst[lidx], lst[ridx], key=key, cmp=cmp):
            lst[lidx], lst[ridx] = lst[ridx], lst[lidx]
        return  # in order
    # picking a pivot
    pivot = lst[randint(lidx, ridx)]
    # partitioning
    li, ri = lidx, ridx
    while li < ri:
        while (li < ri) and _compare(lst[li], pivot, key=key, cmp=cmp):
            li += 1  # already in order
        while (li < ri) and (not _compare(lst[ri], pivot, key=key, cmp=cmp)):
            ri -= 1  # already in order
        if li != ri:
            lst[li], lst[ri] = lst[ri], lst[li]
    _quick_sort(lst, lidx, ri - 1, key=key, cmp=cmp)
    _quick_sort(lst, ri, ridx, key=key, cmp=cmp)


def quick_sort(
    it: Iterable,
    key: None | Callable = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the sorted list.

    Parameters
    ----------
    it : Iterable
    key : None | Callable, default None
    reverse : bool, default False

    Returns
    -------
    list
    """
    key = validate_key_arg(key)
    lst = list(it)
    if (size := len(lst)) > 1:
        cmp = gt if reverse else lt
        _quick_sort(lst, 0, size - 1, key=key, cmp=cmp)
    return lst
