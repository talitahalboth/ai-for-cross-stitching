# Disjoint-Set Union
# data structure that stores a collection of disjoint (non-overlapping) sets
class DSU:
    def __init__(self, size, edges):
        self.size = size
        self.p = []
        for i in range(size):
            self.p.append(i)

    # finds set that i belongs to
    def findSet(self, i):
        if (self.p[i] == i):
            return i
        self.p[i] = self.findSet(self.p[i])
        return self.p[i]

    # check if two elements belong to same set
    def isSameSet(self, i, j):
        return self.findSet(i) == self.findSet(j)

    # merge two sets
    def unionSet(self, i, j, edge):
        if (not self.isSameSet(i, j)):
            self.p[self.findSet(i)] = self.findSet(j)

