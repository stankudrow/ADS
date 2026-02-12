"""The "Selection sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Selection_sort
"""

from collections.abc import Callable, Iterable
from operator import gt, lt

from adspy.algorithms.sorting.common import validate_key_arg


def selection_sort(
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

    seq = list(it)
    size = len(seq)  # O(1)
    op = lt if reverse else gt

    for i in range(size):
        imin = i
        for j in range(i + 1, size):
            if op(key(seq[imin]), key(seq[j])):
                imin = j
        seq[i], seq[imin] = seq[imin], seq[i]
    return seq
