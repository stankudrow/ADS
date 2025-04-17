"""Linked lists data structures."""

from collections.abc import Iterable, Iterator
from typing import Any


class _LinkedNode:
    """Doubly linked node."""

    __slots__ = ("value", "_prev", "_next")

    def __init__(self, value: Any = None) -> None:
        self.value = value
        self._prev: _LinkedNode | None = None
        self._next: _LinkedNode | None = None

    def __eq__(self, value: object) -> bool:
        return bool(self.value == value)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(value={self.value!r})"

    @property
    def prev(self) -> "_LinkedNode | None":
        return self._prev

    @prev.setter
    def prev(self, node: "_LinkedNode | None") -> None:
        self._prev = node if isinstance(node, _LinkedNode) else None

    @property
    def next(self) -> "_LinkedNode | None":
        return self._next

    @next.setter
    def next(self, node: "_LinkedNode | None") -> None:
        self._next = node if isinstance(node, _LinkedNode) else None


# Linked lists


class LinkedListError(Exception): ...


class LinkedList:
    """Doubly linked list."""

    __slots__ = ("_head", "_tail", "_length")

    @classmethod
    def from_iterable(cls, it: Iterable) -> "LinkedList":
        return cls(it=it)

    def __init__(self, it: None | Iterable = None) -> None:
        self._head: _LinkedNode | None = None
        self._tail: _LinkedNode | None = None
        self._length: int = 0

        # Well, it's kinda unfair to use Python lists here :)
        self.extend(it or ())

    def __getitem__(self, key: int | slice) -> Any:
        # inefficient yet simple and delegative
        result = tuple(self)[key]
        if isinstance(key, slice):
            return type(self).from_iterable(it=result)
        return result

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __iter__(self) -> Iterator[Any]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def __len__(self) -> int:
        return self._length

    def __le__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) <= tuple(other)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) < tuple(other)
        return NotImplemented

    def prepend(self, value: Any) -> None:
        node = _LinkedNode(value)
        if self._head is None:
            self._tail = node
            self._head = node
        else:
            self._head.prev = node
            node.next = self._head
            self._head = node
        self._length += 1

    def append(self, value: Any) -> None:
        node = _LinkedNode(value)
        if self._tail is None:
            self._tail = node
            self._head = node
        else:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node
        self._length += 1

    def extend(self, it: Iterable) -> None:
        for item in it:
            self.append(item)
