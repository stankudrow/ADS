from collections.abc import Callable, Sequence
from operator import ge, gt, le, lt
from typing import Any, cast


def _default_key(arg: Any) -> Any:
    return arg


def validate_key_arg(key: Any) -> Callable:
    if key is None:
        key = _default_key
    if callable(key):
        return cast(Callable, key)
    msg = f"{key} is not callable"
    raise TypeError(msg)


def is_sorted(
    seq: Sequence,
    key: None | Callable = None,
    *,
    reverse: bool = False,
    strict: bool = False,
) -> bool:
    """Returns True if the `seq` is sorted.

    Parameters
    ----------
    reverse : bool, default False
        True for the ascending order (equal items are acceptable)
    strict: bool, default False
        if True, then checking the strict order (no equality is allowed)

    Returns
    -------
    bool
    """

    key = validate_key_arg(key)

    if reverse:
        op = ge
        if strict:
            op = gt
    else:
        op = le
        if strict:
            op = lt

    tup = tuple(seq)
    for idx in range(1, len(tup)):
        if not op(key(tup[idx - 1]), key(tup[idx])):
            return False
    return True


def merge(
    seq1: Sequence,
    seq2: Sequence,
    key: None | Callable = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the merged list from two sequences.

    Parameters
    ----------
    seq1 : Sequence
    seq2 : Sequence
    key : None | Callable, default None
    reverse : bool, default False

    Returns
    -------
    list
    """

    key = validate_key_arg(key)

    op = gt if reverse else lt

    merged = []
    lst1, lst2 = map(list, (seq1, seq2))
    len1, len2 = map(len, (lst1, lst2))
    idx1, idx2 = 0, 0
    while (idx1 < len1) and (idx2 < len2):
        if op(key(seq1[idx1]), key(seq2[idx2])):
            merged.append(seq1[idx1])
            idx1 += 1
        else:
            merged.append(seq2[idx2])
            idx2 += 1
    merged += seq1[idx1:]
    merged += seq2[idx2:]
    return merged
