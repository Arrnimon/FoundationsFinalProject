class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def _height(node):
    return node.height if node else 0


def _update_height(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node):
    return _height(node.left) - _height(node.right) if node else 0


def _rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    _update_height(x)
    _update_height(y)
    return y


class AVL:
    """AVL tree implementation with insert, delete, search, and RBtree-compatible wrappers."""
    def __init__(self):
        self.root = None

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

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        _update_height(node)
        bf = _balance_factor(node)

        # Left Left
        if bf > 1 and key < node.left.key:
            return _rotate_right(node)
        # Right Right
        if bf < -1 and key > node.right.key:
            return _rotate_left(node)
        # Left Right
        if bf > 1 and key > node.left.key:
            node.left = _rotate_left(node.left)
            return _rotate_right(node)
        # Right Left
        if bf < -1 and key < node.right.key:
            node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    def _find_min(self, node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # node to delete
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                succ = self._find_min(node.right)
                node.key = succ.key
                node.right = self._delete(node.right, succ.key)

        _update_height(node)
        bf = _balance_factor(node)

        # Rebalance
        if bf > 1:
            if _balance_factor(node.left) < 0:
                node.left = _rotate_left(node.left)
            return _rotate_right(node)
        if bf < -1:
            if _balance_factor(node.right) > 0:
                node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    # Compatibility wrappers
    def insertInTree(self, key):
        return self.insert(key)

    def searchTree(self, key):
        return self.search(key)

    def deleteFromTree(self, key):
        return self.delete(key)
