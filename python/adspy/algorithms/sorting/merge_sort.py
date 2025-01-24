"""The "Merge sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Merge_sort
"""

from collections.abc import Callable, Sequence
from typing import Any

from adspy.algorithms.sorting.common import merge


def _default_key(arg: Any) -> Any:
    return arg


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

    def _merge_sort_rec(
        lst: list,
        key: Callable | None = None,
        *,
        reverse: bool = False,
    ) -> list:
        """The actual recursive implementation."""

        if (size := len(lst)) < 2:
            return lst
        mid = size // 2
        left_half = _merge_sort_rec(lst[:mid], key, reverse=reverse)
        right_half = _merge_sort_rec(lst[mid:], key, reverse=reverse)
        return merge(left_half, right_half, key, reverse=reverse)

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

    lst = list(seq)
    if len(lst) > 1:
        lst = _merge_sort_rec(lst, key=key, reverse=reverse)
    return lst
