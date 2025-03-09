"""Linked lists data structures."""

from typing import Any


class LinkedNode:
    def __init__(self, value: Any = None) -> None:
        self.value = value

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(value={self.value})"


class SinglyLinkedNode(LinkedNode):
    __slots__ = ("value", "_next")

    def __init__(self, value: Any = None) -> None:
        super().__init__(value=value)
        self._next: SinglyLinkedNode | None = None

    @property
    def next(self) -> "SinglyLinkedNode | None":
        return self._next

    @next.setter
    def next(self, node: "SinglyLinkedNode | None") -> None:
        self._next = node if node is None else SinglyLinkedNode(value=node)


class DoublyLinkedNode(LinkedNode):
    __slots__ = ("value", "_prev", "_next")

    def __init__(self, value: Any = None) -> None:
        super().__init__(value=value)
        self._prev: DoublyLinkedNode | None = None
        self._next: DoublyLinkedNode | None = None

    @property
    def prev(self) -> "DoublyLinkedNode | None":
        return self._prev

    @prev.setter
    def prev(self, node: "DoublyLinkedNode | None") -> None:
        self._prev = node if node is None else DoublyLinkedNode(value=node)

    @property
    def next(self) -> "DoublyLinkedNode | None":
        return self._next

    @next.setter
    def next(self, node: "DoublyLinkedNode | None") -> None:
        self._next = node if node is None else DoublyLinkedNode(value=node)


# Linked lists


class LinkedListError(Exception): ...


class SinglyLinkedList:
    def __init__(self) -> None:
        self._head: SinglyLinkedNode | None = None
        self._tail: SinglyLinkedNode | None = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length
