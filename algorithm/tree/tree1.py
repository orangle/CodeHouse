# coding:utf-8

class Tree(object):
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)


def total(tree):
    if tree == None:
        return 0
    return total(tree.left) + total(tree.right) + tree.cargo

def print_tree(tree):
    if tree == None:
        return
    print tree.cargo
    print_tree(tree.left)
    print_tree(tree.right)

def print_postorder(tree):
    if tree == None:
        return
    print_postorder(tree.left)
    print_postorder(tree.right)
    print tree.cargo

def print_inorder(tree):
    if tree == None:
        return
    print_inorder(tree.left)
    print tree.cargo
    print_inorder(tree.right)

def print_tree_indent(tree, level=0):
    if tree == None:
        return
    print_tree_indent(tree.left, level+1)
    print '  '*level + str(tree.cargo)
    print_tree_indent(tree.right, level+1)



left = Tree(2)
right = Tree(3)
tree = Tree(1, left, right)
#print total(tree)
#print_tree(tree)
#print_postorder(tree)
#print_inorder(tree)
print_tree_indent(tree)



