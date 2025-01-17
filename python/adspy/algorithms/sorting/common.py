from collections.abc import Callable, Sequence
from operator import ge, gt, le, lt
from typing import Any


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

    def _default_key(arg: Any) -> Any:
        return arg

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

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
