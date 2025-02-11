"""Linked nodes for linked lists data structures."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

BaseNodeType = TypeVar("BaseNodeType", bound="BaseLinkedNode")
SingleNodeType = TypeVar("SingleNodeType", bound="SinglyLinkedNode")
DoubleNodeType = TypeVar("DoubleNodeType", bound="DoublyLinkedNode")


class BaseLinkedNode(ABC):
    def __init__(self, value: Any = None) -> None:
        self.value = value

    @property
    @abstractmethod
    def next(self) -> BaseNodeType | None:
        raise NotImplementedError

    @next.setter
    @abstractmethod
    def next(self, node: BaseNodeType | None) -> None:
        raise NotImplementedError


class SinglyLinkedNode(BaseLinkedNode):
    def __init__(self, value: Any = None) -> None:
        super().__init__(value=value)
        self._next: SingleNodeType | None = None

    @property
    def next(self) -> SingleNodeType | None:
        return self._next

    @next.setter
    def next(self, node: SingleNodeType | None) -> None:
        self._next = node if node is None else SinglyLinkedNode(value=node)


class DoublyLinkedNode(BaseLinkedNode):
    def __init__(self, value: Any = None) -> None:
        super().__init__(value=value)
        self._prev: DoubleNodeType | None = None
        self._next: DoubleNodeType | None = None

    @property
    def prev(self) -> DoubleNodeType | None:
        return self._prev

    @prev.setter
    def prev(self, node: DoubleNodeType | None) -> None:
        self._prev = node if node is None else DoublyLinkedNode(value=node)

    @property
    def next(self) -> DoubleNodeType | None:
        return self._next

    @next.setter
    def next(self, node: DoubleNodeType | None) -> None:
        self._next = node if node is None else DoublyLinkedNode(value=node)
