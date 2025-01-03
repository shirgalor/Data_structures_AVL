import unittest
from AVLTree import AVLNode, AVLTree

class TestAVLTree(unittest.TestCase):

    def setUp(self):
        """Set up an empty AVL tree before each test."""
        self.tree = AVLTree()

    def test_insert_and_search(self):
        """Test insertion and search functionality."""
        # Insert nodes
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(30, "C")

        # Search for existing keys
        node, edges = self.tree.search(10)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 10)
        self.assertEqual(node.value, "A")
        
        # Search for a non-existing key
        node, edges = self.tree.search(40)
        self.assertIsNone(node)

    def test_edges_consistency(self):
        """Test edges returned from search on a non-existent key match edges from inserting the key."""
        self.tree.insert(10, "")
        self.tree.insert(5, "")
        self.tree.insert(15, "")
        _, search_edges = self.tree.search(50)
        _, _, insert_edges = self.tree.insert(50, "Z")
        self.assertEqual(search_edges, insert_edges)

    def test_finger_insert_and_search(self):
        """Test finger insertion and search functionality."""
        # Finger insert nodes
        self.tree.finger_insert(10, "A")
        self.tree.finger_insert(20, "B")
        self.tree.finger_insert(30, "C")

        # Finger search for existing keys
        node, edges = self.tree.finger_search(20)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 20)
        self.assertEqual(node.value, "B")

    def test_delete_cases(self):
        """Test different cases for deletion."""
        # Insert nodes
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(30, "C")

        # Delete root
        root = self.tree.get_root()
        self.tree.delete(root)
        self.assertIsNone(self.tree.search(20)[0])
        self.assertEqual(self.tree.get_root().height, 1)

        # Delete middle node
        self.tree.insert(25, "D")
        self.tree.insert(15, "E")
        node, _ = self.tree.search(10)
        self.tree.delete(node)
        self.assertIsNone(self.tree.search(10)[0])

        # Delete leaf
        node, _ = self.tree.search(30)
        self.tree.delete(node)
        self.assertIsNone(self.tree.search(30)[0])

    def test_max_cases(self):
        """Test different cases for max retrieval."""
        # Insert nodes
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(30, "C")

        # Find max
        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 30)

        # Delete max and find new max
        self.tree.delete(max_node)
        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 20)

        # Insert new max and verify
        self.tree.insert(40, "D")
        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 40)

    def test_sequences_of_insert_and_delete(self):
        """Test sequences of insertions and deletions."""
        for i in range(1, 11):
            self.tree.insert(i, str(i))
        for i in range(1, 11):
            self.tree.delete(self.tree.search(i)[0])
        self.assertEqual(self.tree.size(), 0)

    # def test_inserting_and_deleting_after_join(self):
    #     """Test inserting and deleting after a join operation."""
    #     tree1 = AVLTree()
    #     tree2 = AVLTree()
    #     tree1.insert(10, "A")
    #     tree2.insert(30, "B")
    #     tree1.join(tree2, 20, "C")

    #     self.tree = tree1
    #     self.tree.insert(25, "D")
    #     self.tree.delete(self.tree.search(20)[0])
    #     self.assertEqual(self.tree.size(), 3)

    # def test_virtual_nodes_after_delete_or_join(self):
    #     """Check all lowest nodes are virtual nodes after delete or join."""
    #     self.tree.insert(10, "A")
    #     self.tree.insert(20, "B")
    #     self.tree.insert(30, "C")

    #     self.tree.delete(self.tree.search(20)[0])
        
    #     def check_virtual(node):
    #         if node is None:
    #             return True
    #         if not node.is_real_node():
    #             return True
    #         return check_virtual(node.left) and check_virtual(node.right)

    #     self.assertTrue(check_virtual(self.tree.get_root()))

    def test_promote_returns(self):
        """Test promote returns for insert and finger_insert."""
        _, _, promotes = self.tree.insert(3, "A")
        self.assertEqual(promotes, 0)
        _, _, promotes = self.tree.insert(2, "B")
        self.assertEqual(promotes, 1)
        _, _, promotes = self.tree.insert(1, "C")
        self.assertEqual(promotes, 1)
        _, _, promotes = self.tree.finger_insert(20, "")
        self.assertEqual(promotes, 2)

    # def test_split(self):
    #     """Test splitting the tree at a given node."""
    #     # Insert nodes
    #     self.tree.insert(10, "A")
    #     self.tree.insert(20, "B")
    #     self.tree.insert(30, "C")

    #     # Split at the root
    #     root = self.tree.get_root()
    #     left_tree, right_tree = self.tree.split(root)
        
    #     self.assertEqual(left_tree.size(), 0)  # Left subtree should be empty
    #     self.assertEqual(right_tree.size(), 2)  # Right subtree should contain two nodes

    # def test_join(self):
    #     """Test joining two AVL trees."""
    #     tree1 = AVLTree()
    #     tree2 = AVLTree()

    #     # Insert nodes into separate trees
    #     tree1.insert(10, "A")
    #     tree2.insert(30, "B")

    #     # Join the trees with a middle key
    #     tree1.join(tree2, 20, "C")

    #     # Check the size of the resulting tree
    #     self.assertEqual(tree1.size(), 3)
    #     self.assertEqual(tree1.search(20)[0].value, "C")

    def test_avl_to_array(self):
        """Test conversion of the AVL tree to an array."""
        # Insert nodes
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(30, "C")

        # Convert to array
        arr = self.tree.avl_to_array()
        self.assertEqual(arr, [(10, "A"), (20, "B"), (30, "C")])

    def test_max_node(self):
        """Test finding the node with the maximum key."""
        # Insert nodes
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(30, "C")

        # Find the max node
        max_node = self.tree.max_node()
        self.assertIsNotNone(max_node)
        self.assertEqual(max_node.key, 30)

    def test_size(self):
        """Test the size of the AVL tree."""
        self.assertEqual(self.tree.size(), 0)  # Empty tree

        self.tree.insert(10, "A")
        self.assertEqual(self.tree.size(), 1)

        self.tree.insert(20, "B")
        self.assertEqual(self.tree.size(), 2)

    def test_get_root(self):
        """Test retrieving the root of the AVL tree."""
        self.assertIsNone(self.tree.get_root())  # Empty tree

        self.tree.insert(10, "A")
        root = self.tree.get_root()
        self.assertIsNotNone(root)
        self.assertEqual(root.key, 10)

        # Delete root and check
        self.tree.delete(root)
        self.assertIsNone(self.tree.get_root())

if __name__ == "__main__":
    unittest.main()
