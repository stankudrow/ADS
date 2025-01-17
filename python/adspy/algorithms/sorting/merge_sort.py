"""The "Merge sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Merge_sort
"""

from collections.abc import Callable, Sequence

from adspy.algorithms.sorting.common import merge


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

        size = len(lst)
        if size < 2:
            return lst
        mid = size // 2
        left_half = _merge_sort_rec(lst[:mid], key, reverse=reverse)
        right_half = _merge_sort_rec(lst[mid:], key, reverse=reverse)
        return merge(left_half, right_half, key, reverse=reverse)

    sorted_lst = _merge_sort_rec(list(seq), key=key, reverse=False)
    if reverse:
        sorted_lst.reverse()
    return sorted_lst
