"""The "Bubble sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Bubble_sort
"""

from collections.abc import Callable, Iterable
from operator import gt, lt

from adspy.algorithms.sorting.common import validate_key_arg


def bubble_sort(
    it: Iterable,
    key: None | Callable = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the sorted list.

    Parameters
    ----------
    seq : Iterable
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

    for _ in range(size):
        swapped = False
        for j in range(1, size):
            if op(key(seq[j - 1]), key(seq[j])):
                seq[j - 1], seq[j] = seq[j], seq[j - 1]
                swapped = True
        if not swapped:
            break
        size -= 1
    return seq
