class Tree:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.lchild = None
            self.sibling = None
            self.parent = None

        def insert(self, new_tree):
            if self.lchild:
                new_tree.root.parent = self
                new_tree.root.sibling = self.lchild
                self.lchild = new_tree.root
            else:
                self.lchild = new_tree.root
                new_tree.root.parent = self

    def __init__(self, data):
        self.root = self.Node(data)

    def insert(self, current_node, new_tree):
        if current_node:
            if current_node.parent:
                new_tree.root.parent = current_node.parent
                new_tree.root.parent.lchild = new_tree.root
                current_node.parent = None
            new_tree.root.sibling = current_node
        else:
            new_tree.root.parent = self.root
            self.root.lchild = new_tree.root
        return new_tree

    def lchild(self):
        return self.root.lchild

    def sibling(self):
        return self.root.sibling

    def data(self):
        return self.root.data

# Constructing the tree
tree = Tree(1)  # Tree with root 1

# Inserting new nodes
tree.insert(tree.lchild(), Tree(2))
# (1 (2))
tree.insert(tree.lchild(), Tree(3))
# (1 (3 2)) - 3 to the left of 2

# Adding children to node 2
n2 = tree.lchild().sibling  # Node 2
n2.insert(Tree(5))
# (1 (3 2(5)))
n2.insert(Tree(6))
# (1 (3 2(6 5)))

def preorden_aux2(node, L):
    if node:
        L.append(node.data)
        preorden_aux2(node.lchild, L)
        preorden_aux2(node.sibling, L)
    return L

def preorden2(tree):
    L = []
    preorden_aux2(tree.root, L)
    return L

def altura_aux(node, profundidad_actual, profundidad_maxima):
    if node:
        if profundidad_actual > profundidad_maxima:
            profundidad_maxima = profundidad_actual
        profundidad_maxima = altura_aux(node.lchild, profundidad_actual + 1, profundidad_maxima)
        profundidad_maxima = altura_aux(node.sibling, profundidad_actual, profundidad_maxima)
    return profundidad_maxima

def altura(tree):
    return altura_aux(tree.root, 0, 0)

# Printing pre-order traversal and height
print(preorden2(tree))  # Expected Output: [1, 3, 2, 6, 5]
print(altura(tree))  # Expected Output: 3
