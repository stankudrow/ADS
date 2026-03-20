"""The "Heap sort" algorithm.

References
----------
- https://en.wikipedia.org/wiki/Heapsort
"""

from collections.abc import Callable, Iterable

from adspy.algorithms.sorting.misc import validate_key_arg
from adspy.data_structures import Heap


def heap_sort(
    it: Iterable,
    /,
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

    seq = [(key(item), item) for item in it]
    heap = Heap(seq, is_max=reverse)
    return [heap.pop()[-1] for _ in range(len(heap))]
