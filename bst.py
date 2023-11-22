import json
from typing import List

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    # Base Case: If the tree is empty (root is None), create a new node with the given key and return it.
    if root is None:
        return Node(key=key, keycount=1)

    # Compare the key with the current node's key.
    if key < root.key:
        # If the key is less than the current node's key, recursively insert it into the left subtree.
        root.leftchild = insert(root.leftchild, key)
    elif key > root.key:
        # If the key is greater than the current node's key, recursively insert it into the right subtree.
        root.rightchild = insert(root.rightchild, key)
    else:
        # If the key is equal to the current node's key, increment its keycount.
        root.keycount += 1
        
    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    # Base Case: If the tree is empty (root is None), return None.
    if root is None:
        return root

    # Compare the key with the current node's key.
    if key < root.key:
        # If the key is less than the current node's key, recursively delete it from the left subtree.
        root.leftchild = delete(root.leftchild, key)
    elif key > root.key:
        # If the key is greater than the current node's key, recursively delete it from the right subtree.
        root.rightchild = delete(root.rightchild, key)
    else:
        # If the key matches the current node's key:
        if key == root.key:
            # Decrement the key count.
            if root.keycount > 1:
                root.keycount -= 1
            else:
                # If keycount is 1, it's time to remove the key from the tree.

                # If the node has only one child (or no child), replace it with its non-empty child (if any).
                if root.leftchild is None:
                    temp = root.rightchild
                    del root
                    return temp
                elif root.rightchild is None:
                    temp = root.leftchild
                    del root
                    return temp

                # If the node has two children, find the in-order successor (minimum value in the right subtree).
                succ = find_min(root.rightchild)

                # Copy the in-order successor's key and key count to this node.
                root.key = succ.key
                root.keycount = succ.keycount

                # Set the key count of the successor to 1.
                succ.keycount = 1
                # Delete the in-order successor node.
                root.rightchild = delete(root.rightchild, succ.key)

    return root

# Helper function to find the node with the minimum key in a BST.
def find_min(node: Node) -> Node:
    current = node
    while current.leftchild is not None:
        current = current.leftchild
    return current

# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    def find_path(node, key, path):
        if node is None:
            return path
        path.append(node.key)
        if key == node.key:
            return path
        elif key < node.key:
            return find_path(node.leftchild, key, path)
        else:
            return find_path(node.rightchild, key, path)

    path = find_path(root, search_key, [])
    return json.dumps(path, indent=2)
    
# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorder(root: Node) -> str:
    def traverse(node, result):
        if node is not None:
            result.append(node.key)  # Visit the current node
            traverse(node.leftchild, result)  # Traverse the left subtree
            traverse(node.rightchild, result)  # Traverse the right subtree

    result = []
    traverse(root, result)  # Start traversal from the root
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorder(root: Node) -> str:
    def traverse(node, result):
        if node is not None:
            traverse(node.leftchild, result)  # Traverse the left subtree
            result.append(node.key)  # Visit the current node
            traverse(node.rightchild, result)  # Traverse the right subtree

    result = []
    traverse(root, result)  # Start traversal from the root
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.
def postorder(root: Node) -> str:
    def traverse(node, result):
        if node is not None:
            traverse(node.leftchild, result)  # Traverse the left subtree
            traverse(node.rightchild, result)  # Traverse the right subtree
            result.append(node.key)  # Visit the current node

    result = []
    traverse(root, result)  # Start traversal from the root
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the BFT traversal (go left-to-right).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    if root is None:
        return json.dumps(None, indent=2)

    result = []
    queue = [root]  # Initialize the queue as a list with the root node.

    while queue:
        current_node = queue.pop(0)  # Dequeue the first node.
        result.append(current_node.key)

        if current_node.leftchild:
            queue.append(current_node.leftchild)  # Enqueue the left child.
        if current_node.rightchild:
            queue.append(current_node.rightchild)  # Enqueue the right child.

    return json.dumps(result, indent=2)
