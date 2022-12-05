#!/usr/bin/env python3
"""The Flood Fill algorithm."""


# Filling an arbitrary shaped area of the same value/colour with another value/colour.
# Filling is being done until the borders of either area or screen are met.
#
# The Origin point is at the top left corner.
# The X-axis of the screen goes from the left to the right.
# The Y-axis of the screen goes from the top to the bottom.
# Also, the order of addressing (__getitem__) nested sequences.
# These details infer to the reason why x and y coordinates are swapped. 
#
# References
#   * he Recursive Book of Recursion - Al Sweigart.


from typing import Any, Sequence


def flood_fill_recursive(
    screen: Sequence[Sequence[Any]],
    ycoord: int,
    xcoord: int,
    new_value: Any,
):
    """flood_fill_recursive _summary_

    _extended_summary_

    Parameters
    ----------
    screen : Sequence[Sequence[Any]]
    ycoord : int
        the y coordinate of the "original" pixel.
    xcoord : int
        the x coordinate of the "original" pixel.
    new_value : str | int
        replaces the value of the "original" pixel.
    """

    def _flood_fill_rec(  # pylint: disable=too-many-arguments
        screen_,
        ylen_,
        xlen_,
        yc,  # pylint: disable=invalid-name
        xc,  # pylint: disable=invalid-name
        oldval,
        newval,
    ):
        if screen_[yc][xc] == oldval:
            screen_[yc][xc] = newval
            if (yc + 1 < ylen_) and (
                screen_[yc + 1][xc] == oldval
            ):
                _flood_fill_rec(
                    screen_,
                    ylen_,
                    xlen_,
                    yc + 1,
                    xc,
                    oldval,
                    newval,
                )
            if (xc + 1 < xlen_) and (
                screen_[yc][xc + 1] == oldval
            ):
                _flood_fill_rec(
                    screen_,
                    ylen_,
                    xlen_,
                    yc,
                    xc + 1,
                    oldval,
                    newval,
                )
            if (xc - 1 > -1) and (screen_[yc][xc - 1] == oldval):
                _flood_fill_rec(
                    screen_,
                    ylen_,
                    xlen_,
                    yc,
                    xc - 1,
                    oldval,
                    newval,
                )
            if (yc - 1 > -1) and (screen_[yc - 1][xc] == oldval):
                _flood_fill_rec(
                    screen_,
                    ylen_,
                    xlen_,
                    yc - 1,
                    xc,
                    oldval,
                    newval,
                )
        # useless-return

    if ycoord < 0 or xcoord < 0:
        raise ValueError(
            f"{(ycoord, xcoord)} contains negative values"
        )
    if screen:
        old_value = screen[ycoord][xcoord]
        if old_value != new_value:
            ylen, xlen = len(screen), len(screen[0])
            _flood_fill_rec(
                screen,
                ylen,
                xlen,
                ycoord,
                xcoord,
                old_value,
                new_value,
            )
