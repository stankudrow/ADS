#!/usr/bin/env python3
"""Tests traversal algorithms on trees."""


from typing import Callable
from pytest import mark

from anytree import Node

from traversals import (
    traverse_preorderly,
    traverse_inorderly,
    traverse_postorderly,
)


def tree1():
    return Node(
        "root",
        children=[
            Node("A", children=[Node("A1")]),
            Node("B", children=[Node("B1"), Node("B2")]),
        ],
    )


# pytest --capture=sys ...
@mark.parametrize(
    "tree, preres, inres, postres",
    [
        (
            tree1(),
            "root\nA\nA1\nB\nB1\nB2\n",
            "A1\nA\nroot\nB1\nB\nB2\n",
            "A1\nA\nB1\nB2\nB\nroot\n",
        ),
    ],
)
def test_traversals(
    capsys,
    tree: Node,
    preres: str,
    inres: str,
    postres: str,
):
    """Tests tree traversal algorithms.

    Parameters
    ----------
    capsys
        pytest stdouterr capturing fixture.
    tree : Node
    preres : str
        preorder/prefix result.
    inres : str
        inorder/infix result.
    postres : str
        postorder/postfix result.
    """
    func: Callable = lambda node: print(node.name)
    traverse_preorderly(tree, func)
    assert capsys.readouterr().out == preres
    traverse_inorderly(tree, func)
    assert capsys.readouterr().out == inres
    traverse_postorderly(tree, func)
    assert capsys.readouterr().out == postres
