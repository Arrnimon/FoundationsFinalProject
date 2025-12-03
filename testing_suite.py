from RBtree1 import Node
from pretty_printer import PrettyPrinter


def smoke_test():
    # Build a small tree manually (avoid using RBtree insertion logic)
    root = Node(20, 'black')
    left = Node(10, 'red')
    right = Node(30, 'red')
    left_left = Node(5, 'black')
    left_right = Node(15, 'black')
    right_left = Node(25, 'black')
    right_right = Node(35, 'black')

    root.left = left
    root.right = right
    left.left = left_left
    left.right = left_right
    right.left = right_left
    right.right = right_right

    print("--- Pretty print (no color) ---")
    PrettyPrinter.pretty_print(root, use_color=False)


if __name__ == '__main__':
    smoke_test()
