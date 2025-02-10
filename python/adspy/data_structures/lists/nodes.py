"""Linked nodes for linked lists data structures."""

from typing import Any, TypeVar

SingleNodeType = TypeVar("SingleNodeType", bound="SinglyLinkedNode")
DoubleNodeType = TypeVar("DoubleNodeType", bound="DoublyLinkedNode")


class SinglyLinkedNode:
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.next = None

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    @property
    def next(self) -> None | SingleNodeType:
        return self._next

    @next.setter
    def next(self, node: None | SingleNodeType) -> None:
        self._next = node


class DoublyLinkedNode:
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self._prev = None
        self._next = None

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    @property
    def prev(self) -> None | DoubleNodeType:
        return self._prev

    @prev.setter
    def prev(self, node: None | DoubleNodeType) -> None:
        self._prev = node

    @property
    def next(self) -> None | DoubleNodeType:
        return self._next

    @next.setter
    def next(self, node: None | DoubleNodeType) -> None:
        self._next = node
