"""Pretty-print utilities for Red-Black trees.

This module is strictly responsible for rendering a tree or node as ASCII
art. It does not modify tree data structures or implement RB-tree logic.

API:
- `PrettyPrinter.pretty_print(obj, use_color=False)`: print to stdout.
- `PrettyPrinter.format_lines(obj, use_color=False)`: return list[str].

This module expects tree/node objects that expose `value`, `color`, `left`,
and `right` attributes. It will also accept an `RBtree` instance that exposes
the `root` attribute.
"""

from __future__ import annotations
from typing import Optional, Any, List

from RBtree1 import RBtree, Node


class PrettyPrinter:
    ANSI_RED = "\x1b[31m"
    ANSI_RESET = "\x1b[0m"

    @staticmethod
    def _color_text(text: str, color_name: str, use_color: bool = True) -> str:
        if not use_color:
            return text
        if color_name == "red":
            return PrettyPrinter.ANSI_RED + text + PrettyPrinter.ANSI_RESET
        return text

    @staticmethod
    def _node_label(node: Any, use_color: bool) -> str:
        value = getattr(node, "value", None)
        color = getattr(node, "color", "black")
        label = f"{value} ({'R' if color == 'red' else 'B'})"
        if use_color and color == "red":
            label = PrettyPrinter._color_text(label, "red", use_color)
        return label

    @staticmethod
    def _format_lines(node_or_tree: Any, use_color: bool = False) -> List[str]:
        """Return list of lines representing the tree/node.

        This function is pure rendering: it does not change the tree.
        It accepts either a node-like object or an `RBtree` instance.
        """
        # Accept RBtree instances by extracting root, but do not modify them
        node = getattr(node_or_tree, "root", node_or_tree)

        def rec(n: Optional[Any]) -> List[str]:
            if n is None:
                return ["(empty)"]

            # label for current node
            label = PrettyPrinter._node_label(n, use_color)

            left = getattr(n, "left", None)
            right = getattr(n, "right", None)

            # leaf
            if (left is None) and (right is None):
                return [label]

            left_lines = rec(left) if left is not None else []
            right_lines = rec(right) if right is not None else []

            # Print right subtree first so the right sibling appears above the left
            lines: List[str] = [label]

            def add_side(prefix: str, lines_list: List[str], is_last_side: bool = False) -> None:
                if not lines_list:
                    lines.append(prefix + "(none)")
                    return
                for i, l in enumerate(lines_list):
                    connector = "└─ " if i == len(lines_list) - 1 else "├─ "
                    if i == 0:
                        lines.append(prefix + connector + l)
                    else:
                        lines.append(prefix + ("   " if is_last_side else "│  ") + l)

            # Right first (top sibling), then left (bottom sibling)
            add_side("", right_lines, is_last_side=(len(left_lines) == 0))
            add_side("", left_lines, is_last_side=True)

            return lines

        return rec(node)

    @staticmethod
    def format_lines(node_or_tree: Any, use_color: bool = False) -> List[str]:
        """Public: return ASCII lines for the given tree/node."""
        return PrettyPrinter._format_lines(node_or_tree, use_color=use_color)

    @staticmethod
    def pretty_print(node_or_tree: Any, use_color: bool = False) -> None:
        """Print the ASCII representation to stdout."""
        for line in PrettyPrinter.format_lines(node_or_tree, use_color=use_color):
            print(line)


def pretty_print(node_or_tree: Any, use_color: bool = False) -> None:
    """Convenience wrapper: print the tree/node."""
    PrettyPrinter.pretty_print(node_or_tree, use_color=use_color)
