class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    """Simple unbalanced Binary Search Tree with insert, delete, search."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = BSTNode(key)
                    return
                cur = cur.right

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def _find_min(self, node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    def delete(self, key):
        self.root = self._delete_rec(self.root, key)

    def _delete_rec(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_rec(node.left, key)
        elif key > node.key:
            node.right = self._delete_rec(node.right, key)
        else:
            # node to delete
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                succ = self._find_min(node.right)
                node.key = succ.key
                node.right = self._delete_rec(node.right, succ.key)
        return node

    # Compatibility wrappers used by benchmark (match RBtree API names)
    def insertInTree(self, key):
        return self.insert(key)

    def searchTree(self, key):
        return self.search(key)

    def deleteFromTree(self, key):
        return self.delete(key)
