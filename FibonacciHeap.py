from math import inf
from math import log2
from math import ceil

class FibonacciHeap:
    def __init__(self):
        self.header = None
        self.numNodes = 0

    def insert(self, node):

        if self.header == None:
            self.header = node

        else:
            self.header.left.right = node
            node.left = self.header.left
            node.right = self.header
            self.header.left = node
            if self.header.value > node.value:
                self.header = node

        self.numNodes += 1

    def findMin(self):
        return self.header

    def extractMin(self):
        minimum = self.header
        firstChild = minimum.child
        currentChild = firstChild

        if minimum != None:
            while currentChild != None:
                currentChild.left.right = currentChild.right
                currentChild.right.left = currentChild.left
                currentChild.parent = None
                currentChild.right = currentChild
                currentChild.left = currentChild
                self.insert(currentChild)
                if currentChild.right == currentChild:
                    currentChild = None

            if minimum.right == minimum:
                self.header = None
            else:
                self.header = minimum.right
                minimum.left.right = minimum.right
                self.header.left = minimum.left
                minimum.right = None
                minimum.left = None

            self.numNodes -= 1
            self.consolidate()

        return minimum

        

    def decreaseKey(self, node, value):
        if node.value < value:
            raise ValueError("Value is larger than existing value in the node")

        node.value = value

        if node.parent != None and node.value < node.parent.value:
            """
            cut off the nodes whose value is less than its parent and cascade this operation to its parent 
            to check if its parent has lost its second child
            """
            parent = node.parent
            self.cut(node)
            self.cascadingCut(parent)

        if node.value < self.header.value:
            self.header = node


    #cut off the node which is marked or whose value has been changed and insert it to the root list
    def cut(self, node):
        node.marked = False
        parent = node.parent
        parent.degree -= 1

        if parent.child == node:
            if node.right == node:
                parent.child = None
            else:
                parent.child = node.right

        tmp = node.left
        node.left.right = node.right
        node.right.left = tmp
        node.parent = None

        self.insert(node)

    def cascadingCut(self, node):
        parent = node.parent
        if parent != None:
            if node.marked == False:

                node.marked = True
                print(node.value)
                print(node.marked)

            else:
                self.cut(node)
                self.cascadingCut(parent)


    def merge(self, heap):
        min1 = self.header
        min2 = heap.header

        if min1 == None or min2 == None:
            return

        #concatenate both root lists
        tmp = min1.right
        min1.right = min2.right
        min2.right.left = min1
        min2.right = tmp
        tmp.left = min2
        #total number of nodes
        self.numNodes += heap.numNodes
        #change minimum
        if min1.value > min2.value:
            self.header = min2



    def consolidate(self):
        current = self.header
        degreeTable = [None for i in range(ceil(log2(self.numNodes) + 1))]
        minimum = current

        if current == None:
            return

        while current != None and current.right != self.header:
            if current.value < minimum.value:
                minimum = current

            if degreeTable[current.degree] == None:
                degreeTable[current.degree] = current
                current = current.right

            else:
                nodeWithSameDegree = degreeTable[current.degree]

                if current.value <= nodeWithSameDegree.value:
                    # current.sibling = nodeWithSameDegree.sibling
                    #remove node from root list
                    self.heapLink(current, nodeWithSameDegree)
                    degreeTable[nodeWithSameDegree.degree] = None

                else:
                    self.heapLink(nodeWithSameDegree, current)
                    degreeTable[current.degree] = None
                    current = nodeWithSameDegree


        self.header = minimum

    def printTree(self, current):
        if current.traversed:
            return

        current.traversed = True

        if current.parent == None:
            print("Root %d, Degree = %d, Marked = %s" %(current.value, current.degree, current.marked))
        else:
            print("Node %d, Degree = %d, Parent = %d, Marked = %s" %(current.value, current.degree, current.parent.value, current.marked))

        if current.child != None:
            self.printTree(current.child)

        if current.right != self.header:
            self.printTree(current.right)



    def delete(self, node):
        self.decreaseKey(node, -inf)
        return self.extractMin()

    def reverseRootListOrder(self):
        current = self.header.sibling
        last = current
        first = current

        while current != None:
            current.parent = None
            next = current.sibling
            self.header.sibling = current
            if first != current:
                current.sibling = first
                first = current
            last.sibling = next
            current = next

    def heapLink(self, nodeToBecomeParent, nodeToBecomeChild):
        #remove node from root list
        nodeToBecomeChild.left.right = nodeToBecomeChild.right
        nodeToBecomeChild.right.left = nodeToBecomeChild.left

        #consolidate both trees with same degree
        if nodeToBecomeParent.child == None:
            #cyclic links to itself
            nodeToBecomeChild.right = nodeToBecomeChild
            nodeToBecomeChild.left = nodeToBecomeChild
        else:
            nodeToBecomeChild.left = nodeToBecomeParent.child.left
            nodeToBecomeParent.child.left.right = nodeToBecomeChild
            nodeToBecomeParent.child.left = nodeToBecomeChild
            nodeToBecomeChild.right = nodeToBecomeParent.child

        #child will change it's parent and be unmarked
        nodeToBecomeChild.parent = nodeToBecomeParent
        nodeToBecomeChild.marked = False
        #parent's degree increment by 1 and link its child pointer to child node
        nodeToBecomeParent.child = nodeToBecomeChild
        nodeToBecomeParent.degree += 1

        #parent will become the header when it's child was originally a header
        if nodeToBecomeChild == self.header:
            self.header = nodeToBecomeParent


class Node:
    def __init__(self, value):
        self.value = value
        self.degree = 0
        self.sibling = None
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.marked = False
        self.traversed = False


if __name__ == "__main__":
    newHeap = FibonacciHeap()
    # anotherHeap = FibonacciHeap()
    # for i in range(6):
    #     node = Node(i)
    #     newHeap.insert(node)
    #
    # for i in range(6, 12):
    #     node = Node(i)
    #     anotherHeap.insert(node)
    #
    # newHeap.merge(anotherHeap)
    # current = newHeap.header
    # for i in range(12):
    #     print(current.value)
    #     current = current.right
    #
    # head = newHeap.extractMin()
    # current = newHeap.header
    # newHeap.printTree(current)
    ns = [7,23,17,30,24,45,26,35,18,39,21,52,38,41]
    d = []
    a = []
    decrease_key = [15, 5]
    for i in range(len(ns)):
        node = Node(ns[i])

        if ns[i] == 45 or ns[i] == 35:
            d.append(node)

        newHeap.insert(node)
        newHeap.consolidate()
        if ns[i] == 26 or ns[i] == 18 or ns[i] == 39:
            a.append(node)

    for i in a:
        i.marked = True
        
    for i in range(len(d)):
        newHeap.decreaseKey(d[i], decrease_key[i])

    current = newHeap.header
    newHeap.printTree(current)





