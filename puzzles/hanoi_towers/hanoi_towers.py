#!/usr/bin/env python3
"""The Towers of Hanoi problem."""


from functools import wraps


# Input:
#   * the source (src) rod with N items/disks;
#   * the target/destination (dst) rod to move the disks/items onto;
#   * the auxiliary/temporary (tmp) rod as a helper peg.
#
# The sequence is read from the left (bottom) to the right (top)
# and the disks/items are enumerated in the above order from N to 1.
#
# The idea of the algorithm is as follows:
#   * move N - 1 disks from the source rod to the auxiliary one;
#   * move the remaining item/disk from the source to the dest;
#   * move the remaining N - 1 disks from `tmp` to `dst` - a subtask.
#
# Please address the References section below before a leap of faith.
#
# References:
#   * https://www.youtube.com/watch?v=GaC1Dzpafhk - the demonstration.
#   * https://www.youtube.com/watch?v=boS4N1_TLBk - the proof of 2^N - 1.
#   * https://www.youtube.com/watch?v=MbonokcLbNo - Mathologer explains.
#   * Book: Classic Computer Science Problems in Python - David Kopec.


class HanoiError(Exception):
    """The Hanoi Towers Exception."""


def hanoi_recursive(source: list, auxiliary: list, target: list):
    """hanoi_recursive

    Parameters
    ----------
    source : list
            the source (src) rod.
    auxiliary : list
            the temporary (tmp) rod.
    target : list
            the destination (dst) rod.

    Raises
    ------
        HanoiError: if auxiliary and target rods are not empty.
    """

    @wraps(hanoi_recursive)
    def _hanoi(src: list, tmp: list, dst: list, items: int):
        if items == 1:
            dst.append(src.pop())
        else:
            # all items/disks are moved from source to the temporary rod.
            _hanoi(src, dst, tmp, items - 1)
            # moving the remaining items/disk to the target/destination rod.
            _hanoi(src, tmp, dst, 1)
            # move the remaining items/disks from the tmp to the dst rod.
            _hanoi(tmp, src, dst, items - 1)

    if auxiliary or target:
        raise HanoiError(
            "Bad setup: "
            f"source = {source}, "
            f"auxiliary = {auxiliary}, ",
            f"target = {target}.",
        )
    if len(source):
        _hanoi(source, auxiliary, target, len(source))
