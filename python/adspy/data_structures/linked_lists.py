"""Linked list data structures."""

from collections.abc import Iterable, Iterator, MutableSequence
from functools import total_ordering
from typing import Any

from typing_extensions import Self

from adspy.algorithms.sorting import merge_sort


class _DoublyLinkedNode:
    """Doubly linked node."""

    __slots__ = ("value", "_prev", "_next")

    def __init__(self, value: Any = None) -> None:
        self.value = value
        self._prev: _DoublyLinkedNode | None = None
        self._next: _DoublyLinkedNode | None = None

    def __eq__(self, value: object) -> bool:
        return bool(self.value == value)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(value={self.value!r})"

    @property
    def prev(self) -> "_DoublyLinkedNode | None":
        return self._prev

    @prev.setter
    def prev(self, node: "_DoublyLinkedNode | None") -> None:
        self._prev = node if isinstance(node, _DoublyLinkedNode) else None

    @property
    def next(self) -> "_DoublyLinkedNode | None":
        return self._next

    @next.setter
    def next(self, node: "_DoublyLinkedNode | None") -> None:
        self._next = node if isinstance(node, _DoublyLinkedNode) else None


# Linked lists


class LinkedListError(Exception): ...


@total_ordering
class DoublyLinkedList(MutableSequence):
    """Doubly Linked List."""

    __slots__ = ("_head", "_tail", "_length")

    @classmethod
    def from_iterable(cls, it: Iterable) -> Self:
        """Return a "(Doubly) Linked List" instance from the `it`erable."""

        return cls(it)

    def __init__(self, it: None | Iterable = None) -> None:
        self._head: _DoublyLinkedNode | None = None
        self._tail: _DoublyLinkedNode | None = None
        self._length: int = 0

        # Well, it's kinda unfair to use Python lists here :)
        self.extend(it or ())

    def __add__(self, other: Iterable) -> Self:
        dlist = self.__copy__()
        dlist += other
        return dlist

    def __bool__(self) -> bool:
        return bool(len(self))

    def __contains__(self, value: Any) -> bool:
        return value in tuple(self)

    def __copy__(self) -> Self:
        return type(self)(self)

    def _get_normalised_index(self, index: int) -> int:
        idx = index if index > -1 else len(self) + index
        return 0 if idx < 0 else idx

    def _get_indices(self, key: int | slice) -> tuple[int, ...]:
        if isinstance(key, int):
            key = self._get_normalised_index(index=key)
            key = slice(key, key + 1, 1)
        return tuple(range(key.start, key.stop, key.step))

    def _check_indices(self, key: int | slice) -> tuple[int, ...]:
        indices = tuple(self._get_indices(key))
        if isinstance(key, int) and (len(indices) > len(self)):
            msg = f"bad key {key!r}"
            raise IndexError(msg)
        return indices

    def __delitem__(self, key: int | slice) -> None:
        indices = self._check_indices(key=key)
        for idx, node in enumerate(self._yield_nodes()):
            if idx not in indices:
                continue
            self._detach(node)

    def __getitem__(self, key: int | slice) -> Any:
        lst = type(self)()
        indices = set(self._check_indices(key=key))
        for idx, node in enumerate(self._yield_nodes()):
            if idx not in indices:
                continue
            lst.append(node)
        return lst

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __iadd__(self, other: Iterable) -> Self:
        self.extend(other)
        return self

    def __imul__(self, nbr: int) -> Self:
        items = tuple(self)
        self.clear()
        for _ in range(nbr):
            self.extend(items)
        return self

    def _yield_nodes(self) -> Iterator[_DoublyLinkedNode]:
        node = self._head
        while node:
            yield node
            node = node.next

    def __iter__(self) -> Iterator:
        for node in self._yield_nodes():
            yield node.value

    def __len__(self) -> int:
        return self._length

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) < tuple(other)
        return NotImplemented

    def __mul__(self, nbr: int) -> Self:
        dlist = self.__copy__()
        dlist *= nbr
        return dlist

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        it = tuple(self)
        return f"{cls_name}(it={it})"

    def __reversed__(self) -> Iterator:
        tail = self._tail
        while tail:
            yield tail.value
            tail = tail.prev

    def __setitem__(self, key: int | slice, value: Any) -> None:
        indices = self._check_indices(key=key)

        if isinstance(key, slice):
            value = tuple(value)  # raises TypeError

        # relies on ordered dictionaries
        values = (value,) if isinstance(key, int) else value
        idx_values = dict(zip(indices, values, strict=False))
        del indices
        del values

        for idx, node in enumerate(self._yield_nodes()):
            if idx not in idx_values:
                continue
            node.value = idx_values.pop(idx)

        if isinstance(key, slice):
            for idx in tuple(idx_values.keys()):
                self.append(idx_values.pop(idx))

    def append(self, value: Any) -> None:
        """Append (add at the end) a value."""

        node = _DoublyLinkedNode(value)
        if self._tail is None:
            self._tail = node
            self._head = node
        else:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node
        self._length += 1

    def _detach(self, node: None | _DoublyLinkedNode) -> None:
        if node is None:
            return

        ante: None | _DoublyLinkedNode = node.prev
        post: None | _DoublyLinkedNode = node.next

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

    def extend(self, it: Iterable) -> None:
        """Append the items from the `it`erable."""

        for item in it:
            self.append(item)

    def insert(self, index: int, value: Any) -> None:
        """Insert a value in the list at the `index`."""

        pidx = self._get_normalised_index(index)

        if not pidx:
            self.prepend(value)
            return
        if pidx < 0:
            self.append(value)
            return

        new_node = _DoublyLinkedNode(value=value)
        for idx, node in enumerate(self._yield_nodes()):
            if idx == pidx:
                # mypy treats the `prev_node` value of type None | Node
                if prev_node := node.prev:
                    prev_node.next = new_node
                new_node.prev = prev_node

                new_node.next = node
                node.prev = new_node

                self._length += 1
                break

    def remove(self, value: Any) -> None:
        """Remove the first occurence of the value."""

        for node in self._yield_nodes():
            if node.value == value:
                self._detach(node)
                break

    def pop(self, index: int = -1) -> Any:
        """Remove the node with the `index`."""

        nonneg_idx = self._get_normalised_index(index=index)

        for idx, node in enumerate(self._yield_nodes()):
            if idx == nonneg_idx:
                value = node.value
                self._detach(node)
                return value

        msg = f"bad index={index}"
        raise IndexError(msg)

    def prepend(self, value: Any) -> None:
        """Prepend (add at the beginning) a value."""

        node = _DoublyLinkedNode(value)
        if self._head is None:
            self._tail = node
            self._head = node
        else:
            self._head.prev = node
            node.next = self._head
            self._head = node
        self._length += 1

    def sort(self) -> None:
        items = merge_sort(tuple(self))
        self.clear()
        self.extend(items)
