"""Queue data structures."""

from collections.abc import Iterable, Iterator, MutableSequence
from functools import total_ordering
from sys import maxsize as MAX_INT
from typing import Any

from typing_extensions import Self

from adspy.data_structures.linked_lists import DoublyLinkedList


# Python `deque` does not inherit from MutableSequence
@total_ordering
class Deque:
    """Double-Ended Queue.

    Pronounced as "deck".
    """

    __slots__ = ("_lst", "_maxlen")

    def __init__(
        self, it: None | Iterable = None, maxlen: None | int = None
    ) -> None:
        if maxlen and maxlen < 0:
            msg = f"maxen={maxlen} nust be non-negative"
            raise ValueError(msg)
        self._maxlen = -1 if maxlen is None else maxlen

        self._lst = DoublyLinkedList()
        if it:
            self.extend(it)

    @property
    def maxlen(self) -> int:
        """Return the maxlen attribute value."""
        return self._maxlen

    def __add__(self, other: Iterable) -> Self:
        return type(self)(self._lst + other)

    def __bool__(self) -> bool:
        return bool(self._lst)

    def __contains__(self, value: Any) -> bool:
        return value in self._lst

    def __copy__(self) -> Self:
        return self.copy()

    def __delitem__(self, key: int | slice) -> None:
        del self._lst[key]

    def __getitem__(self, key: int | slice) -> Any:
        return type(self)(self._lst[key])

    def __eq__(self, other: object) -> bool:
        return self._lst == other

    def __iadd__(self, other: Iterable) -> Self:
        self.extend(other)
        return self

    def __imul__(self, nbr: int) -> Self:
        items = tuple(self)
        self.clear()
        for _ in range(nbr):
            self.extend(items)
        return self

    def __iter__(self) -> Iterator[Any]:
        yield from self._lst

    def __len__(self) -> int:
        return len(self._lst)

    def __lt__(self, other: object) -> bool:
        return self._lst < other

    def __mul__(self, nbr: int) -> Self:
        return type(self)(self._lst * nbr)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        it = tuple(self)
        return f"{cls_name}({it})"

    def __reversed__(self) -> Iterator:
        yield from reversed(self._lst)

    def __setitem__(self, key: int | slice, value: Any) -> None:
        self._lst[key] = value

    def append(self, value: Any, /) -> None:
        """Append the value."""
        if not self.maxlen:
            return
        if len(self) == self.maxlen:
            self.popleft()
        self._lst.append(value)

    def appendleft(self, value: Any, /) -> None:
        """Prepend the value."""
        if not self.maxlen:
            return
        if len(self) == self.maxlen:
            self.pop()
        self._lst.prepend(value)

    def clear(self) -> None:
        """Remove all elements."""
        self._lst.clear()

    def copy(self) -> Self:
        """Return the copy of the deque."""
        return type(self)(self)

    def count(self, value: Any, /) -> int:
        """Return the number of occurrences of the value."""
        return self._lst.count(value)

    def extend(self, it: Iterable, /) -> None:
        """Append the items from the `it`erable."""
        # not optimal, but efficient
        for item in it:
            self.append(item)

    def extendleft(self, it: Iterable, /) -> None:
        """Prepend the items from the `it`erable."""
        # not optimal, but efficient
        for item in it:
            self.appendleft(item)

    def index(self, value: Any, start: int = 0, stop: int = MAX_INT) -> int:
        """Return the index of the first occurrence of the value.

        The start parametre (default 0) marks the start index.

        Raises
        ------
        ValueError
            if the value is not present
        """
        return self._lst.index(value, start, stop)

    def insert(self, index: int, value: Any, /) -> None:
        """Insert a value in the list at the given index.

        Parameters
        ----------
        index : int
        value : Any

        Returns
        -------
        None
        """
        if len(self) >= self.maxlen > -1:
            msg = "deque already at its maximum size"
            raise IndexError(msg)
        self._lst.insert(index, value)

    def pop(self) -> Any:
        """Return with removal the rightmost value."""
        return self._lst.popright()

    def popleft(self) -> Any:
        """Return with removal the leftmost value."""
        return self._lst.popleft()

    def remove(self, value: Any, /) -> None:
        """Remove the first occurence of the value."""
        self._lst.remove(value)

    def reverse(self) -> None:
        """Reverse in place."""
        self._lst.reverse()

    def rotate(self, n: int = 1) -> None:
        """Rotate `n` steps.

        If n is positive, rotate to the right.
        Otherwise, to the left.

        Parameters
        ----------
        n : int
            the number of steps for rotation.

        Returns
        -------
        None
        """


MutableSequence.register(Deque)
