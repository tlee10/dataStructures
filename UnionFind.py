class UnionFind:

    def __init__(self, size):
        self.parent = [-1] * size

    def find(self, a):
        if self.parent[a] < 0:
            return a

        else:
            self.parent[a] = self.find(self.parent[a])
            return self.parent[a]


    def union(self, a, b):
        """
        Unify two disjoint sets. This function will look for the root of both elements and compare each component's size,
        smaller set will be combined with the other set.
        :param p: element
        :param q: element
        """
        rootA = self.find(a)
        rootB = self.find(b)

        if rootA == rootB:
            return

        #compare size of both sets
        if self.parent[rootA] < self.parent[rootB]:
            self.parent[rootA] += self.parent[rootB]
            self.parent[rootB] = rootA
        else:
            self.parent[rootA] += self.parent[rootB]
            self.parent[rootB] = rootA

    def connected(self, a, b):
        return self.find(a) == self.find(b)

if __name__ == "__main__":
    uf = UnionFind(10)

    print(uf.connected(1,2))
    uf.union(1,2)
    print(uf.connected(1, 2))
    uf.union(3,4)
    print(uf.find(4))
    uf.union(2, 4)
    print(uf.find(3))

