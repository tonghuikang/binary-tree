import random
import math


class NodeKey():
    def __init__(self, value, name=None):
        self.name = name
        self.value = value

    def __lt__(self, other):
        return self.value < other.value or (self.value == other.value and self.name < other.name)

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name

    def __ne__(self, other):
        return self.value != other.value or self.name != other.name

    def __gt__(self, other):
        return self.value > other.value or (self.value == other.value and self.name > other.name)

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        return str(self.value) + " // " + str(self.name)


class Node():
    def __init__(self, value, name=None):
        self.key = NodeKey(value, name)
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0

    def __str__(self):
        if self.parent is None:
            parent_text = "None"
        else:
            parent_text = str(self.parent.key)

        if self.left_child is None:
            left_child_text = "None"
        else:
            left_child_text = str(self.left_child.key)

        if self.right_child is None:
            right_child_text = "None"
        else:
            right_child_text = str(self.right_child.key)
        return "K: " + str(self.key) + " H: " + str(self.height) + " P: " + parent_text + " L: " + left_child_text + " R: " + right_child_text

    def is_leaf(self):
        """ Return True if Leaf, False Otherwise
        """
        return self.height == 0

    def max_child_height(self):
        """ Return Height Of Tallest Child or -1 if No Children
        """
        if self.left_child and self.right_child:
            # two children
            return max(self.left_child.height, self.right_child.height)
        elif self.left_child is not None and self.right_child is None:
            # one child, on left
            return self.left_child.height
        elif self.left_child is None and self.right_child is not None:
            # one child, on right
            return self.right_child.height
        else:
            # no Children
            return -1

    def weigh(self):
        """ Return How Left or Right Sided the Tree Is
        Positive Number Means Left Side Heavy, Negative Number Means Right Side Heavy
        """
        if self.left_child is None:
            left_height = -1
        else:
            left_height = self.left_child.height

        if self.right_child is None:
            right_height = -1
        else:
            right_height = self.right_child.height

        balance = left_height - right_height
        return balance

    def rotate_right(self):
        # assign variables
        to_demote = self
        top = to_demote.parent
        to_promote = to_demote.right_child
        swapper = to_promote.left_child

        # swap children
        to_promote.left_child = to_demote
        to_demote.right_child = swapper

        # re-assign parents
        to_promote.parent = top
        to_demote.parent = to_promote
        if swapper is not None:
            swapper.parent = to_demote

        if top is not None:
            if top.right_child == to_demote:
                top.right_child = to_promote
            elif top.left_child == to_demote:
                top.left_child = to_promote
        return to_promote

    def rotate_left(self):
        # assign variables
        to_demote = self
        top = to_demote.parent
        to_promote = to_demote.left_child
        swapper = to_promote.right_child

        # swap children
        to_promote.right_child = to_demote
        to_demote.left_child = swapper

        # re-assign parents
        to_promote.parent = top
        to_demote.parent = to_promote
        if swapper is not None:
            swapper.parent = to_demote

        if top is not None:
            if top.right_child == to_demote:
                top.right_child = to_promote
            elif top.left_child == to_demote:
                top.left_child = to_promote
        return to_promote

    def max(self):
        """ Finds the largest descendant of this Node
        """
        node = self
        while node.right_child:
            node = node.right_child
        return node

    def min(self):
        """ Finds the smallest descendant of this Node
        """
        node = self
        while node.left_child:
            node = node.left_child
        return node

    def update_height(self):
        """ Updates Height of This Node and All Ancestor Nodes, As Necessary
        """
        node = self
        # changed = True
        while node is not None:
            # old_height = node.height
            node.height = node.max_child_height() + 1
            # changed = node.height != old_height
            node = node.parent

    def out(self):
        """ Return String Representing Tree From Current Node Down
        Only Works for Small Trees
        """
        start_node = self
        space_symbol = "*"
        spaces_count = 250
        out_string = ""
        initial_spaces_string = space_symbol * spaces_count + "\n"
        if start_node is None:
            return "AVLTree is empty"
        else:
            level = [start_node]
            while len([i for i in level if (not i is None)]) > 0:
                level_string = initial_spaces_string
                for i in xrange(len(level)):
                    j = (i + 1) * spaces_count / (len(level) + 1)
                    level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j + 1:]
                level_next = []
                for i in level:
                    level_next += ([i.left_child, i.right_child] if i else [None, None])
                level = level_next
                out_string += level_string
        return out_string


class AVLTree():
    """ Binary Search Tree
    """
    def __init__(self, *args):
        self.root = None  # root Node
        self.element_count = 0
        self.allow_duplicate_values = True
        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def __len__(self):
        return self.element_count

    def height(self):
        """ Return Max Height Of Tree
        """
        if self.root:
            return self.root.height
        else:
            return 0

    def balance(self, node=None):
        """ Perform balancing Operation
        """
        if node is None:
            node = self.root
        while node.weigh() < -1 or node.weigh() > 1:
            if node.weigh() < 0:
                # right side heavy
                if node.right_child.weigh() > 0:
                    # right-side left-side heavy
                    old_right_child = node.right_child
                    node.right_child.rotate_left()
                    old_right_child.update_height()
                # right-side right-side heavy
                new_node = node.rotate_right()
                if new_node.parent is None:
                    self.root = new_node
                node.update_height()
            else:
                # left side heavy
                if node.left_child.weigh() < 0:
                    # left-side right-side heavy
                    old_left_child = node.left_child
                    node.left_child.rotate_right()
                    old_left_child.update_height()
                # left-side left-side heavy
                new_node = node.rotate_left()
                if new_node.parent is None:
                    self.root = new_node
                node.update_height()

    def insert(self, value, name=None):
        if self.root is None:
            # If nothing in tree
            self.root = Node(value, name)
        else:
            if self.find(value, name) is None:
                # If key doesn't exist in tree
                self.element_count += 1
                self.add_as_child(self.root, Node(value, name))

    def add_as_child(self, parent_node, child_node):
        node_to_rebalance = None
        if child_node.key < parent_node.key:
            # should go on left
            if parent_node.left_child is None:
                # can add to this node
                parent_node.left_child = child_node
                child_node.parent = parent_node
                child_node.update_height()

                node = parent_node
                while node:
                    if node.weigh() not in [-1, 0, 1]:
                        node_to_rebalance = node
                        break
                    node = node.parent
            else:
                self.add_as_child(parent_node.left_child, child_node)
        else:
            # should go on right
            if parent_node.right_child is None:
                # can add to this node
                parent_node.right_child = child_node
                child_node.parent = parent_node
                child_node.update_height()

                node = parent_node
                while node:
                    if node.weigh() not in [-1, 0, 1]:
                        node_to_rebalance = node
                        break
                    node = node.parent
            else:
                self.add_as_child(parent_node.right_child, child_node)

        if node_to_rebalance is not None:
            self.balance(node_to_rebalance)

    def inorder_non_recursive(self):
        node = self.root
        retlst = []
        while node.left_child:
            node = node.left_child
        while node:
            if node.key.name is not None:
                retlst.append([node.key.value, node.key.name])
            else:
                retlst.append(node.key.value)
            if node.right_child:
                node = node.right_child
                while node.left_child:
                    node = node.left_child
            else:
                while node.parent and (node == node.parent.right_child):
                    node = node.parent
                node = node.parent
        return retlst

    def preorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        if node.left_child:
            retlst = self.preorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.preorder(node.right_child, retlst)
        return retlst

    def inorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.inorder(node.left_child, retlst)
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        if node.right_child:
            retlst = self.inorder(node.right_child, retlst)
        return retlst

    def postorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.postorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.postorder(node.right_child, retlst)
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        return retlst

    def as_list(self, pre_in_post):
        if not self.root:
            return []
        if pre_in_post == 0:
            return self.preorder(self.root)
        elif pre_in_post == 1:
            return self.inorder(self.root)
        elif pre_in_post == 2:
            return self.postorder(self.root)
        elif pre_in_post == 3:
            return self.inorder_non_recursive()

    def find(self, value, name=None):
        return self.find_in_subtree(self.root, NodeKey(value, name))

    def find_in_subtree(self, node, node_key):
        if node is None:
            return None  # key not found
        if node_key < node.key:
            return self.find_in_subtree(node.left_child, node_key)
        elif node_key > node.key:
            return self.find_in_subtree(node.right_child, node_key)
        else:  # key is equal to node key
            return node

    def remove(self, key):
        # first find
        node = self.find(key)

        if not node is None:
            self.element_count -= 1

            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.

            if node.is_leaf():
                self.remove_leaf(node)
            elif (bool(node.left_child)) ^ (bool(node.right_child)):
                self.remove_branch(node)
            else:
                assert node.left_child and node.right_child
                self.swap_with_successor_and_remove(node)

    def remove_leaf(self, node):
        parent = node.parent
        if parent:
            if parent.left_child == node:
                parent.left_child = None
            else:
                assert (parent.right_child == node)
                parent.right_child = None
            parent.update_height()
        else:
            self.root = None
        del node
        # rebalance
        node = parent
        while node:
            if not node.weigh() in [-1, 0, 1]:
                self.balance(node)
            node = node.parent

    def remove_branch(self, node):
        parent = node.parent
        if parent:
            if parent.left_child == node:
                parent.left_child = node.right_child or node.left_child
            else:
                assert (parent.right_child == node)
                parent.right_child = node.right_child or node.left_child
            if node.left_child:
                node.left_child.parent = parent
            else:
                assert node.right_child
                node.right_child.parent = parent
            parent.update_height()
        del node
        # rebalance
        node = parent
        while node:
            if not node.weigh() in [-1, 0, 1]:
                self.balance(node)
            node = node.parent

    def swap_with_successor_and_remove(self, node):
        successor = node.right_child.min()
        self.swap_nodes(node, successor)
        assert (node.left_child is None)
        if node.height == 0:
            self.remove_leaf(node)
        else:
            self.remove_branch(node)

    def swap_nodes(self, node_1, node_2):
        assert (node_1.height > node_2.height)
        parent_1 = node_1.parent
        left_child_1 = node_1.left_child
        right_child_1 = node_1.right_child
        parent_2 = node_2.parent
        assert (not parent_2 is None)
        assert (parent_2.left_child == node_2 or parent_2 == node_1)
        left_child_2 = node_2.left_child
        assert (left_child_2 is None)
        right_child_2 = node_2.right_child

        # swap heights
        tmp = node_1.height
        node_1.height = node_2.height
        node_2.height = tmp

        if parent_1:
            if parent_1.left_child == node_1:
                parent_1.left_child = node_2
            else:
                assert (parent_1.right_child == node_1)
                parent_1.right_child = node_2
            node_2.parent = parent_1
        else:
            self.root = node_2
            node_2.parent = None

        node_2.left_child = left_child_1
        left_child_1.parent = node_2
        node_1.left_child = left_child_2  # None
        node_1.right_child = right_child_2
        if right_child_2:
            right_child_2.parent = node_1
        if not (parent_2 == node_1):
            node_2.right_child = right_child_1
            right_child_1.parent = node_2

            parent_2.left_child = node_1
            node_1.parent = parent_2
        else:
            node_2.right_child = node_1
            node_1.parent = node_2

            # use for debug only and only with small trees

    def out(self, start_node=None):
        if start_node is None:
            start_node = self.root
        return start_node.out()

    def sanity_check(self, *args):
        if len(args) == 0:
            node = self.root
        else:
            node = args[0]
        if (node is None) or (node.is_leaf() and node.parent is None):
            # trivial - no sanity check needed, as either the tree is empty or there is only one node in the tree
            pass
        else:
            if node.height != node.max_child_height() + 1:
                raise Exception("Invalid height for node " + str(node) + ": " + str(node.height) + " instead of " + str(node.max_child_height() + 1) + "!")

            bal_factor = node.weigh()
            #Test the balance factor
            if not (-1 <= bal_factor <= 1):
                raise Exception("Balance factor for node " + str(node) + " is " + str(bal_factor) + "!")
                #Make sure we have no circular references
            if not (node.left_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.left_child is node!")
            if not (node.right_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.right_child is node!")

            if node.left_child:
                if not (node.left_child.parent == node):
                    raise Exception("Left child of node " + str(node) + " doesn't know who his father is!")
                if not (node.left_child.key <= node.key):
                    raise Exception("Key of left child of node " + str(node) + " is greater than key of his parent!")
                self.sanity_check(node.left_child)

            if node.right_child:
                if not (node.right_child.parent == node):
                    raise Exception("Right child of node " + str(node) + " doesn't know who his father is!")
                if not (node.right_child.key >= node.key):
                    raise Exception("Key of right child of node " + str(node) + " is less than key of his parent!")
                self.sanity_check(node.right_child)


def test():
    def random_data_generator(max_r):
        for i in xrange(max_r):
            yield random.randint(0, max_r)

    print("check empty tree creation")
    a = AVLTree()
    print("about to do sanity check 1")
    a.sanity_check()

    print("check not empty tree creation")
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    seq_copy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #random.shuffle(seq)
    b = AVLTree(seq)
    print("about to do sanity check 2")
    b.sanity_check()

    print("check that inorder traversal on an AVL tree (and on a binary search tree in the whole) will return values from the underlying set in order")
    assert (b.as_list(3) == b.as_list(1) == seq_copy)

    print("check that node deletion works")
    c = AVLTree(random_data_generator(10000))
    before_deletion = c.element_count
    for i in random_data_generator(1000):
        c.remove(i)
    after_deletion = c.element_count
    c.sanity_check()
    assert (before_deletion >= after_deletion)

    print("check that an AVL tree's height is strictly less than 1.44*log2(N+2)-1 (there N is number of elements)")
    assert (c.height() < 1.44 * math.log(after_deletion + 2, 2) - 1)
