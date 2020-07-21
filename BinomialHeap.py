from math import inf

class BinomialHeap:
    def __init__(self):
        self.header = Node(None)

    def insert(self, value):
        newHeap = BinomialHeap()
        newHeap.header.sibling = Node(value)

        self.merge(newHeap)

    def findMin(self):
        min = Node(inf)
        current = self.header.sibling

        while current != None:
            if current.value < min.value:
                min = current

            current = current.sibling

        return min

    def extractMin(self):
        min = Node(inf)
        minPrev = self.header
        minNext = None
        prev = self.header
        current = self.header.sibling

        while current != None:
            if current.value < min.value:
                min = current
                minPrev = prev
                minNext = current.sibling

            prev = current
            current = current.sibling

        if min != None:
            #new heap will be a root list of min's children
            newHeap = BinomialHeap()
            newHeap.header.sibling = min.child

            min.child = None
            min.sibling = None
            minPrev.sibling = minNext

            #min's children will now be orphans
            newHeap.reverseRootListOrder()
            self.merge(newHeap)

        return min

    def decreaseKey(self, node, value):
        if node.value < value:
            raise ValueError("Value is larger than existing value in the node")

        node.value = value
        child = node
        current = node.parent

        while current != None and current.value > child.value:
            tmp = current.value
            current.value = child.value
            child.value = tmp
            child = current
            current = current.parent

    def merge(self, heap):
        prev1 = self.header
        prev2 = heap.header
        c1 = prev1.sibling
        c2 = prev2.sibling

        while c1 != None and c2 != None:
            if c1.degree > c2.degree:
                prev1.sibling = c2
                prev2.sibling = c2.sibling
                c2.sibling = c1
                c2 = prev2.sibling

            else:
                prev1 = c1
                c1 = c1.sibling

        if c2 != None:
            prev1.sibling = c2

        self.consolidate()

    def consolidate(self):
        prev = self.header
        current = prev.sibling
        next = current.sibling

        if current == None:
            return

        while next != None:
            if current.degree != next.degree:
                prev = current
                current = current.sibling
                next = current.sibling

            else:
                if next.sibling != None and next.sibling.degree == current.degree:
                    prev = current
                    current = current.sibling

                else:
                    if current.value <= next.value:
                        current.sibling = next.sibling
                        next.sibling = current.child
                        current.child = next
                        next.parent = current
                        current.degree += 1

                    else:
                        prev.sibling = next
                        current.sibling = next.child
                        next.child = current
                        current.parent = next
                        next.degree += 1
                        current = next

                next = current.sibling


    def printTree(self, current):
        if current.parent == None:
            print("Root %d, Degree = %d" %(current.value, current.degree))
        else:
            print("Node %d, Degree = %d, Parent = %d" %(current.value, current.degree, current.parent.value))
        if current.child != None:
            self.printTree(current.child)

        if current.sibling != None:
            self.printTree(current.sibling)



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


class Node:
    def __init__(self, value):
        self.value = value
        self.degree = 0
        self.sibling = None
        self.parent = None
        self.child = None

if __name__ == "__main__":
    h1 = BinomialHeap()
    h2 = BinomialHeap()

    n1 = Node(1)
    n2 = Node(2)
    n1.child = n2
    n2.parent = n1
    n1.degree = 1

    n3 = Node(3)
    n3.sibling = n1
    h1.header.sibling = n3

    n4 = Node(4)
    n5 = Node(5)
    n4.sibling = n5
    n6 = Node(6)
    n7 = Node(7)
    n5.degree = 2
    n5.child = n6
    n6.parent = n5
    n6.sibling = n7
    n7.parent = n5
    h2.header.sibling = n4

    h1.merge(h2)

    h1.insert(8)
    h1.insert(9)
    h1.insert(10)
    current = h1.header.sibling
    h1.printTree(current)

    minimum = h1.extractMin()
    print(minimum.value)
    current = h1.header.sibling
    h1.printTree(current)

    minimum = h1.delete(n7)
    print(minimum.value)
    current = h1.header.sibling
    h1.printTree(current)

