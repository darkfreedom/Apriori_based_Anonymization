"""
class for count tree
"""

#!/usr/bin/env python
#coding=utf-8

# count tree


class CountTree(object):

    """
    Class for Count Tree Used in AA and DA.
    Store tree node in instances.
    self.value: node value
    self.level: tree level (root is 0)
    self.parent: ancestor node list
    self.child: successor node list
    self.support: support
    self.prefix: i-itemset
    """

    def __init__(self, value=None, parent=None):
        self.value = ''
        self.level = 0
        self.support = 0
        self.parent = []
        self.child = []
        self.prefix = []
        self.path = []
        self.traversal = []
        self.traversal_dict = {}
        if value is not None:
            self.value = value
            self.path.append(value)
        if parent is not None:
            self.parent = parent.parent[:]
            self.parent.insert(0, parent)
            self.prefix = parent.prefix[:]
            if parent.value != '*':
                self.prefix.append(parent.value)
            self.path = self.prefix[:]
            self.path.append(self.value)
            parent.child.append(self)
            self.level = parent.level + 1

    def node(self, tran, prefix=[]):
        """
        Search tree with value, return cut tree node.
        """
        index = 0
        len_tran = len(tran)
        for index, t in enumerate(self.child):
            if t.value == tran[0]:
                break
        else:
            print "Error can not find node"
            index = 0
        next_prefix = prefix[:]
        next_prefix.append(tran[0])
        if len_tran > 1:
            return self.child[index].node(tran[1:], next_prefix)
        else:
            return self.child[index]

    def add_to_tree(self, tran, prefix=[]):
        """
        Add combiation to count tree, add prefix to node
        """
        index = 0
        len_tran = len(tran)
        for index, t in enumerate(self.child):
            if t.value == tran[0]:
                break
        else:
            CountTree(tran[0], self)
            index = -1
        next_prefix = prefix[:]
        next_prefix.append(tran[0])
        if len_tran > 1:
            self.child[index].add_to_tree(tran[1:], next_prefix)
        else:
            self.child[index].support += 1

    def dfs_traversal(self, traversal, traversal_dict):
        """
        return deep first traversal of count tree
        """
        if self.value != '*':
            v_temp = ';'.join(self.path)
            traversal.append(v_temp)
            traversal_dict[v_temp] = self
        for child in self.child:
            child.dfs_traversal(traversal, traversal_dict)

    def print_tree(self):
        """
        print node and its direct children in count tree
        """
        print "prefix %s" % self.prefix
        for t in self.child:
            print t.value,
