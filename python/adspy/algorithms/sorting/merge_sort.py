"""The "Merge sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Merge_sort
"""

from collections.abc import Callable, Sequence

from adspy.algorithms.sorting.common import merge, validate_key_arg


def _merge_sort(
    lst: list,
    key: Callable | None = None,
    *,
    reverse: bool = False,
) -> list:
    """The actual recursive implementation."""

    if (size := len(lst)) < 2:
        return lst
    mid = size // 2
    left_half = _merge_sort(lst[:mid], key, reverse=reverse)
    right_half = _merge_sort(lst[mid:], key, reverse=reverse)
    return merge(left_half, right_half, key, reverse=reverse)


def merge_sort(
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
    if len(lst) > 1:
        lst = _merge_sort(lst, key=key, reverse=reverse)
    return lst
