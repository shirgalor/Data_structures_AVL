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
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
         return self.height != -1
    
    def get_height(self):
        return self.height 
    
    def update_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))




"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root = None
        self.min_pointer = None
        self.max_pointer = None
        self.size = 0

    """
    sheer's helper functions
    """
    def update_min_max(self, new_node):
            #Update the min and max pointers of the AVL tree.
            if self.min_pointer is None or new_node.key < self.min_pointer.key:
                self.min_pointer = new_node
            if self.max_pointer is None or new_node.key > self.max_pointer.key:
                self.max_pointer = new_node
    
    def get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right)
    
    def get_height(self, node):
        if node is None or not node.is_real_node():
            return -1
        return node.height
    
    def add_virtual_nodes(self, node):
        if node is None:
            return
        if node.left is None:
            node.left = AVLNode()
        if node.right is None:
            node.right = AVLNode()
        return
    
   
    def rotate_left(self,node):
        if not node or not node.right:
            return node  
        
        new_root = node.right
        node.right = new_root.left
        
        if new_root.left:
            new_root.left.parent = node 
        
        new_root.left = node
        new_root.parent = node.parent
        node.parent = new_root

        node.update_height(node)
        new_root.update_height(node)

        return new_root
    
    def rotate_right(self,node):
        if not node or not node.left:
            return node  
        
        new_root = node.left
        node.left = new_root.right
        
        if new_root.right:
            new_root.right.parent = node  
        
        new_root.right = node
        new_root.parent = node.parent
        node.parent = new_root

        node.update_height()
        new_root.update_height()

        return new_root


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
                return current_node, edges 
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
        self.size += 1
        self.update_min_max(AVLNode(key, val))
        return None, -1, -1


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
        self.update_min_max(AVLNode(key, val))
        return None, -1, -1


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        self.size -= 1
        # Update the min and max pointers of the AVL tree.
        return	

    
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
