class Node:
    def __init__(self, value=None, color='red'):
        self.value = value
        self.color = color  # 'red' or 'black'
        self.left = None
        self.right = None
        self.parent = None
        self.is_right_child = False
        self.isRoot = False

    def recolor_to_black(self):
        self.color = 'black'

    def recolor_to_red(self):
        if self.isRoot == True:
            self.color = 'black' ##root must stay black
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


    def searchTree(self, valueToBeSearched):
        node = self.root
        while node is not None:
            if valueToBeSearched < node.value:
                node = node.left
            elif valueToBeSearched > node.value:
                node = node.right
            else:
                return True  # Found it
        return False  # Not found
    


    def checkRotations(self, node):
        if node == None:
            return 
        
        if node.parent != None: 
            parent = node.parent
        else:
            parent = None 
            return # no violations if no parent
        
        # No violation if parent is black
        if parent.color == 'black':
            return
            
        if parent.parent != None:
            grandparent = parent.parent
        else:
            grandparent = None
            return  # parent is root and red, just recolor it

        # determine uncle
        uncle = None
        if grandparent is not None:
            if grandparent.left == parent:
                uncle = grandparent.right
            else:
                uncle = grandparent.left

        # Case 1: parent and uncle are red -> recolor and bubble up
        if uncle is not None and uncle.color == 'red':
            parent.recolor_to_black()
            uncle.recolor_to_black()
            if not grandparent.isRoot:
                grandparent.recolor_to_red()
            # bubble up
            self.checkRotations(grandparent)
            print("case 1 executed")
            return
            

        # At this point, uncle is black or None, and parent is red
        
        # Case 2: Left-Right (node is right child, parent is left child)
        if node.is_right_child and not parent.is_right_child:
            self.rotateLeft(parent)
            # After rotation, continue with the old parent (now child)
            node = parent
            parent = node.parent
            grandparent = parent.parent
            print("case 2 executed")

        # Case 2 mirrored: Right-Left (node is left child, parent is right child)
        if not node.is_right_child and parent.is_right_child:
            self.rotateRight(parent)
            # After rotation, continue with the old parent (now child)
            node = parent
            parent = node.parent
            grandparent = parent.parent
            print("case 2 mirrored executed")

        # Case 3: Left-Left (both are left children)
        if not node.is_right_child and not parent.is_right_child:
            self.rotateRight(grandparent)
            parent.recolor_to_black()
            grandparent.recolor_to_red()
            print("case 3 executed")
            return
        
        # Case 3 mirrored: Right-Right (both are right children)
        if node.is_right_child and parent.is_right_child:
            self.rotateLeft(grandparent)
            parent.recolor_to_black()
            grandparent.recolor_to_red()
            print("case 3 mirrored executed")
            return


    def rotateLeft(self, nodeToRotateOn):
        newRoot = nodeToRotateOn.right
        nodeToRotateOn.right = newRoot.left

    # Update parent pointer for the transferred subtree
        if newRoot.left is not None:
            newRoot.left.parent = nodeToRotateOn
            newRoot.left.is_right_child = True 
        
        # Update parent pointer for the transferred subtree
        if newRoot.left is not None:
            newRoot.left.parent = nodeToRotateOn
        
        # Update newRoot's parent
        newRoot.parent = nodeToRotateOn.parent
        
        # Update grandparent's child pointer
        if nodeToRotateOn.parent is None:
            self.root = newRoot
            newRoot.isRoot = True
            nodeToRotateOn.isRoot = False
        elif nodeToRotateOn.is_right_child:
            nodeToRotateOn.parent.right = newRoot
            newRoot.is_right_child = True
        else:
            nodeToRotateOn.parent.left = newRoot
            newRoot.is_right_child = False
        
        # Complete the rotation
        newRoot.left = nodeToRotateOn
        nodeToRotateOn.parent = newRoot
        nodeToRotateOn.is_right_child = False


    def rotateRight(self, nodeToRotateOn):
        newRoot = nodeToRotateOn.left
        nodeToRotateOn.left = newRoot.right

        if newRoot.right is not None:
            newRoot.right.parent = nodeToRotateOn
            newRoot.right.is_right_child = False 
        
        # Update parent pointer for the transferred subtree
        if newRoot.right is not None:
            newRoot.right.parent = nodeToRotateOn
        
        # Update newRoot's parent
        newRoot.parent = nodeToRotateOn.parent
        
        # Update grandparent's child pointer
        if nodeToRotateOn.parent is None:
            self.root = newRoot
            newRoot.isRoot = True
            nodeToRotateOn.isRoot = False
        elif nodeToRotateOn.is_right_child:
            nodeToRotateOn.parent.right = newRoot
            newRoot.is_right_child = True
        else:
            nodeToRotateOn.parent.left = newRoot
            newRoot.is_right_child = False
        
        # Complete the rotation
        newRoot.right = nodeToRotateOn
        nodeToRotateOn.parent = newRoot
        nodeToRotateOn.is_right_child = True


    def insertInTree(self, value):
        # new nodes are red by default in a red-black tree

        newNode = Node(value, 'red')

        # insert as root if tree is empty
        if self.root is None:
            self.root = newNode
            self.root.parent = None
            self.size = 1
            self.root.isRoot = True
            # ensure root is black
            self.root.color = 'black'
            return

        nextNode = self.root
        while True:
            if value < nextNode.value:
                if nextNode.left is None:
                    nextNode.left = newNode
                    newNode.parent = nextNode
                    newNode.is_right_child = False
                    if self.size == 0:
                        newNode.isRoot = True
                    self.size += 1
                    break
                else:
                    nextNode = nextNode.left
            else:
                if nextNode.right is None:
                    nextNode.right = newNode
                    newNode.parent = nextNode
                    newNode.is_right_child = True
                    if self.size == 0:
                        newNode.isRoot = True
                    self.size += 1
                    break
                else:
                    nextNode = nextNode.right

        # increase size and rebalance
        self.size += 1
        self.checkRotations(newNode)
        return
    

    
    def deleteFromTree(self, value):
        node = self.root
        # Find the node
        while node and node.value != value:
            node = node.left if value < node.value else node.right
        if node is None:
            print("Value not found")
            return

        # Case 1: Node has two children
        if node.left and node.right:
            # Find predecessor (max in left subtree)
            pred = node.left
            while pred.right:
                pred = pred.right
            node.value = pred.value  # Copy value
            node = pred  # Now delete the predecessor node

        # Now node has at most one child
        child = node.left if node.left else node.right

        # remember original parent for deletion fixup
        original_parent = node.parent

        if node.parent is None:
            # Node is root
            self.root = child
            if child:
                child.parent = None
                child.isRoot = True
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            if child:
                child.parent = node.parent

        # Optionally: clean up node's pointers
        node.left = node.right = node.parent = None

        # Call deletion fixup with the replacement node and original parent
        self.checkRotationsForDeletion(child, original_parent)

 
        

    def findLargestFromLeftSubtree(self, node):
        nextNode = node.left
        while nextNode.right is not None: 
            nextNode = nextNode.right

        return nextNode

    def InOrderTraversal(self):
        """Return a list of node values in in-order (left, root, right).

        This is a simple, non-recursive-safe implementation using recursion.
        It does not modify the tree.
        """
        result = []

        def _rec(n):
            if n is None:
                return
            _rec(n.left)
            result.append(n.value)
            _rec(n.right)

        _rec(self.root)
        return result

    def checkRotationsForDeletion(self, x, parent=None):
        """Fix red-black properties after deletion.

        x: the node that replaced the deleted node (may be None)
        parent: the parent of x at the time of replacement (if x is None)
        Implements the classical CLRS delete-fixup algorithm.
        """
        def is_black(n):
            return (n is None) or (getattr(n, 'color', 'black') == 'black')

        # If x is None, use the provided parent as the starting point
        while (x is not None and x != self.root and x.color == 'black') or (x is None and parent is not None):
            if x is None:
                p = parent
                # If parent has no children, break
                if p is None:
                    break
                # Determine side: if parent's left is None or was the replacement, treat as left
                is_left = (p.left is None)
            else:
                p = x.parent
                if p is None:
                    break
                is_left = (x == p.left)

            if p is None:
                break

            if is_left:
                w = p.right
                # Case 1: sibling is red
                if w is not None and w.color == 'red':
                    w.color = 'black'
                    p.color = 'red'
                    self.rotateLeft(p)
                    w = p.right

                # Case 2: sibling's children are both black
                if is_black(getattr(w, 'left', None)) and is_black(getattr(w, 'right', None)):
                    if w is not None:
                        w.color = 'red'
                    x = p
                    parent = x.parent
                else:
                    # Case 3: sibling's right child is black
                    if is_black(getattr(w, 'right', None)):
                        if w is not None and w.left is not None:
                            w.left.color = 'black'
                        if w is not None:
                            w.color = 'red'
                            self.rotateRight(w)
                            w = p.right
                    # Case 4
                    if w is not None:
                        w.color = p.color
                    p.color = 'black'
                    if w is not None and w.right is not None:
                        w.right.color = 'black'
                    self.rotateLeft(p)
                    x = self.root
                    parent = None
            else:
                # mirror cases: x is right child
                w = p.left
                if w is not None and w.color == 'red':
                    w.color = 'black'
                    p.color = 'red'
                    self.rotateRight(p)
                    w = p.left

                if is_black(getattr(w, 'left', None)) and is_black(getattr(w, 'right', None)):
                    if w is not None:
                        w.color = 'red'
                    x = p
                    parent = x.parent
                else:
                    if is_black(getattr(w, 'left', None)):
                        if w is not None and w.right is not None:
                            w.right.color = 'black'
                        if w is not None:
                            w.color = 'red'
                            self.rotateLeft(w)
                            w = p.left
                    if w is not None:
                        w.color = p.color
                    p.color = 'black'
                    if w is not None and w.left is not None:
                        w.left.color = 'black'
                    self.rotateRight(p)
                    x = self.root
                    parent = None

        # Ensure the node (if exists) is black
        if x is not None:
            x.color = 'black'
