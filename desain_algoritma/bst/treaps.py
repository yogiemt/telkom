import random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.randint(1, 100)
        self.left = None
        self.right = None

    def __str__(self):
        # Short, readable label used by the ASCII printer
        return f"{self.key}(p={self.priority})"

    def left_rotation(self):
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        return new_root
    
    def right_rotation(self):
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        return new_root
    
    def insert_node(self, key, priority=None):
        if key < self.key:
            if self.left is None:
                self.left = TreapNode(key, priority)
            else:
                self.left = self.left.insert_node(key, priority)
            if self.left.priority > self.priority:
                return self.right_rotation()
        elif key > self.key:
            if self.right is None:
                self.right = TreapNode(key, priority)
            else:
                self.right = self.right.insert_node(key, priority)
            if self.right.priority > self.priority:
                return self.left_rotation()
        return self

    def search_node(self, key):
        if self.key == key:
            return self
        elif key < self.key and self.left:
            return self.left.search_node(key)
        elif key > self.key and self.right:
            return self.right.search_node(key)
        return None
    
    def remove_node(self, key):
        if key < self.key:
            if self.left:
                self.left = self.left.remove_node(key)
        elif key > self.key:
            if self.right:
                self.right = self.right.remove_node(key)
        else:
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                if self.left.priority > self.right.priority:
                    new_root = self.right_rotation()
                    new_root.right = new_root.right.remove_node(key)
                    return new_root
                else:
                    new_root = self.left_rotation()
                    new_root.left = new_root.left.remove_node(key)
                    return new_root
        return self

def print_tree_horizontal(node, prefix="", is_left=True):
    if node is not None:
        # Print the right subtree first (so it appears on top)
        print_tree_horizontal(node.right, prefix + ("│   " if is_left else "    "), False)
        
        # Print current node
        print(prefix + ("└── " if is_left else "┌── ") + f"{node.key} (p={node.priority})")
        
        # Print the left subtree
        print_tree_horizontal(node.left, prefix + ("    " if is_left else "│   "), True)


# Helper that builds a pretty ASCII block for a subtree and returns:
# (lines: list[str], width: int, height: int, middle: int)
def _build_lines(node):
    """Recursively build ASCII tree layout."""
    if node is None:
        return [], 0, 0, 0

    label = str(node)
    left_lines, left_w, left_h, left_mid = _build_lines(node.left)
    right_lines, right_w, right_h, right_mid = _build_lines(node.right)

    label_w = len(label)

    # No children — just return label
    if left_w == 0 and right_w == 0:
        return [label], label_w, 1, label_w // 2

    gap = 2  # spacing between subtrees
    # Ensure total width can at least contain the label itself to avoid overflow
    total_w = max(left_w + gap + right_w, label_w)
    label_start = max(0, left_w + gap // 2 - label_w // 2)
    # Clamp label_start so the label fits inside the allocated width
    label_start = min(label_start, max(0, total_w - label_w))

    # First line (label)
    first = [" "] * total_w
    for i, ch in enumerate(label):
        first[label_start + i] = ch
    first = "".join(first)

    # Second line (branches)
    second = [" "] * total_w
    if node.left:
        second[left_mid] = "/"
        for i in range(left_mid + 1, label_start):
            second[i] = "_"
    if node.right:
        right_root = left_w + gap + right_mid
        for i in range(label_start + label_w, right_root):
            second[i] = "_"
        second[right_root] = "\\"
    second = "".join(second)

    # Merge child lines (pad shorter one)
    child_h = max(left_h, right_h)
    left_block = left_lines + [" " * left_w] * (child_h - left_h)
    right_block = right_lines + [" " * right_w] * (child_h - right_h)
    merged = [l + (" " * gap) + r for l, r in zip(left_block, right_block)]
    # If we increased total_w above left_w+gap+right_w to fit the label,
    # pad merged child lines so they also match total_w and indexing won't fail.
    merged = [line + (" " * (total_w - len(line))) if len(line) < total_w else line for line in merged]

    return [first, second] + merged, total_w, 2 + child_h, label_start + label_w // 2


def print_tree(root):
    lines, _, _, _ = _build_lines(root)
    for line in lines:
        print(line.rstrip())


if __name__ == "__main__":
    treap = TreapNode(1, 73)
    keys_to_insert = [2, 3, 4, 5, 6, 7, 8]
    priorities = [10, 97, 56, 80, 31, 85, 92]

    for key, priority in zip(keys_to_insert, priorities):
        treap = treap.insert_node(key, priority)
    
    print("Treap after insertions:")
    print_tree(treap)

    search_key = 4
    found_node = treap.search_node(search_key)
    if found_node:
        print(f"\nNode with key {search_key} found: (Key: {found_node.key}, Priority: {found_node.priority})")
    else:
        print(f"\nNode with key {search_key} not found.")
    

    remove_key = 8
    treap = treap.remove_node(remove_key)
    print(f"\nTreap after removing key {remove_key}:")
    print_tree(treap)