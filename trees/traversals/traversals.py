#!/usr/bin/env python3
"""Preorder/Prefix Tree Traversal algorithm."""


from typing import Callable, TypeVar


TreeNode = TypeVar("TreeNode")


def traverse_preorderly(node: TreeNode, func: Callable):
    """Preorder/Prefix Tree Traversal algorithm.

    Parameters
    ----------
    node : TreeNode
        a tree or a node of a tree.
    func : Callable
        to apply to each node.
    """
    func(node)
    for child in node.children:
        traverse_preorderly(child, func)


def traverse_inorderly(node: TreeNode, func: Callable):
    """Inorder/Infix Tree Traversal algorithm.

    Parameters
    ----------
    node : TreeNode
        a tree or a node of a tree.
    func : Callable
        to apply to each node.

    Raises
    ------
    ValueError:
        if a non-binary tree node is encountered.
    """
    children = len(node.children)
    if children > 2:
        raise ValueError(f"non-binary tree node: {node}")
    if children >= 1:
        traverse_inorderly(node.children[0], func)
    func(node)
    if children >= 2:
        traverse_inorderly(node.children[1], func)


def traverse_postorderly(node: TreeNode, func: Callable):
    """Postorder/Postfix Tree Traversal algorithm.

    Parameters
    ----------
    node : TreeNode
        a tree or a node of a tree.
    func : Callable
        to apply to each node.
    """
    for child in node.children:
        traverse_postorderly(child, func)
    func(node)
