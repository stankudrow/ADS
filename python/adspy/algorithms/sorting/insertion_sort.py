"""The "Insertion sort" algorithm.

References
----------
- https://en.wikipedia.org/wiki/Insertion_sort
"""

from collections.abc import Callable, Iterable
from operator import gt, lt

from adspy.algorithms.sorting.misc import validate_key_arg


def insertion_sort(
    it: Iterable,
    /,
    key: Callable | None = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the sorted list.

    Parameters
    ----------
    it: Iterable
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

    for i in range(1, size):
        current = seq[i]
        j = i - 1
        while j > -1 and op(key(seq[j]), key(current)):
            seq[j + 1] = seq[j]
            j -= 1
        seq[j + 1] = current
    return seq
