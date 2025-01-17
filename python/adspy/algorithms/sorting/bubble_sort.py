"""The "Bubble sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Bubble_sort
"""

from collections.abc import Callable, Sequence
from typing import Any


def bubble_sort(
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

    def _default_key(arg: Any) -> Any:
        return arg

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

    lst = list(seq)
    size = len(lst)
    while True:
        swapped = False
        for idx in range(1, size):
            if key(lst[idx - 1]) > key(lst[idx]):
                lst[idx - 1], lst[idx] = lst[idx], lst[idx - 1]
                swapped = True
        if not swapped:
            break
        size -= 1
    if reverse:
        lst.reverse()
    return lst
