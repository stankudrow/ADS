from collections.abc import Sequence
from operator import ge, gt, le, lt


def is_sorted(
    seq: Sequence, *, reverse: bool = False, strict: bool = False
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
        if not op(tup[idx - 1], tup[idx]):
            return False
    return True
