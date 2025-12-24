
class BinaryTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def __str__(self):
        return f"({self.key})"

    def insert(self, key):
        """Insert a key into the BST."""
        if key < self.key:
            if self.left is None:
                self.left = BinaryTreeNode(key)
            else:
                self.left.insert(key)
        else:
            if self.right is None:
                self.right = BinaryTreeNode(key)
            else:
                self.right.insert(key)
        # if key == self.key → ignore duplicates
        return self

    def search(self, key):
        """Search for a key in the BST."""
        if self.key == key:
            return self
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        return None

    def find_min(self):
        """Return node with the smallest key."""
        current = self
        while current.left is not None:
            current = current.left
        return current

    def remove(self, key):
        """Remove a node from the BST."""
        if key < self.key:
            if self.left:
                self.left = self.left.remove(key)
        elif key > self.key:
            if self.right:
                self.right = self.right.remove(key)
        else:
            # Found the node to delete
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            # Node with two children: find inorder successor
            temp = self.right.find_min()
            self.key = temp.key
            self.right = self.right.remove(temp.key)
        return self
    
    def inorder_traversal(self):
        """Inorder traversal of the BST."""
        elements = []
        if self.left:
            elements += self.left.inorder_traversal()
        elements.append(self.key)
        if self.right:
            elements += self.right.inorder_traversal()
        return elements
    

data = int(input())
binaryTree = BinaryTreeNode(data)

while True:
    data = int(input())
    if data == 0:
        break
    binaryTree.insert(data)

print(" ".join([str(x) for x in binaryTree.inorder_traversal()]))



