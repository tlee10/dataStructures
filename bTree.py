import random
"""
PROPERTIES OF B-TREE
1. Every node x has the following fields:
    a. n[x], the number of keys currently stored in node x,
    b. the n[x] keys themselves, stored in nondecreasing order, so that key1[x] ≤
    key2[x] ≤ ··· ≤ keyn[x][x],
    c. leaf [x], a boolean value that is TRUE if x is a leaf and FALSE if x is an
    internal node.

2. Each internal node x also contains n[x]+ 1 pointers c1[x], c2[x], ..., cn[x]+1[x] to its
children. Leaf nodes have no children, so their ci fields are undefined.

3. The keys keyi[x] separate the ranges of keys stored in each subtree: if ki is any key
stored in the subtree with root ci [x], then
k1 ≤ key1[x] ≤ k2 ≤ key2[x] ≤··· ≤ keyn[x][x] ≤ kn[x]+1.

4. All leaves have the same depth, which is the tree's height h.

5. There are lower and upper bounds on the number of keys a node can contain. These
bounds can be expressed in terms of a fixed integer t ≥ 2 called the minimum degree of the B-tree:
    a. Every node other than the root must have at least t - 1 keys. Every internal node other than the root thus has at least t children. If the tree is nonempty, the root must have at least one key.
    b. Every node can contain at most 2t - 1 keys. Therefore, an internal node can have at most 2t children. We say that a node is full if it contains exactly 2t - 1 keys.[1]

min item = t - 1
max item = 2t - 1

min child = t
max child = 2t
"""

class Node:
    def __init__(self, degree):
        self.numKeys = 0
        self.keys = [None] * (2*degree - 1)
        self.children = [None] * (2*degree)
        self.isLeaf = True

class BTree():
    def __init__(self, degree):
        self.root = Node(degree)
        self.degree = degree

    def search(self, node, k):
        i = 0

        while i < node.numKeys and k > node.keys[i]:
            i += 1

        if i < node.numKeys and k == node.keys[i]:
            return (node, i)

        if node.isLeaf:
            return None #key not found

        else:
            return self.search(node.children[i], k)

    #x = non-full parent of y, y = a full node, index = position of y in c[x]
    def splitChild(self, x, index, y):
        z = Node(self.degree)
        z.isLeaf = y.isLeaf
        z.numKeys = self.degree - 1

        #allocate the later half of y's keys to z
        for i in range(self.degree - 1):
            z.keys[i] = y.keys[i + self.degree]
            y.keys[i + self.degree] = None

        #allocate the later half of y's children to z
        if y.isLeaf == False:
            for i in range(self.degree):
                z.children[i] = y.children[i + self.degree]
                y.children[i + self.degree] = None

        y.numKeys = self.degree - 1

        #shift every child link of x after index one space to the right
        for i in range(x.numKeys, index + 1, -1):
            x.children[i] = x.children[i-1]

        x.children[index + 1] = z #z will be new child for node x at index

        #move the median value of y to x
        x.keys[index] = y.keys[self.degree-1]
        y.keys[self.degree - 1] = None

        x.numKeys += 1

    def insert(self, k):
        r = self.root
        t = self.degree

        #if root is full
        if r.numKeys == 2*t - 1:
            s = Node(t)
            self.root = s
            s.isLeaf = False
            s.children[0] = r
            #split then insert new k
            self.splitChild(s, 0, r)
            self.insertNonFull(s, k)
        else:
            self.insertNonFull(r, k)

    def insertNonFull(self, x, k):
        i = x.numKeys - 1

        #only insert into leaves
        if x.isLeaf:
            #shift every key that is bigger than k one place to the right
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
            x.numKeys += 1

        else:
            #move to the right position
            while i >= 0 and k < x.keys[i]:
                i -= 1

            i += 1

            #if child is full
            if x.children[i].numKeys == 2*self.degree - 1:
                self.splitChild(x, i, x.children[i])
                if k > x.keys[i]:
                    i += 1

            self.insertNonFull(x.children[i], k)

    def delete(self, k):
        if self.root.numKeys == 0:
            self.root = self.root.children[0]

        self.delete_aux(self.root, k)

    def delete_aux(self, x, k):
        # for i in range(x.numKeys):
        #     if x.isLeaf == False:
        #         for j in range(x.children[i].numKeys):
        #             if x.children[i].keys[j] > x.keys[i]:
        #                 print("NOT SORTED ", str(k))
        #                 print(x.keys[i])
        #                 print(x.children[i].keys)
        #
        # for i in range(x.numKeys):
        #     if x.isLeaf == False:
        #         for j in range(x.children[i + 1].numKeys):
        #             if x.children[i + 1].keys[j] < x.keys[i]:
        #                 print("LARGE NOT SORTED ", str(k))
        print("CURRENT KEYS")
        print(x.keys)
        i = 0

        while i < x.numKeys and k > x.keys[i]:
            i += 1

        if i < x.numKeys and x.keys[i] == k: #k in node x

            if x.isLeaf:  # x is a leaf
                self.replaceDeletedKey(x, i, 0)

            else: #x is an internal node
                self.deleteInternalNode(x, k, i)

        else: #k not in node x

            if x.isLeaf == False:
                if x.children[i].numKeys >= self.degree: #child i has more than t - 1 keys
                    if i < x.numKeys:
                        print("PARENT KEY = ", str(x.keys[i]))
                    print("INDEX = ", str(i))
                    print("CHILDREN")
                    print(x.children[i].keys)
                    self.delete_aux(x.children[i], k)

                else: #child i has less than t degree
                    # immediate sibling of child i has more than t-1 keys
                    if i - 1 >= 0 and x.children[i - 1].numKeys >= self.degree:
                        self.borrowFromPrev(x, i)

                    elif i + 1 <= x.numKeys and x.children[i+1].numKeys >= self.degree:
                        self.borrowFromNext(x, i)

                    else:
                        if i - 1 >= 0:
                            self.merge(x, x.children[i], x.children[i - 1], i, i - 1)
                            i -= 1

                        else:
                            self.merge(x, x.children[i], x.children[i + 1], i, i + 1)
                    if i < x.numKeys:
                        print("PARENT KEY = ", str(x.keys[i]))
                    print("INDEX = ", str(i))
                    print("CHILDREN")
                    print(x.children[i].keys)
                    self.delete_aux(x.children[i], k)

            else:
                print("KEY NOT FOUND")

    #this function is used when a key in a node is deleted or moved
    def replaceDeletedKey(self, x, index, j):
        for i in range(index, x.numKeys - 1):
            x.keys[i] = x.keys[i + 1]

        if x.isLeaf == False:
            for i in range(j, x.numKeys):
                x.children[i] = x.children[i + 1]

        x.keys[x.numKeys - 1] = None
        x.children[x.numKeys] = None
        x.numKeys -= 1

    def merge(self, x, y, z, index, j):

        #if sibling is on the right
        if j > index:
            # move k to y and merge z with y
            y.keys[y.numKeys] = x.keys[index]
            y.numKeys += 1
            start = y.numKeys
            for i in range(z.numKeys):
                y.keys[start + i] = z.keys[i]

            for i in range(z.numKeys + 1):
                y.children[start + i] = z.children[i]

            y.numKeys += z.numKeys

        else: #sibling on the left
            # move k to y and merge z with y
            z.keys[z.numKeys] = x.keys[index - 1]
            z.numKeys += 1
            start = z.numKeys
            for i in range(y.numKeys):
                z.keys[start + i] = y.keys[i]

            for i in range(y.numKeys + 1): #no + 1 because the numkeys of y had been incremented above
                z.children[start + i] = y.children[i]

            z.numKeys += y.numKeys
            j += 1
            index -= 1

        #after k is moved down to x's child, update x's keys
        self.replaceDeletedKey(x, index, j)

    def borrowFromPrev(self, x, index):

        child = x.children[index]
        sibling = x.children[index - 1]

        #shift all keys in child one place to the right
        for i in range(child.numKeys, 0, -1):
            child.keys[i] = child.keys[i - 1]

        child.keys[0] = x.keys[index - 1] # move k down from x to child
        child.numKeys += 1

        x.keys[index - 1] = sibling.keys[sibling.numKeys - 1]

        if sibling.isLeaf == False:
            lastChildOfSibling = sibling.children[sibling.numKeys] #since one key from sibling is moved up to x, need to link the sibling's child that is bigger than that key to child
            if child.isLeaf == False:
                #shift child's children one place to the right
                for i in range(child.numKeys, 0, -1):
                    child.children[i] = child.children[i - 1]

            child.children[0] = lastChildOfSibling

            #remove key from sibling
            sibling.keys[sibling.numKeys - 1] = None
            sibling.children[sibling.numKeys] = None
            sibling.numKeys -= 1


    def borrowFromNext(self, x, index):
        child = x.children[index]
        sibling = x.children[index + 1]

        child.keys[child.numKeys] = x.keys[index]  # move k down from x to child
        child.numKeys += 1

        x.keys[index] = sibling.keys[0]

        if sibling.isLeaf == False:
            firstChildOfSibling = sibling.children[0]  # since one key from sibling is moved up to x, need to link the sibling's child that is smaller than that key to child

            for i in range(sibling.numKeys):
                sibling.children[i] = sibling.children[i + 1]

            for i in range(sibling.numKeys - 1):
                sibling.keys[i] = sibling.keys[i + 1]

            child.children[child.numKeys] = firstChildOfSibling

            # remove key from sibling
            sibling.keys[sibling.numKeys - 1] = None
            sibling.children[sibling.numKeys] = None
            sibling.numKeys -= 1

    def deleteInternalNode(self, x, k, i):
        t = self.degree

        if x.isLeaf:
            if x.keys[i] == k:
                self.replaceDeletedKey(x, i, 0)

        else:
            if x.children[i].numKeys >= t:
                x.keys[i] = self.deletePredecessor(x.children[i])

            elif x.children[i + 1].numKeys >= t:
                x.keys[i] = self.deleteSuccessor(x.children[i + 1])

            else:
                self.merge(x, x.children[i], x.children[i + 1], i, i + 1)
                self.deleteInternalNode(x.children[i], k, t - 1)

    # Delete the predecessor
    def deletePredecessor(self, x):
        if x.isLeaf:
            key = x.keys[x.numKeys - 1]
            self.replaceDeletedKey(x, x.numKeys - 1, 0)
            return key

        i = x.numKeys - 1

        if x.children[i + 1].numKeys >= self.degree:
            i += 1

        elif x.children[i + 1].numKeys < self.degree and x.children[i].numKeys >= self.degree:
            self.borrowFromPrev(x, i+1)

        elif x.children[i + 1].numKeys < self.degree:
            self.merge(x, x.children[i], x.children[i + 1], i, i+1)

        return self.deletePredecessor(x.children[i])

    # Delete the successor
    def deleteSuccessor(self, x):
        if x.isLeaf:
            key = x.keys[0]
            self.replaceDeletedKey(x, 0, 0)
            return key

        if x.children[0].numKeys < self.degree and x.children[1].numKeys >= self.degree:
            self.borrowFromNext(x, 0)

        elif x.children[0].numKeys < self.degree:
            self.merge(x, x.children[0], x.children[1], 0, 1)

        return self.deleteSuccessor(x.children[0])

    # def findPredecessor(self, x, k, index):
    #     child = x.children[index]
    #     i = child.numKeys - 1
    #
    #     while i > 0 and k < child.keys[i]:
    #         i -= 1
    #
    #     return child.keys[i]
    #
    # def findSucessor(self, x, k, index):
    #     child = x.children[index + 1]
    #     i = 0
    #
    #     while i < child.numKeys - 1 and k > child.keys[i]:
    #         i += 1
    #
    #     return child.keys[i]


