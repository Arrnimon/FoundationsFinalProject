

class Node:
    def __init__(self, value=None, color='red'):
        self.value = value
        self.color = color  # 'red' or 'black'
        self.left = None
        self.right = None
        self.parent = None
        self.is_right_child = False

    def recolor(self):
        if self.color == 'red':
            self.color = 'black'
        else:
            self.color = 'red'


class RBtree:
    def __init__(self):
        # the root of the tree; empty tree starts with no root
        self.root = None
        self.size = 0
        self.leftSubtree = None
        self.rightSubtree = None

    def is_empty(self):
        return self.size == 0
    

    def insertInTree(self, value):
        # new nodes are red by default in a red-black tree
        newNode = Node(value, 'red')

        # insert as root if tree is empty
        if self.root is None:
            self.root = newNode
            self.root.parent = None
            self.size = 1
            # ensure root is black
            self.root.color = 'black'
            return

        nextNode = self.root
        while True:
            if value < nextNode.value:
                if nextNode.left is None:
                    nextNode.left = newNode
                    newNode.parent = nextNode
                    break
                else:
                    nextNode = nextNode.left
            else:
                if nextNode.right is None:
                    nextNode.right = newNode
                    newNode.parent = nextNode
                    break
                else:
                    nextNode = nextNode.right

        # increase size and rebalance
        self.size += 1
        self.checkRotations(newNode)
        return

    def checkRotations(self, node):
        parent = node.parent
        grandparent = parent.parent

        # determine uncle
        uncle = None
        if grandparent is not None:
            if grandparent.left == parent:
                uncle = grandparent.right
            else:
                uncle = grandparent.left

        # Case 1: parent and uncle are red -> recolor and bubble up
        if parent.color == 'red' and uncle is not None and uncle.color == 'red':
            parent.color = 'black'
            uncle.color = 'black'
            grandparent.color = 'red'
            # may need to continue fixing up the tree
            self.checkRotations(grandparent)
            return

        # Case 2 and 3: uncle is black (or None) and parent is red -> rotations
        if parent.color == 'red' and (uncle is None or uncle.color == 'black'):
            # compute helper boolean flags for child/parent alignment
            node.is_right_child = (parent.right == node)
            parent.is_right_child = (grandparent is not None and grandparent.right == parent)

            # double-rotation cases: convert to single-line case
            if node.is_right_child and not parent.is_right_child:
                # Right child of left subtree -> rotate left on parent
                self.rotateLeft(parent)
                # after rotation, update references
                node = parent


    def rotateLeft(self, nodeToRotateOn):
        if nodeToRotateOn is None:
            return
        newRoot = nodeToRotateOn.right
        if newRoot is None:
            return
        # perform rotation
        nodeToRotateOn.right = newRoot.left
        if newRoot.left is not None:
            newRoot.left.parent = nodeToRotateOn
        newRoot.parent = nodeToRotateOn.parent
        if nodeToRotateOn.parent is None:
            self.root = newRoot
        else:
            if nodeToRotateOn.parent.left == nodeToRotateOn:
                nodeToRotateOn.parent.left = newRoot
            else:
                nodeToRotateOn.parent.right = newRoot
        newRoot.left = nodeToRotateOn
        nodeToRotateOn.parent = newRoot


    def rotateLeft(nodeToRotateOn):
        temp = nodeToRotateOn.right.left
        newRoot = nodeToRotateOn.right
        newRoot.left = nodeToRotateOn
        if(temp is not None):
            nodeToRotateOn.right = temp


    def rotateRight(nodeToRotateOn):
        newRoot = nodeToRotateOn.left
        temp = newRoot.right
        newRoot.right = nodeToRotateOn
        if(temp is not None):
            nodeToRotateOn.left = temp







    


