Self-Balancing Binary Tree
=============

Python [binary tree] module that is [self-balancing] and uses [AVL trees].

What Problem This Solves
------------------------
* Small space,  Ave: O(n), Max: O(n)
* Fast search,  Ave: O(log n), Max: O(log n)
* Fast insert,  Ave: O(log n), Max: O(log n)
* Fast delete,  Ave: O(log n), Max: O(log n)
* Objects with duplicate values may be added

How This Solves It
------------------

Usage
-----
New tree

`tree = AVLTree()`

Insert Entity into the tree

`tree.insert(5, "optional unique ID")`

[self-balancing]: https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree
[binary tree]: https://en.wikipedia.org/wiki/Binary_tree
[AVL trees]: http://en.wikipedia.org/wiki/AVL_tree
