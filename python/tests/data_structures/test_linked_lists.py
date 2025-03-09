from adspy.data_structures.linked_lists import (
    DoublyLinkedNode,
    SinglyLinkedNode,
)


class TestSinglyLinkedNodes:
    def test_value_attribute_accessors(self):
        snode = SinglyLinkedNode()

        assert snode.value is None

        value = 42
        snode.value = value

        assert snode.value == value

    def test_next_attribute_accessors(self):
        snode = SinglyLinkedNode()

        assert snode.next is None

        next_node = SinglyLinkedNode(21)
        snode.next = next_node

        assert snode.value is None
        assert snode.next.value is next_node


class TestDoublyLinkedNodes:
    def test_value_attribute_accessors(self):
        dnode = DoublyLinkedNode()

        assert dnode.value is None

        value = 42
        dnode.value = value

        assert dnode.value == value

    def test_next_attribute_accessors(self):
        dnode = DoublyLinkedNode()

        assert dnode.prev is None
        assert dnode.next is None

        prev_node = DoublyLinkedNode(21)
        dnode.prev = prev_node

        next_node = DoublyLinkedNode(42)
        dnode.next = next_node

        assert dnode.prev.value is prev_node
        assert dnode.next.value is next_node
