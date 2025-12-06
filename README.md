# RB Tree Pretty Print Demo

This repo contains a pretty-print utility that can render a red-black tree
as ASCII. The `rb_tree_pretty.py` module now prefers to use the `RBtree` and
`Node` implementation from `RBtree1.py` when available — falling back to a
small internal demo tree for demonstration purposes.

How to run

```powershell
python rb_tree_pretty.py
```

The demo prints a tree twice: once with no ANSI color and once with red nodes
highlighted using ANSI sequences (if your terminal supports them).

Notes

- `pretty_print` focuses on pretty ASCII output and color hints only; it is
  intentionally minimal and readable for teaching and logging. It accepts
  either an `RBtree` instance from `RBtree1` or a plain node object with
  `value`, `left`, `right`, and `color` attributes.
- If you want full red-black behavior (rotations, rebalancing), I can add
  `insert_fixup` and rotate operations — let me know.

