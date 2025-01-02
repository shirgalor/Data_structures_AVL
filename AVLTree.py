#id1:
#name1:
#username1:
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
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left : AVLNode = None
        self.right : AVLNode = None
        self.parent : AVLNode = None
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
        self.size = 0

    def _update_min_max(self):
        self.min_pointer = self._find_min()
        self.max_pointer = self._find_max()
    
     
    def _add_virtual_nodes(self, node):
        if node is None:
            return
        if node.left is None:
            node.left = AVLNode()
            node.left.parent = node
        if node.right is None:
            node.right = AVLNode()
            node.right.parent = node
        return
    
   
    def _rotate_left(self, node:AVLNode):
        if not node or not node.right:
            return node  
        
        new_root = node.right
        node.right = new_root.left
        
        if new_root.left:
            new_root.left.parent = node 
        
        new_root.left = node
        new_root.parent = node.parent

        if new_root.parent is not None:
            if new_root.parent.key < new_root.key:
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
        
        new_root = node.left
        node.left = new_root.right
        
        if new_root.right:
            new_root.right.parent = node  
        
        new_root.right = node
        new_root.parent = node.parent

        if new_root.parent is not None:
            if new_root.parent.key < new_root.key:
                new_root.parent.right = new_root
            else:
                new_root.parent.left = new_root
        
        node.parent = new_root

        node.update_height()
        new_root.update_height()

        if self.root.key == node.key:
            self.root = new_root

        return new_root
    
    def _find_min(self):
        node = self.root
        while node.height != -1:
            node = node.left
        return node.parent
    
    def _find_max(self):
        node = self.root
        while node.height != -1:
            node = node.right
        return node.parent
    
    


    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        current_node = self.root
        edges = 0
        while current_node is not None:
            if current_node.key == key:
                return current_node, edges + 1
            elif current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
            edges += 1
        return None, edges + 1

 

    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        current_node = self.max_pointer
        edge = -1
        while current_node is not None:
            if current_node.key == key:
                return current_node, edge + 1
            elif current_node.key > key:
                current_node = current_node.parent
            elif current_node.key < key: 
                new_tree = AVLTree(current_node)
                found_node, path =  new_tree.search(key)
                if found_node is not None:
                    return found_node, path + edge + 1
                break
            edge += 1
        return None, -1
    


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
        new_node, edges, promote = self._insert(self.root, key, val)
        if self.root is None:
            self.root = new_node

        self._update_min_max()
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
        self.size += 1
        self._update_min_max()
        return None, -1, -1


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        self.size -= 1
        self._delete(node)
        self._update_min_max()

    
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
        return


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
        return None, None

    
    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        def avl_to_array_helper(node):
            if node is None or node.height == -1:
                return []
            return avl_to_array_helper(node.left) + [(node.key, node.value)] + avl_to_array_helper(node.right)
        return avl_to_array_helper(self.root)
        


    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        return self.max_pointer
    

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self.size


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root
    

    def _successor(self, node:AVLNode):
        if node.right.height != -1:
            node = node.right
            while node.left.height != -1:
                node = node.left
            return node
        else:
            while node.parent is not None and node.parent.right == node:
                node = node.parent
            return node.parent
        
    def _predecessor(self, node:AVLNode):
        if node.left.height != -1:
            node = node.left
            while node.right.height != -1:
                node = node.right
            return node
        else:
            while node.parent is not None and node.parent.left == node:
                node = node.parent
            return node.parent
    

    def _insert(self, root: AVLNode, key, val):
        self.size += 1

        # create new node
        new_node = AVLNode(key, val)
        self._add_virtual_nodes(new_node)
        new_node.height = 0

        # tree is empty
        if root is None:
            root = new_node
            return root, 0, 0
        
        # find insertion point
        edges = 0
        current_node = root
        while current_node.is_real_node():
            if current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
            edges += 1

        current_node = current_node.parent # go back to the last real node
        
        # insert new node
        if current_node.key < key:
            current_node.right = new_node
        else:
            current_node.left = new_node

        new_node.parent = current_node

        # rebalance
        promote = 0
        current_node.update_height()
        balance = current_node.get_balance()
        while abs(balance) < 2:
            promote += 1
            if current_node.parent is None:
                break
            current_node = current_node.parent
            current_node.update_height()
            balance = current_node.get_balance()

        self._rebalance(current_node)

        return new_node, edges, promote
    
    def _delete_leaf(self, node:AVLNode):
        virtual_node = AVLNode()
    
        if node.parent is None:
            self.root = None
        elif node.key < node.parent.key: # left child
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
        
        if node.left.is_real_node():
            replacement = self._predecessor(node)
        elif node.right.is_real_node():
            replacement = self._successor(node)        

        if replacement:
            if node.parent: # node is somewhere in the tree
                if replacement.key < node.parent.key: # replacement should be left child
                    node.parent.left = replacement
                else:
                    node.parent.right = replacement
                replacement.parent = node.parent
                rebalance_node = replacement.parent
            else: # node is the root
                if replacement.key < replacement.parent.key:
                    replacement.parent.left = AVLNode()
                else:
                    replacement.parent.right = AVLNode()
                replacement.parent = None
                replacement.left = node.left
                node.left.parent = replacement
                replacement.right = node.right
                node.right.parent = replacement
                self.root = replacement
                rebalance_node = replacement
        else: # node is a leaf
            self._delete_leaf(node)
        
        self._rebalance_tree(rebalance_node)

    def _rebalance(self, node:AVLNode):
        """Rebalances the AVL tree starting at node, returns the new root of the subtree."""
        if node is None or not node.is_real_node():
            return node
        balance = node.get_balance()
        if abs(balance) <= 1:
            return node
        
        if balance == 2: # left heavy
            if node.left.get_balance() == -1: # double rotation
                node.left = self._rotate_left(node.left)
            node = self._rotate_right(node)

        elif balance == -2: # right heavy
            if node.right.get_balance() == 1: # double rotation
                node.right = self._rotate_right(node.right)
            node = self._rotate_left(node) 

        return node

    def _rebalance_tree(self, node:AVLNode):
        """Rebalances the AVL tree starting at node, returns the new root."""
        current_node = node

        while current_node is not None:
            current_node.left = self._rebalance(current_node.left)
            current_node.right = self._rebalance(current_node.right)
            current_node.update_height()
            current_node = current_node.parent

        self.root = self._rebalance(self.root)
        self.root.parent = None

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
