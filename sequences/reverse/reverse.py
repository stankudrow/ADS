#!/usr/bin/env python3
"""Reversing a sequence."""


def reverse_iterative(seq):
    """reverse_iterative

    Parameters
    ----------
    seq : with __add__ protocol.

    Returns
    -------
    reversed sequence with __add__ protocol.
    """
    lind, rind = 0, len(seq) - 1
    copy_seq = list(seq)  # item assignment supported
    while rind - lind > 0:
        copy_seq[lind], copy_seq[rind] = (
            copy_seq[rind],
            copy_seq[lind],
        )
        lind, rind = lind + 1, rind - 1
    if isinstance(seq, str):
        return "".join(copy_seq)
    # type consistency, like when performing [::-1]
    return type(seq)(copy_seq)


def reverse_recursive(seq):
    """reverse_recursive

    Parameters
    ----------
    seq : with __add__ protocol.

    Returns
    -------
    reversed sequence with __add__ protocol.
    """

    def _revseq(seq_, lind: int, rind: int):
        """The recursive implementation."""
        if rind - lind > 0:
            seq_[lind], seq_[rind] = (
                seq_[rind],
                seq_[lind],
            )
            _revseq(seq_, lind + 1, rind - 1)

    copy_seq = list(seq)
    _revseq(copy_seq, 0, len(seq) - 1)
    if isinstance(seq, str):
        return "".join(copy_seq)
    return type(seq)(copy_seq)
