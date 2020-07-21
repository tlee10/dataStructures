from numpy import array
from numpy import insert

class FenwickTree:
    def __init__(self, list):
        self.size = len(list) + 1
        self.tree = self.constructTree(list)

    def pointUpdate(self, index, x):
        index += 1
        while index < self.size:
            self.tree[index] += x
            index += self.getLSB(index)

    def constructTree(self, list):
        tree = insert(array(list), 0, 0)
        insert(tree, 0, 0)
        for i in range(1, len(tree)):
            j = i + self.getLSB(i)
            if j < self.size:
                tree[j] += tree[i]
        return tree

    def getLSB(self, index):
        return index & -index

    def prefixSum(self, index):
        index += 1
        sum = 0
        while index != 0:
            sum += self.tree[index]
            index -= self.getLSB(index)
        return sum

    def rangeQuery(self, startIndex, endIndex):
        startIndex += 1
        endIndex += 1
        return self.prefixSum(endIndex) - self.prefixSum(startIndex-1)

if __name__ == "__main__":
    print(7 & -7)
    l = [1,2,3,4,5,6,7,8,9,10]
    ft = FenwickTree(l)
    print(ft.prefixSum(0) == sum(l[:1]))
    print(ft.prefixSum(1) == sum(l[:2]))
    print(ft.tree)
    print(ft.prefixSum(2))
    l[6] += 6
    ft.pointUpdate(6, 6)
    print(ft.tree)
    print(ft.prefixSum(2) == sum(l[:3]))
    print(ft.prefixSum(3) == sum(l[:4]))
    print(ft.prefixSum(4) == sum(l[:5]))
    print(ft.prefixSum(5) == sum(l[:6]))
    print(ft.prefixSum(6) == sum(l[:7]))
    print(ft.prefixSum(7) == sum(l[:8]))
    print(ft.prefixSum(8) == sum(l[:9]))
    print(ft.prefixSum(9) == sum(l))




