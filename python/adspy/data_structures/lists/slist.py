"""Singly linked list data structure.

References
----------
- https://en.wikipedia.org/wiki/Linked_list
"""

from array import array
from collections import OrderedDict
from collections.abc import Callable, Iterable, Iterator, MutableSequence
from functools import total_ordering
from sys import maxsize as MAX_INT
from typing import Any

from typing_extensions import Self

from adspy.algorithms.sorting.merge_sort import merge_sort


class _SinglyLinkedNode:
    """Singly linked node."""

    __slots__ = ("value", "_next")

    def __init__(self, value: Any = None, /) -> None:
        self.value = value
        self._next: _SinglyLinkedNode | None = None

    def __hash__(self) -> int:
        return hash((self.value, id(self._next)))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _SinglyLinkedNode):
            return self.value == other.value and self._next is other._next
        return NotImplemented

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self.value!r})"

    @property
    def next(self) -> "_SinglyLinkedNode | None":
        return self._next

    @next.setter
    def next(self, node: "_SinglyLinkedNode | None", /) -> None:
        self._next = node if isinstance(node, _SinglyLinkedNode) else None


# Node utils


def _delete_node(node: None | _SinglyLinkedNode) -> Any:
    if not node:
        return None
    value = node.value
    node.next = None
    del node
    return value


# Linked lists


class SinglyLinkedListError(Exception):
    """Generic Singly Linked List Error."""


@total_ordering
class SinglyLinkedList(MutableSequence):
    """Singly Linked List."""

    __slots__ = ("_head", "_length")

    def __init__(self, it: None | Iterable = None, /) -> None:
        self._head: _SinglyLinkedNode | None = None
        # If you see the implementation,
        # you may understand why self._tail is pointless,
        # yet it is useful for DoublyLinkedList(s)
        # self._tail: _SinglyLinkedNode | None = None  # noqa: ERA001
        self._length: int = 0

        # Well, it's kinda unfair to use Python lists here :)
        self.extend(it or ())

    def __add__(self, other: Iterable) -> Self:
        slist = self.copy()
        slist += other
        return slist

    def __bool__(self) -> bool:
        return bool(len(self))

    def __contains__(self, value: Any) -> bool:
        return any(node == value for node in self)

    def __copy__(self) -> Self:
        return self.copy()

    def __delitem__(self, key: int | slice) -> None:
        indices = self._get_index_range(key)
        try:
            index_offset = 0
            for idx in indices:
                self.pop(idx - index_offset)
                index_offset += 1  # noqa: SIM113
        except IndexError:
            pass

    def __getitem__(self, key: int | slice) -> Any:
        indices = self._get_index_range(key)
        slist = self._get_empty_list()
        if not indices:
            return slist

        index_item_map = OrderedDict.fromkeys(indices)
        for idx, node in enumerate(self._yield_nodes()):
            if idx not in indices:
                continue
            indices.remove(idx)
            index_item_map[idx] = node.value
            if not indices:
                break

        slist.extend(val for val in index_item_map.values() if val is not None)
        if isinstance(key, int):
            return next(iter(slist))
        return slist

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __iadd__(self, other: Iterable) -> Self:
        self.extend(other)
        return self

    def __imul__(self, nbr: int) -> Self:
        rng = range(nbr)
        items = tuple(self)
        self.clear()
        for _ in rng:
            self.extend(items)
        return self

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
        slist = self.copy()
        slist *= nbr
        return slist

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        it = list(self)
        return f"{cls_name}({it})"

    def __reversed__(self) -> Iterator:
        revlist = self._get_empty_list()
        for value in self:
            revlist.prepend(value)
        for value in revlist:
            yield value

    def __setitem__(self, key: int | slice, value: Any) -> None:
        if isinstance(key, slice):
            value = tuple(value)  # may raise TypeError
        values = (value,) if isinstance(key, int) else value
        indices = self._get_index_range(key)
        if (ilen := len(indices)) and ilen < (vlen := len(values)):
            msg = (
                f"attempt to assign sequence of size {ilen} "
                f"to extended slice of size {vlen}"
            )
            raise ValueError(msg)
        idx_values = OrderedDict(zip(indices, values, strict=False))
        if not indices:
            self.extend(values)
            return

        del indices, values
        iterator = iter(self)
        new_list = self._get_empty_list()
        for idx, value in enumerate(iterator):
            new_list.append(
                value if idx not in idx_values else idx_values.pop(idx)
            )

        if isinstance(key, slice):
            new_list.extend(idx_values.values())
        del idx_values
        new_list.extend(iterator)
        self.clear()
        self.extend(new_list)

    def __str__(self) -> str:
        return str(list(self))

    @property
    def _pretail(self) -> None | _SinglyLinkedNode:
        pretail_node: None | _SinglyLinkedNode = None
        for node in self._yield_nodes():
            if node.next:
                pretail_node = node
        return pretail_node

    @property
    def _tail(self) -> None | _SinglyLinkedNode:
        if pretail := self._pretail:
            return pretail.next
        return self._head

    def _detach_next(self, node: None | _SinglyLinkedNode) -> Any:
        if not node:
            return None
        node_to_detach = node.next
        next_node_to_link = None
        if node_to_detach:
            next_node_to_link = node_to_detach.next
        node.next = next_node_to_link
        self._length -= 1
        return _delete_node(node_to_detach)

    def _get_empty_list(self) -> Self:
        return type(self)()

    def _get_index_range(self, key: int | slice) -> array:
        if isinstance(key, int):
            return array("Q", (self._validate_index(key),))

        lstsiz = len(self)
        if (step := key.step) is None:
            step = 1
        if (start := key.start) is None:
            start = 0
        if (stop := key.stop) is None:
            stop = lstsiz

        start = self._normalise_index(start)
        if start >= lstsiz and step < 0:
            start = self._validate_index(lstsiz - 1)
        if start < 0 and step > 0:
            start = 0

        stop = self._normalise_index(stop)
        if stop < 0 and step < 0:
            stop = -1  # to include 0 in range for stop field
        if stop > lstsiz and step < 0:
            stop = lstsiz

        return array("Q", range(start, stop, step))

    def _normalise_index(self, idx: int) -> int:
        if idx < 0:
            idx = len(self) + idx
        return idx

    def _validate_index(self, idx: int) -> int:
        nidx = self._normalise_index(idx)
        if not (-1 < nidx < len(self)):
            msg = f"index {idx!r} is out of range"
            raise IndexError(msg)
        return nidx

    def _yield_nodes(self) -> Iterator[_SinglyLinkedNode]:
        """Yield list nodes sequentially.

        Yields
        ------
        _SinglyLinkedNode
        """
        node = self._head
        while node:
            yield node
            node = node.next

    def append(self, value: Any) -> None:
        """Append (add to the end) the value.

        Parameters
        ----------
        value : Any

        Returns
        -------
        None
        """
        node = _SinglyLinkedNode(value)
        if tail := self._tail:
            tail.next = node
        else:
            self._head = node
        self._length += 1

    def clear(self) -> None:
        """Remove all items from the list.

        This makes the list empty obviously.

        Returns
        -------
        None
        """
        for _ in range(len(self)):
            self.popleft()

    def copy(self) -> Self:
        """Return the copy of the list.

        Returns
        --------
        Self - the copied list
        """
        return type(self)(self)

    def count(self, value: Any) -> int:
        """Return the number of occurrences of the value.

        Parameters
        ----------
        value : Any

        Returns
        -------
        int - counted `value` in the list
        """
        cnt = 0
        for item in self:
            if item == value:
                cnt += 1
        return cnt

    def extend(self, values: Iterable) -> None:
        """Append the items from the `it`erable.

        Parameters
        ----------
        values : Iterable

        Returns
        -------
        None
        """
        for item in values:
            self.append(item)

    def extendleft(self, it: Iterable, /) -> None:
        """Prepend the items from the `it`erable.

        Parameters
        ----------
        it : Iterable

        Returns
        -------
        None
        """
        for item in reversed(tuple(it)):
            self.prepend(item)

    def index(self, value: Any, start: int = 0, stop: int = MAX_INT) -> int:
        """Return the index of the first occurrence of the value.

        Parameters
        ----------
        value : Any
            the `value` which index is to be located
        start : int, default 0
            the index to start searching with
        stop : int, default sys.MAX_INT
            the indext up to which the searching should go

        Raises
        ------
        ValueError
            if start index > stop index
            if the value is not present in the list

        Returns
        -------
        int - the index of the `value`
        """
        istart = self._normalise_index(start)
        istop = self._normalise_index(stop)
        if istart > istop:
            raise ValueError

        it = iter(self)
        # skip the nodes before the start index
        for _ in range(istart):
            try:
                next(it)
            except StopIteration as e:
                msg = f"the list is exhausted before the {istart} index"
                raise ValueError(msg) from e

        for idx, item in enumerate(it, istart):
            if idx >= istop:
                break
            if item == value:
                return idx
        msg = f"no {value} in the list"
        raise ValueError(msg) from None

    def insert(self, index: int, value: Any, /) -> None:
        """Insert a value in the list at the given index.

        Examples
        --------
        slist = SinglyLinkedList()
        slist.insert(0, 42)  # [42]
        slist.insert(-1, 12)  # [12, 42]
        slist.insert(1, 21)  # [12, 21, 42]

        Parameters
        ----------
        index : int
            index at which the `value` must be inserted
        value : Any
            the value to be inserted at the `index`

        Returns
        -------
        None
        """
        nidx = self._normalise_index(index)
        if nidx < 1:
            # will increment the self._length
            self.prepend(value)
            return
        if nidx >= len(self):
            # will increment the self._length
            self.append(value)
            return

        node_iterator = self._yield_nodes()
        prev_node = next(node_iterator)  # == self._head
        new_node = _SinglyLinkedNode(value)
        for idx, node in enumerate(node_iterator, 1):
            if idx == nidx:
                prev_node.next = new_node
                new_node.next = node
                self._length += 1
                break
            prev_node = node

    def pop(self, index: int = -1, /) -> Any:
        """Return with removal the value at the index.

        Parameters
        ----------
        index : int, default -1 - remove the value at this index

        Raises
        ------
        IndexError
            when popping from an empty list.

        Returns
        -------
        Any
            the first/head item of the list
        """
        if index in (-1, len(self) - 1):
            return self.popright()
        if not index:
            return self.popleft()
        normal_idx = self._normalise_index(index)
        for idx, node in enumerate(self._yield_nodes()):
            if (next_idx := idx + 1) == normal_idx:
                if not (next_node := node.next):
                    break
                value = next_node.value
                self._detach_next(node)
                return value
            if next_idx > normal_idx:
                break
        msg = f"bad index={index}"
        raise IndexError(msg)

    def popleft(self) -> Any:
        """Return the detached leftmost node.

        Raises
        ------
        IndexError
            when popping from an empty list.

        Returns
        -------
        Any
            the first/head item of the list
        """
        if old_head := self._head:
            self._head = old_head.next
            self._length -= 1
            return _delete_node(old_head)
        msg = "cannot pop from an empty list"
        raise IndexError(msg)

    def popright(self) -> Any:
        """Return the detached rightmost node.

        Raises
        ------
        IndexError
            when popping from an empty list.

        Returns
        -------
        Any
            the last/tail item of the list
        """
        if pretail := self._pretail:
            return self._detach_next(pretail)
        return self.popleft()

    def prepend(self, value: Any, /) -> None:
        """Prepend (add to the beginning) the value.

        Parameters
        ----------
        value : Any

        Returns
        -------
        None
        """
        node = _SinglyLinkedNode(value)
        node.next = self._head
        self._head = node
        self._length += 1

    def remove(self, value: Any, /) -> None:
        """Remove the first occurence of the value.

        Parameters
        ----------
        value : Any - value to remove from the list

        Raises
        ------
        ValueError
            if value not in the list

        Returns
        -------
        None
        """
        for idx, node in enumerate(self._yield_nodes()):
            if not idx and node.value == value:
                self.popleft()
                return
            if (next_node := node.next) and (next_node.value == value):
                self._detach_next(node)
                return
        msg = f"{value!r} is not in the list"
        raise ValueError(msg)

    def reverse(self) -> None:
        """Reverse the list in place."""
        # if this is not exhausted here
        rev = tuple(reversed(self))
        # then the list is cleared...
        self.clear()
        # ... and no node to extend from the `rev`
        self.extend(rev)

    def sort(
        self, /, *, key: None | Callable = None, reverse: bool = False
    ) -> None:
        """Sort the list in place.

        Parameters
        ----------
        key : None | Callable, default None
        reverse : bool, default False

        Returns
        -------
        None
        """
        items = merge_sort(tuple(self), key=key, reverse=reverse)
        self.clear()
        self.extend(items)
