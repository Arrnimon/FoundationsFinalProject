from RBtree1 import Node, RBtree
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

def TestOne():
    ##inserts the values automatically using the insert function in RBtree1

    tree = RBtree()
    values_to_insert = [20, 10, 30, 5, 15, 25, 35]
    for value in values_to_insert:
        tree.insertInTree(value)
    
    print("--- Pretty print of automatically inserted tree (no color) ---")
    PrettyPrinter.pretty_print(tree, use_color=True)





if __name__ == '__main__':
    TestOne()
    
