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
        """Return a "(Doubly) Linked List" instance from the `it`erable."""

        return cls(it=it)

    def __init__(self, it: None | Iterable = None) -> None:
        self._head: _LinkedNode | None = None
        self._tail: _LinkedNode | None = None
        self._length: int = 0

        # Well, it's kinda unfair to use Python lists here :)
        self.extend(it or ())

    def __bool__(self) -> bool:
        return bool(len(self))

    def __getitem__(self, key: int | slice) -> Any:
        # inefficient yet simple and delegative
        result = tuple(self)[key]
        if isinstance(key, slice):
            return type(self).from_iterable(it=result)
        return result

    def __delitem__(self, key: int | slice) -> None:
        seq = tuple(self)

        deletable = seq[key]
        if isinstance(key, int):
            deletable = (deletable,)

        self.clear()
        self.extend(it=tuple(item for item in seq if item not in deletable))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) <= tuple(other)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) < tuple(other)
        return NotImplemented

    def _yield_nodes(self) -> Iterator[_LinkedNode]:
        node = self._head
        while node:
            yield node
            node = node.next

    def __iter__(self) -> Iterator[Any]:
        for node in self._yield_nodes():
            yield node.value

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        it = tuple(self)
        return f"{cls_name}(it={it})"

    def prepend(self, value: Any) -> None:
        """Prepend (add at the beginning) a value."""

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
        """Append (add at the end) a value."""

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
        """Append the items from the `it`erable."""

        if not (items := tuple(it)):
            return

        length = len(items)
        itemator = iter(items)

        head = _LinkedNode(value=next(itemator))
        cur = head
        for item in itemator:
            node = _LinkedNode(value=item)
            cur.next = node
            node.prev = cur
            cur = node

        if self._tail is None:
            self._head = head
        self._tail = cur
        self._length += length

    def _detach(self, node: None | _LinkedNode) -> None:
        if node is None:
            return

        ante: None | _LinkedNode = node.prev
        post: None | _LinkedNode = node.next

        if ante:
            ante.next = post
        else:
            self._head = post

        if post:
            post.prev = ante
        else:
            self._tail = ante

        self._length -= 1
        del node

    def clear(self) -> None:
        """Remove all elements from the list."""

        for node in self._yield_nodes():
            self._detach(node)

    def remove(self, value: Any) -> None:
        """Remove the first occurence of the value."""

        for node in self._yield_nodes():
            if node.value == value:
                self._detach(node)
                break

    def pop(self, index: int = -1) -> Any:
        """Removes the node with the `index`."""

        nonneg_idx = index if index > -1 else (len(self) + index)

        for idx, node in enumerate(self._yield_nodes()):
            if idx == nonneg_idx:
                value = node.value
                self._detach(node)
                return value

        msg = f"bad index={index}"
        raise IndexError(msg)
