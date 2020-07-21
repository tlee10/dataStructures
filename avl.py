class AVLTree:
    def __init__(self):
        self.root = None
        self.count = 0

    def __len__(self):
        return self.count

    def insert(self, newItem: object) -> object:
        cond = True
        if self.count == 0:
            self.root = TreeNode(newItem)
            self.count += 1
            self.setHeight(self.root)

        else:
            node = self.root
            flag = True
            #keep looping until hits None
            while flag:
                #newItem is smaller than current node
                if node.item > newItem:
                    if node.left == None:
                        node.left = TreeNode(newItem)
                        node.left.parent = node
                        node = node.left
                        flag = False
                    else:
                        node = node.left
                #newItem is larger than current node
                elif node.item < newItem:
                    if node.right == None:
                        node.right = TreeNode(newItem)
                        node.right.parent = node
                        node = node.right
                        flag = False
                    else:
                        node = node.right

                else:
                    flag = False
                    print("Key %s exists in tree" %newItem)
                    cond = False

            #new item is inserted if true
            if cond:
                self.count += 1
                self.rebalance(node)


    def remove(self, item):
        if self.root == None:
            return False

        else:
            return self.remove_aux(item, self.root)

    def remove_aux(self, item, currentNode):
        if currentNode.item > item:
            if currentNode.left != None:
                return self.remove_aux(item, currentNode.left)
            else:
                return False

        elif currentNode.item < item:
            if currentNode.right != None:
                return self.remove_aux(item, currentNode.right)
            else:
                return False

        else:
            # if a node to be removed has two direct child, find the minimum node from its right sub-tree
            # and replace it with the minimum node
            if currentNode.left != None and currentNode.right != None:
                minRightSubTreeNode = self.findMinNode(currentNode.right)

                # change the item of currentNode to the item of the minimum node from the right sub-tree of currentNode
                currentNode.item = minRightSubTreeNode.item

                # remove the duplicated node (minRightSubTreeNode)
                if minRightSubTreeNode.right != None:
                    self.identifyChildToReplace(minRightSubTreeNode, minRightSubTreeNode.right)
                else:
                    self.identifyChildToReplace(minRightSubTreeNode, None)

                self.rebalance(minRightSubTreeNode.parent)
                self.resetNode(minRightSubTreeNode)

            elif currentNode.left != None:
                #currentNode only has left child
                self.identifyChildToReplace(currentNode, currentNode.left)
                self.rebalance(currentNode.parent)
                self.resetNode(currentNode)

            elif currentNode.right != None:
                #currentNode only has right child
                self.identifyChildToReplace(currentNode, currentNode.right)
                self.rebalance(currentNode.parent)
                self.resetNode(currentNode)


            else:
                #currentNode has no child
                self.identifyChildToReplace(currentNode, None)
                self.rebalance(currentNode.parent)
                self.resetNode(currentNode)

            self.count -= 1
            return True


    def findMinNode(self, node):
        if node.left == None:
            return node

        return self.findMinNode(node.left)

    def identifyChildToReplace(self, currentNode, replacement):
        """
        This function determines checks whether the node to be replaced(currentNode) is left or right child
        of its parent and replace it with another node(replacement). Replacement can be None if currentNode
        has no child.
        :param currentNode: node to be replaced
        :param replacement: replacement node
        time complexity - O(1)
        """
        if currentNode.parent == None:
            self.root = replacement
            replacement.parent = None

        elif currentNode.parent.right == currentNode:
            currentNode.parent.right = replacement
            if replacement != None:
                replacement.parent = currentNode.parent

        elif currentNode.parent.left == currentNode:
            currentNode.parent.left = replacement
            if replacement != None:
                replacement.parent = currentNode.parent

    def preorder(self):
        if self.root == None:
            print("Tree is empty")
        f = open("result.txt", "a")
        self.preorder_aux(self.root, f)
        f.close()

    def preorder_aux(self, node, f):
        #visit root, left, right (preorder)
        f.write(str(node.item) + "\n")
        if node.left != None:
            self.preorder_aux(node.left, f)
        if node.right != None:
            self.preorder_aux(node.right, f)

    def getHeight(self, node):
        if node == None:
            return -1

        return node.height

    def setHeight(self, node):
        node.height =  1 + max(self.getHeight(node.left), self.getHeight(node.right))

    def getBalanceFactor(self, node):
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rebalance(self, node):
        while node != None:
            balance = self.getBalanceFactor(node)

            if balance >= 2:
                #LR imbalance
                if self.getBalanceFactor(node.left) < 0:
                    self.rotateLeft(node.left)
                #LL imbalance
                self.rotateRight(node)

            elif balance <= -2:
                #RL imbalance
                if self.getBalanceFactor(node.right) > 0:
                    self.rotateRight(node.right)
                #RR imbalance
                self.rotateLeft(node)

            else:
                self.setHeight(node)

            node = node.parent

    def rotateLeft(self, node):
        pivot = node.right
        tmp = pivot.left

        #rotate pivot to left
        pivot.left = node
        self.identifyChildToReplace(node, pivot)
        node.parent = pivot

        #set pivot's original left child as node's right child
        node.right = tmp
        if tmp != None:
            tmp.parent = node

        #reset the height
        self.setHeight(node)
        self.setHeight(pivot)


    def rotateRight(self, node):
        pivot = node.left
        tmp = pivot.right

        #rotate pivot to right
        pivot.right = node
        self.identifyChildToReplace(node, pivot)
        node.parent = pivot

        #set pivot's original right child as node's left child
        node.left = tmp
        if tmp != None:
            tmp.parent = node

        #reset the height
        self.setHeight(node)
        self.setHeight(pivot)

    def resetNode(self, node):
        node.parent = None
        node.left = None
        node.right = None
        node.height = None

    def inorder(self):
        self.inorder_aux(self.root)

    def inorder_aux(self, node):
        if node.left != None:
            self.inorder_aux(node.left)

        print(node.item)

        if node.right != None:
            self.inorder_aux(node.right)

class TreeNode:
    def __init__(self, newItem):
        self.item = newItem
        self.right = None
        self.left = None
        self.parent = None
        self.height = None


if __name__ == "__main__":
    a = AVLTree()
