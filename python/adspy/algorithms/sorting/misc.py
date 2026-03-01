from collections.abc import Callable, Iterable
from operator import ge, le
from typing import Any, cast


def validate_key_arg(key: Any) -> Callable:
    if key is None:
        return lambda x: x
    if callable(key):
        return cast("Callable", key)
    msg = f"{key} is not callable"
    raise TypeError(msg)


def merge(
    it1: Iterable,
    it2: Iterable,
    key: None | Callable = None,
    *,
    desc: bool = False,
) -> list:
    """Returns the merged list from two sequences.

    Parameters
    ----------
    it1 : Iterable
    it2 : Iterable
    key : None | Callable, default None
    desc : bool, default False

    Returns
    -------
    list
    """
    key = validate_key_arg(key)
    op = ge if desc else le

    merged = []
    seq1, seq2 = map(list, (it1, it2))
    i, j = 0, 0
    while i < len(seq1) and j < len(seq2):
        item1, item2 = seq1[i], seq2[j]
        if op(key(item1), key(item2)):
            merged.append(item1)
            i += 1
        else:
            merged.append(item2)
            j += 1
    # seq1 or seq2 (or both) is (are) empty
    merged += seq1[i:]
    merged += seq2[j:]
    return merged
