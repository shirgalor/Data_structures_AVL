#id1: 322722364
#name1: Maya Gal - Yam
#username1: mayagalyam
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key=None, value=None, parent=None):
        self.key = key
        self.value = value
        self.left : AVLNode = None
        self.right : AVLNode = None
        self.parent : AVLNode = parent
        self.height = -1
        

    """returns whether self is not a virtual node 
    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
         return self.height != -1
    
    def update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)

    def get_balance(self):
        return self.left.height - self.right.height

"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root: AVLNode = None
        self._min = None
        self._max = None
        self._size = 0

    def _update_min_max(self, new_node=None):

        if self.root is None:
            self._min = None
            self._max = None
            return
        
        if new_node:
            if new_node.key > self._max.key:
                self._max = new_node
            elif new_node.key < self._min.key:
                self._min = new_node
        else:
            # Find the minimum and maximum nodes
            self._min = self._find_min() # O(log n)
            self._max = self._find_max() # O(log n)
     
    def _add_virtual_nodes(self, node):
        if node is None:
            return
        if node.left is None:
            node.left = AVLNode(parent=node)
        if node.right is None:
            node.right = AVLNode(parent=node)
        return  
   
    def _rotate_left(self, node:AVLNode):
        if not node or not node.right: # Invalid node
            return node
        
        # Rotate the tree to the left
        new_root = node.right 
        node.right = new_root.left

        if new_root.left:
            new_root.left.parent = node 

        new_root.left = node
        new_root.parent = node.parent

        # Reparent new_root
        if new_root.parent is not None:
            if new_root.parent.key < new_root.key: # new_root is right child
                new_root.parent.right = new_root
            else:
                new_root.parent.left = new_root

        node.parent = new_root

        node.update_height()
        new_root.update_height()

        if self.root.key == node.key:
            self.root = new_root

        return new_root
    
    def _rotate_right(self, node:AVLNode):
        if not node or not node.left:
            return node  

        # Rotate the tree to the right
        new_root = node.left
        node.left = new_root.right
        
        if new_root.right:
            new_root.right.parent = node  
        
        new_root.right = node
        new_root.parent = node.parent

        # Reparent new_root
        if new_root.parent is not None:
            if new_root.parent.key < new_root.key: # new_root is right child
                new_root.parent.right = new_root
            else:
                new_root.parent.left = new_root
        
        node.parent = new_root

        node.update_height()
        new_root.update_height()

        if self.root.key == node.key:
            self.root = new_root

        return new_root
    
    def _find_min(self, start_node=None):
        node = start_node or self.root
        while node.is_real_node(): # O(start_node.height) - O(log n) if starting from the root
            node = node.left
        return node.parent
    
    def _find_max(self, start_node=None):
        node = start_node or self.root
        while node.is_real_node(): # O(start_node.height) - O(log n) if starting from the root
            node = node.right
        return node.parent

    def _search(self, key, root: AVLNode):
        edges = 0
        current_node = root

        while current_node.is_real_node(): # O(h) = O(log n)
            if current_node.key == key: # found
                return current_node, edges + 1
            elif current_node.key < key:  # go right
                current_node = current_node.right 
            else:
                current_node = current_node.left
            edges += 1
        return current_node, edges + 1
           
    def _successor(self, node:AVLNode):
        if node.right.height != -1:
            node = node.right
            while node.left.height != -1: # O(node.height) = O(log n)
                node = node.left
            return node
        else:
            while node.parent is not None and node.parent.right == node: # O(log n)
                node = node.parent
            return node.parent
    
    def _insert(self, root: AVLNode, key, val):
        # Create new node
        new_node = AVLNode(key, val)
        self._add_virtual_nodes(new_node)
        new_node.height = 0

        # Tree is empty
        if root is None:
            root = new_node
            return root, 0, 0
        
        # Find insertion point
        current_node, edges = self._search(key, root) # O(log n)
        current_node = current_node.parent # Go back to the last real node
        
        # Insert new node
        if current_node.key < key:
            current_node.right = new_node
        else:
            current_node.left = new_node

        new_node.parent = current_node

        # Rebalance
        promote = 0
        current_node.update_height()
        balance = current_node.get_balance()
        while abs(balance) < 2: # O(log n)
            promote += 1
            if current_node.parent is None:
                break
            current_node = current_node.parent
            current_node.update_height()
            balance = current_node.get_balance()

        self._rebalance(current_node) # O(1)

        return new_node, edges, promote
    
    def _delete_leaf(self, node:AVLNode):
        """Deletes a leaf node from the AVL tree and replaces it with a virtual node."""
        virtual_node = AVLNode(parent=node.parent)
    
        if node.parent is None: # Tree has only one node
            self.root = None
        elif node.key < node.parent.key: # Node is left child
            node.parent.left = virtual_node
            node.parent = None
        else:
            node.parent.right = virtual_node
            node.parent = None

    def _delete(self, node:AVLNode):
        replacement = None
        rebalance_node = node.parent

        has_left = node.left.is_real_node()
        has_right = node.right.is_real_node()
        
        if not (has_left or has_right): # node is a leaf
            self._delete_leaf(node)
        elif has_left and not has_right: # unary node (with left child)
            if node.parent is None: # node is the root
                self.root = node.left
                node.left.parent = None
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
        elif has_right and not has_left: # unary node (with right child)
            if node.parent is None: # node is the root
                self.root = node.right
                node.right.parent = None
            else:
                node.parent.left = node.right
                node.right.parent = node.parent
        else: # node has two children
            replacement = self._successor(node)

            if replacement.parent.key != node.key:
                # remove replacement from its current position
                replacement.parent.left = replacement.right
                replacement.right.parent = replacement.parent

            # swap replacement with node
            if node.parent: # node is somewhere in the tree (not the root)
                if replacement.key < node.parent.key: # replacement should be left child
                    node.parent.left = replacement
                else:
                    node.parent.right = replacement
                replacement.parent = node.parent
                rebalance_node = replacement.parent
            else: # node is the root
                if replacement.key < replacement.parent.key:
                    replacement.parent.left = AVLNode(parent=replacement.parent)
                else:
                    replacement.parent.right = AVLNode(parent=replacement.parent)
                replacement.parent = None
                self.root = replacement
                rebalance_node = replacement
        
            # update children of replacement
            replacement.left = node.left
            node.left.parent = replacement
            replacement.right = node.right
            node.right.parent = replacement

        
        # Rebalance
        self._rebalance_tree(rebalance_node) # O(log n)
        self.root = self._rebalance(self.root) # O(1)
        if self.root:
            self.root.parent = None

    def _rebalance(self, node:AVLNode):
        """Rebalances the AVL tree starting at node, returns the new root of the subtree."""
        if node is None or not node.is_real_node():
            return node
        balance = node.get_balance()
        if abs(balance) <= 1:
            return node
        
        if balance == 2: # left heavy
            if node.left.get_balance() == -1: # double rotation
                node.left = self._rotate_left(node.left) # O(1)
            node = self._rotate_right(node) # O(1)

        elif balance == -2: # right heavy
            if node.right.get_balance() == 1: # double rotation
                node.right = self._rotate_right(node.right) # O(1)
            node = self._rotate_left(node) # O(1)

        return node

    def _rebalance_tree(self, node:AVLNode):
        """Rebalances the AVL tree starting at node, returns the new root."""
        current_node = node
        last_node = None

        while current_node is not None: # O(log n)
            current_node.left = self._rebalance(current_node.left) # O(1)
            current_node.right = self._rebalance(current_node.right) # O(1)
            current_node.update_height()
            last_node = current_node
            current_node = current_node.parent

        return last_node
    
    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        if self.root is None: # Empty tree
            return None, -1
        node, edges = self._search(key, self.root) # O(log n)
        if node.is_real_node():
            return node, edges
        return None, edges # Node not found

    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        current_node = self._max
        edge = -1

        # Traverse up the tree starting at max
        while current_node is not None: # O(new_node.height)
            if current_node.key == key: # Found
                return current_node, edge + 1
            elif current_node.key > key: # Move up
                current_node = current_node.parent 
            elif current_node.key < key: 
                found_node, path =  self._search(root=current_node, key=key) # Search the subtree - O(new_node.height)
                if found_node is not None:
                    return found_node, path + edge
                break # Total time complexity: O(new_node.height)
            edge += 1

        return None, -1 # Node not found
    
    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
        self._size += 1
        new_node, edges, promote = self._insert(self.root, key, val) # O(log n)
        if self.root is None:
            self.root = new_node

        self._update_min_max() # O(log n)
        return new_node, edges, promote

    """inserts a new node into the dictionary with corresponding key and value, starting at the max
    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def finger_insert(self, key, val):
        if self._max is None:
            return self.insert(key, val) # Empty tree - O(1)
        else:
            self._size += 1
            current_node = self._max

            search_edges = 0
            while current_node.parent is not None: # O(new_node.height)
                if current_node.key > key:
                    current_node = current_node.parent
                elif current_node.key < key: 
                    break
                search_edges += 1
            
            new_node, insert_edges, promote = self._insert(root=current_node, key=key, val=val) # O(current_node.height)
            self._update_min_max(new_node=new_node) # O(1)

            return new_node, search_edges + insert_edges, promote

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        self._size -= 1
        self._delete(node) # O(log n)
        self._update_min_max() # O(log n)

    
    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """
    def join(self, tree2, key, val):
        new_node = AVLNode(key, val)

        # Update the size of the resulting tree if both trees are non-empty
        if self._size and tree2.size():
            self._size += 1 + tree2.size()

        # Case 1: Both trees are empty
        if self.root is None and (tree2 is None or tree2.root is None):
            # Insert the new node as the root since both trees are empty
            self.root, _, _  = self.insert(key, val) # O(1)
            return
        
        # case 2: one tree is empty 
        if self.root is None or (tree2 is None or tree2.root is None):
            non_empty_tree = self if self.root else tree2
            self.root = non_empty_tree.root
            self._size = non_empty_tree.size()
            self._update_min_max() # O(log n)
            self.insert(key, val) # O(log n)
            return

        # Case 3: Both trees are non-empty
        # Ensure self is the lower tree 
        if self.root.height > tree2.root.height:
            self, tree2 = tree2, self

        b_parent = None
        b = tree2.root
        target_height = self.root.height # Target height to attach `self` to `tree2`

        # Attach `self` to the left or right of the new node based on the key comparison
        if self.root.key < key:
            while b.height > target_height:
                b_parent = b
                b = b.left
            # Attach `self` as the left child of the new node
            new_node.left = self.root
            self.root.parent = new_node
            # Attach the subtree from `tree2` as the right child of the new node
            new_node.right = b

        elif self.root.key > key:
            # Traverse `tree2` to find the appropriate position based on height
            while b.height > target_height:
                b_parent = b
                b = b.right
            # Attach `self` as the right child of the new node
            self.root.parent = new_node
            new_node.right = self.root
            new_node.left = b

        # Update the parent's reference to point to the new node
        if b_parent:
            if b_parent.left == b:
                b_parent.left = new_node
            else:
                b_parent.right = new_node
            b_parent.update_height()
      
        # Update parent pointers and heights for the new node
        new_node.parent = b_parent
        b.parent = new_node
        if new_node:
            new_node.update_height()
        if new_node.parent:
            new_node.parent.update_height()
        tree1 = AVLTree()
        tree1.root = new_node

        # Rebalance the tree starting from the new node
        self.root = self._rebalance_tree(new_node)  # O(log n)
        self._update_min_max() # O(log n)
    

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node):
        # Create two empty trees
        tree1 = AVLTree() 
        tree2 = AVLTree() 

        # If the given node is None, return empty trees
        if node is None:
            return None, None
        
        # Detach the left and right subtree of the node and
        #  ssign it to tree2 and tree1 respectively
        if node.left.is_real_node():
            tree2.root = node.left
            node.left.parent = None # Detach

        if node.right.is_real_node():
            tree1.root = node.right
            node.right.parent = None # Detach   
        
        # Traverse up the tree to split the remaining structure
        while node.parent is not None:
            temp_tree = AVLTree()
            if node.parent.left == node:
                # If the current node is the left child, detach the parent's right subtree
                temp_tree.root = node.parent.right
                if temp_tree.root.is_real_node():
                    node.parent.right.parent = None  # Detach the subtree
                     # Join the detached subtree and the parent to tree1
                    tree1.join(temp_tree, node.parent.key, node.parent.value)
                
            else:
                # If the current node is the right child, detach the parent's left subtree
                temp_tree.root = node.parent.left
                if node.parent.left.is_real_node():
                    node.parent.left.parent = None  # Detach the subtree
                    # Join the detached subtree and the parent to tree1
                    tree2.join(temp_tree, node.parent.key, node.parent.value)
            node = node.parent   # Move up to the parent node

        return tree2, tree1

    
    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        """
        Recursive helper function to traverse the tree in in-order fashion.
        @type node: AVLNode
        @param node: The current node being processed.
        @rtype: list
        @returns: A list of (key, value) tuples from the subtree rooted at `node`.
        """
        def avl_to_array_helper(node):
            # If the node is None or a virtual node, return an empty list
            if node is None or node.height == -1:
                return []
            # Traverse the left subtree, process the current node, then the right subtree
            return avl_to_array_helper(node.left) + [(node.key, node.value)] + avl_to_array_helper(node.right) # O(k/2) + O(k/2) = O(k) for tree of size k
        return avl_to_array_helper(self.root) # O(n)
        
    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        return self._max
    
    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self._size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

    def print_tree_with_heights(self):
        if not self.root:
            print('<empty tree>')
        else:
            content = []
            self._print_tree_with_heights(self.root, content, 0, 'H')
            print('\n'.join(content))

    def _print_tree_with_heights(self, node, content, level, label):
        if node is not None:
            self._print_tree_with_heights(node.right, content, level + 1, 'R')
            key = node.key if node.is_real_node() else 'V'
            content.append(' ' * 4 * level + f'{label}: ' + f'<{key}:{node.height}>')
            self._print_tree_with_heights(node.left, content, level + 1, 'L')

    """
    Helper function to print the AVL tree. Taken from CS1001 course, created by a previus student.
    """
    def _repr_(self):  
        def printree(root):
            if root is None:
                return ["#"]
            if not root.is_real_node():
                return ["#"]
            root_key = str(root.key)
            root_height = str(root.height)
            left, right = printree(root.left), printree(root.right)
            lwid = len(left[-1])
            rwid = len(right[-1])
            rootwid = len(root_key)+len(root_height)+2
            result = [(lwid) * " " + root_key +":"+root_height+ (rwid) * " "]
            ls = len(left[0].rstrip())
            rs = len(right[0]) - len(right[0].lstrip())
            result.append(ls * " " + (lwid - ls) * "" + "/" + rootwid * " " + "\\" + rs * "" + (rwid - rs) * " ")
            for i in range(max(len(left), len(right))):
                row = ""
                if i < len(left):
                    row += left[i]
                else:
                    row += lwid * " "
                    
                row += (rootwid + 2) * " "
                if i < len(right):
                    row += right[i]
                else:
                    row += rwid * " "
                result.append(row)
            return result
        return '\n'.join(printree(self.root))
    
    def __repr__(self):
        return self._repr_()
    
    def __str__(self):
        return self._repr_()
