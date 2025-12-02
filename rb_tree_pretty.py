"""Pretty-print a Red-Black tree (ASCII) using the RBtree1 implementation.

This module focuses on printing a `RBtree` instance from `RBtree1.py` or
any node-like object with `value`, `color`, `left`, and `right` attributes.

Usage:
    from RBtree1 import RBtree
    t = RBtree()
    t.insertInTree(10)
    t.insertInTree(5)
    pretty_print(t, use_color=False)
"""
from __future__ import annotations
import sys
from typing import Optional

try:
    # prefer the user's provided RB tree implementation
    from RBtree1 import RBtree as RBTreeImpl, Node as RBNodeImpl
except Exception:
    RBTreeImpl = None
    RBNodeImpl = None


ANSI_RED = '\x1b[31m'
ANSI_RESET = '\x1b[0m'


def color_text(text: str, color_name: str, use_color: bool = True) -> str:
    if not use_color:
        return text
    if color_name == 'red':
        return ANSI_RED + text + ANSI_RESET
    return text


def _pretty_lines(node, use_color=True):
    """Return list of lines for tree rooted at `node`.

    The printing is tolerant of the input being either:
    - a node-like object with attributes: value, color, left, right
    - None
    """
    if node is None:
        return ["(empty)"]

    # Accept RBtree objects as top-level input
    if hasattr(node, 'root'):
        node = node.root
        if node is None:
            return ["(empty)"]

    # Node basics
    value = getattr(node, 'value', None)
    color = getattr(node, 'color', 'black')

    label = f"{value} ({'R' if color == 'red' else 'B'})"
    if use_color and color == 'red':
        label = color_text(label, 'red', use_color)

    left = getattr(node, 'left', None)
    right = getattr(node, 'right', None)

    if left is None and right is None:
        return [label]

    lines = [label]

    def add_side(prefix, lines_list, is_last_side=False):
        if not lines_list:
            lines.append(prefix + '(none)')
            return
        for i, l in enumerate(lines_list):
            connector = '└─ ' if i == len(lines_list) - 1 else '├─ '
            if i == 0:
                lines.append(prefix + connector + l)
            else:
                lines.append(prefix + ('   ' if is_last_side else '│  ') + l)

    left_lines = _pretty_lines(left, use_color) if left is not None else []
    right_lines = _pretty_lines(right, use_color) if right is not None else []

    is_right_last = len(right_lines) == 0
    add_side('', left_lines, is_last_side=is_right_last)
    add_side('', right_lines, is_last_side=True)

    return lines


def pretty_print(tree_or_root, use_color=False):
    """Print tree either from a node or RBtree instance.

    - If passed an `RBtree` instance (from RBtree1), it uses its `root`.
    - If passed a node directly, it prints that node's subtree.
    """
    # If passed an RBtree-like object, extract root
    root = getattr(tree_or_root, 'root', tree_or_root)
    lines = _pretty_lines(root, use_color=use_color)
    for line in lines:
        print(line)


if __name__ == '__main__':
    # Quick demo using RBtree1 if available; otherwise fall back to a
    # minimal internal construction compatible with the printer.
    if RBTreeImpl is not None:
        t = RBTreeImpl()
        # Try to use the RBtree1 insertion API but handle any internal errors
        # from RBtree1's implementation — we don't want a demo to crash.
        try:
            t.insertInTree(10)
            t.insertInTree(5)
            t.insertInTree(15)
            # Add more to see colors and depth
            t.insertInTree(2)
            t.insertInTree(7)
            t.insertInTree(12)
            t.insertInTree(20)
        except Exception:
            # If RBtree1 has a bug, fall back to constructing nodes manually
            root = RBNodeImpl(10, 'black')
            left = RBNodeImpl(5, 'red')
            right = RBNodeImpl(15, 'red')
            left.left = RBNodeImpl(2, 'black')
            left.right = RBNodeImpl(7, 'black')
            right.left = RBNodeImpl(12, 'black')
            right.right = RBNodeImpl(20, 'black')
            left.parent = root
            right.parent = root
            left.left.parent = left
            left.right.parent = left
            right.left.parent = right
            right.right.parent = right
            root.left = left
            root.right = right
            t.root = root

        print('Pretty print using RBtree1 (no ANSI colors):')
        pretty_print(t, use_color=False)
        print('\nPretty print using RBtree1 (with ANSI colors):')
        pretty_print(t, use_color=True)
    else:
        # Minimal fallback: lightweight node-like objects
        class Node:
            def __init__(self, value, color='black', left=None, right=None):
                self.value = value
                self.color = color
                self.left = left
                self.right = right

        root = Node(10, 'black', left=Node(5, 'red', left=Node(2, 'black'), right=Node(7, 'black')),
                    right=Node(15, 'red', left=Node(12, 'black'), right=Node(20, 'black')))

        print('Pretty print using fallback nodes (no ANSI colors):')
        pretty_print(root, use_color=False)
        print('\nPretty print using fallback nodes (with ANSI colors):')
        pretty_print(root, use_color=True)
class Node:
    def __init__(self, value, color='black', left=None, right=None, parent=None):
        self.value = value
        self.color = color  # 'red' or 'black'
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        return f"Node({self.value!r}, {self.color!r})"


class RBTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, value, color='red'):
        """
        Simple binary-search tree insertion; color is set to `color` flag for the node
        (this is NOT a full RB insertion with balancing/fixup) — it's enough for
        testing pretty-print and colors.
        """
        new = Node(value, color=color)
        if self.root is None:
            self.root = new
            self.root.color = 'black'  # keep root black as basic convention
            self.size = 1
            return self.root

        cur = self.root
        while True:
            if value < cur.value:
                if cur.left is None:
                    cur.left = new
                    new.parent = cur
                    self.size += 1
                    return new
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = new
                    new.parent = cur
                    self.size += 1
                    return new
                cur = cur.right


# Pretty print: ASCII tree, with optional ANSI coloring for red nodes

ANSI_RED = '\x1b[31m'
ANSI_BLACK = '\x1b[30m'  # usually black isn't visible; we use default for black
ANSI_BOLD = '\x1b[1m'
ANSI_RESET = '\x1b[0m'


def color_text(text, color_name, use_color=True):
    if not use_color:
        return text
    if color_name == 'red':
        return ANSI_RED + text + ANSI_RESET
    # For black, just return the text without color (default terminal color)
    return text


def _pretty_lines(node, use_color=True):
    """
    Helper: returns list of lines representing the tree rooted at `node`.
    This approach is the "top-down" ASCII art; it handles the left and right
    subtrees and composes the string lines so the tree is visually aligned.
    """
    if node is None:
        return ["(empty)"]

    # Node label: value + color label
    label = f"{node.value} ({'R' if node.color == 'red' else 'B'})"
    if use_color and node.color == 'red':
        # add ANSI color for red label
        label = color_text(label, 'red', use_color)

    # Recursively build left/right lines
    left_lines = _pretty_lines(node.left, use_color) if node.left else []
    right_lines = _pretty_lines(node.right, use_color) if node.right else []

    # If both children are empty, just return the label
    if not left_lines and not right_lines:
        return [label]

    # Build left subtree lines with a left prefix and right subtree lines with a right prefix
    # We'll construct using ├─ and └─ and vertical bars for continuation
    lines = [label]

    def add_side(prefix, lines_list, is_last_side=False):
        if not lines_list:
            lines.append(prefix + '(none)')
            return
        for i, l in enumerate(lines_list):
            connector = '└─ ' if i == len(lines_list) - 1 else '├─ '
            if i == 0:
                lines.append(prefix + connector + l)
            else:
                # continuation lines: replace connector with spaces to line up
                lines.append(prefix + ('   ' if is_last_side else '│  ') + l)

    # Add left and right with proper join
    # We print left first then right; use prefixes to align children under the root
    add_side('', left_lines, is_last_side=(len(right_lines) == 0))
    add_side('', right_lines, is_last_side=True)

    return lines


def pretty_print(root, use_color=False):
    """Print a tree in readable ASCII form.

    - `use_color`: if True, nodes colored 'red' will be displayed in ANSI red (if supported).
      Default is False to be safe on Windows/Powershell terminals.
    """
    lines = _pretty_lines(root, use_color=use_color)
    for line in lines:
        print(line)


if __name__ == '__main__':
    # Demo usage
    t = RBTree()
    # Insert sample values and set explicit colors for demo
    t.insert(10, color='black')
    left = t.insert(5, color='red')
    right = t.insert(15, color='red')
    left_left = Node(2, 'black')
    left_right = Node(7, 'black')
    left.left = left_left
    left.right = left_right

    right_left = Node(12, 'black')
    right_right = Node(20, 'black')
    right.left = right_left
    right.right = right_right

    print('Pretty print without ANSI colors:')
    pretty_print(t.root, use_color=False)
    print('\nPretty print WITH ANSI colors (red is highlighted):')
    pretty_print(t.root, use_color=True)
