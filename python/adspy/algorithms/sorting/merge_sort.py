"""The "Merge sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Merge_sort
"""

from collections.abc import Callable, Iterable

from adspy.algorithms.sorting.misc import merge, validate_key_arg


def _merge_sort(
    lst: list,
    /,
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
    return merge(left_half, right_half, key, desc=reverse)


def merge_sort(
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
    return _merge_sort(list(it), key=key, reverse=reverse)
