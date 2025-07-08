"""The "Quick sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Quicksort
"""

from collections.abc import Callable, Sequence
from operator import gt, lt
from random import randint
from typing import Any

from adspy.algorithms.sorting.common import validate_key_arg


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
    lefter, righter = left, right
    while lefter < righter:
        while (lefter < righter) and _compare(
            lst[lefter], pivot, key=key, cmp=cmp
        ):
            lefter += 1
        while (lefter < righter) and (
            not _compare(lst[righter], pivot, key=key, cmp=cmp)
        ):
            righter -= 1
        if lefter != righter:
            lst[lefter], lst[righter] = lst[righter], lst[lefter]
    _quick_sort(lst, left, righter - 1, key=key, cmp=cmp)
    _quick_sort(lst, righter, right, key=key, cmp=cmp)


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

    key = validate_key_arg(key)

    lst = list(seq)
    if (size := len(lst)) > 1:
        cmp = gt if reverse else lt
        _quick_sort(lst, 0, size - 1, key=key, cmp=cmp)
    return lst
