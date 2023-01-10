import random
import numpy as np

# check if a path forms  an AB cycle
from .individual import Individual


def isABcycle(path, size):
    A = 0
    B = 1
    pathVertices = np.array([path[0][0]])

    # pathVertices.append()
    for i in range(len(path)):
        pathVertices = np.append(pathVertices, path[i][1])
    # stores the time at which an edge was visited and its from parent A.
    # 0 if edge wasn't visited
    visitedByA = np.zeros(size, dtype=int)

    current = A
    count = 0
    for edge in pathVertices:
        if (visitedByA[edge] != 0 and current == A):
            # returns 1 and position at which the cycle starts
            return (1, visitedByA[edge] - 1)
        if (current == A):
            visitedByA[edge] = count + 1
            current = B
        else:
            current = A
        count += 1

    return 0, 0


# generates AB Cycles
def generateABcycle(Ea, Eb, problem, size):
    # Set of AB Cycles generated
    abcycles = []
    # helper variable to store beginning of cycle
    i = 0
    # Adjacency list of A
    adjListA = []
    # Adjacency list of B
    adjListB = []
    createArrayOfEmptyArray(adjListA, adjListB, size)
    edgesInA = addEdgesToAdjList(adjListA, Ea)
    edgesInB = addEdgesToAdjList(adjListB, Eb)
    A = 0
    B = 1
    while (edgesInA > 0):

        # select vertex U the belongs to the vertices V s.t. number of edges incident to vertex  included in A != 0
        # randomly.
        vi = random.randint(0, size - 1)
        while (len(adjListA[vi]) == 0):
            vi = random.randint(0, size - 1)
        # current path
        path = []
        parent = A
        # choose randomly one of the other vertices that vi connects to
        vj = random.choice(adjListA[vi])
        # remove vertices from adj list
        adjListA[vi].remove(vj)
        adjListA[vj].remove(vi)
        edgesInA -= 1

        # stores vertices u,v of an edge
        edgeA = []
        edgeA.append(vi)
        edgeA.append(vj)
        # add edge to path
        path.append(edgeA)
        # controls last vertex visited in path
        prev = vj
        isCycle = 0
        while not isCycle:
            if (parent == A):
                edgeB = []
                edgeB.append(prev)
                v = adjListB[prev][0]
                if (len(adjListB[prev]) == 2):
                    v = random.choice(adjListB[prev])
                adjListB[prev].remove(v)
                adjListB[v].remove(prev)
                edgeB.append(v)
                path.append(edgeB)
                prev = v
                parent = B
            else:
                edgeA = []
                edgeA.append(prev)
                v = adjListA[prev][0]
                if (len(adjListA[prev]) == 2):
                    v = random.choice(adjListA[prev])
                edgeA.append(v)
                adjListA[prev].remove(v)
                adjListA[v].remove(prev)
                parent = A
                path.append(edgeA)
                prev = v
                edgesInA -= 1

            isCycle, i = isABcycle(path, size)
        # put back in adj lists vertices that werent used in cycle
        if (i > 0):
            for index in range(0, i):
                v = path[index][0]
                u = path[index][1]
                if (index % 2 == 0):
                    adjListA[v].append(u)
                    adjListA[u].append(v)
                    edgesInA += 1
                else:
                    adjListB[v].append(u)
                    adjListB[u].append(v)
        # get vertices that form cycle from the path
        cycle = []
        for i in range(i, len(path)):
            cycle.append(path[i])
        abcycles.append(cycle)
    return abcycles


def addEdgesToAdjList(adjListA, edgesList):
    edgesCount = 0
    for edge in edgesList:
        u = edge[0]
        v = edge[1]
        # add edges v -> u and u -> v to adjacency list
        adjListA[u].append(v)
        adjListA[v].append(u)
        edgesCount += 1
    return edgesCount

def createArrayOfEmptyArray(adjListA, adjListB, size):
    for _ in range(size):
        adjListA.append([])
        adjListB.append([])


# select cycles with probability 0.5
def selectRandomCycles(abCycles):
    D = []
    for element in abCycles:
        p = random.random()
        if (p < 0.5):
            D.append(element)
    # return at least one cycle randomly
    if (len(D) == 0):
        D.append(random.choice(abCycles))
    return D


def generateIntermediateSolution(D, C):
    A = 0
    B = 1
    for subTour in D:
        current = A
        for edge in subTour:
            reveseEdge = [edge[1], edge[0]]
            # remove from the child each edge that comes from parent A
            if (current == A and (edge in C)):
                C.remove(edge)
            elif (current == A and (reveseEdge in C)):
                C.remove(reveseEdge)
            # add to child each edge that comes from parent B
            elif (current == B):
                C.append(edge)

            if (current == A):
                current = B
            else:
                current = A
    return C


# splits tours
def splitTours(tourArray):
    from .DSU import DSU
    dsu = DSU(len(tourArray), tourArray)
    for edge in tourArray:
        # if there is and edge u -> v, merge sets of edge u and edge v
        dsu.unionSet(edge[0], edge[1], edge)

    # array of position to store each of the final sets
    position = [None] * len(tourArray)
    cont = 0
    for i in range(dsu.size):
        if (position[dsu.findSet(i)] == None):
            position[dsu.findSet(i)] = cont
            cont += 1
    # array with final edges of cycles
    ret = []
    for i in range(cont):
        ret.append([])
    for edge in tourArray:
        ret[position[dsu.findSet(edge[0])]].append(edge)
    return ret


def cut(e1, e2, problem):
    # price of cutting edge
    c1 = problem.distance_matrix[e1[0]][e1[1]]
    c2 = problem.distance_matrix[e2[0]][e2[1]]
    return c1 + c2


def link(e1, e2, problem):
    # price of linking two 4 vetices (from 2 edges)
    c1 = problem.distance_matrix[e1[0]][e2[0]]
    c2 = problem.distance_matrix[e1[1]][e2[1]]

    c3 = problem.distance_matrix[e1[0]][e2[1]]
    c4 = problem.distance_matrix[e1[1]][e2[0]]

    return min((c1 + c2), (c3 + c4))


# exchanges links between 2 edges as to minimize cost
def exchangeLinks(e1, e2, problem):
    a = e1[0]
    b = e1[1]
    c = e2[0]
    d = e2[1]

    c1 = problem.distance_matrix[a][c]
    c2 = problem.distance_matrix[b][d]

    c3 = problem.distance_matrix[a][d]
    c4 = problem.distance_matrix[b][c]

    if (c1 + c2 < c3 + c4):
        e1 = [a, c]
        e2 = [b, d]
    else:
        e1 = [a, d]
        e2 = [b, c]
    return (e1, e2)


# modifies set of subtours as to unite all in a single tour
def modification(problem, U, size):
    k = len(U)
    s = k
    while (s > 1):
        iStar = 0
        minLen = len(U[0])
        for i in range(s):
            if (len(U[i]) < minLen and len(U) > 0):
                iStar = i
                minLen = len(U[i])
        menor = -1
        jStar = 0
        ix = 0
        jx = 0
        for j in range(s):
            if (j != iStar):
                for i0 in range(len(U[iStar])):
                    for i1 in range(len(U[j])):
                        corte = cut(U[iStar][i0], U[j][i1], problem)
                        linka = link(U[iStar][i0], U[j][i1], problem)
                        res = linka - corte
                        if (menor == -1):
                            menor = res
                            ix = i0
                            jStar = j
                            jx = i1
                        if (res < menor):
                            menor = res
                            ix = i0
                            jStar = j
                            jx = i1
                        pass
        edgea = U[iStar][ix]
        edgeb = U[jStar][jx]
        U[iStar].remove(edgea)
        U[jStar].remove(edgeb)
        for edge in U[jStar]:
            U[iStar].append(edge)

        newA, newB = exchangeLinks(edgea, edgeb, problem)
        U[iStar].append(newA)
        U[iStar].append(newB)
        U[jStar] = U[s - 1]
        s -= 1
    adjList = []
    for i in range(size):
        adjList.append([])
    for u in U[0]:
        v = u[0]
        w = u[1]
        adjList[v].append(w)
        adjList[w].append(v)
    return U[0]


def eax(a, b, problem):
    Ea = []
    Eb = []
    C = []
    size = len(a.permutation)
    for i in range(size):
        i2 = (i + 1) % size
        Ea.append([a.permutation[i], a.permutation[i2]])
        Eb.append([b.permutation[i], b.permutation[i2]])
        # child starts as copy of parent A
        C.append([a.permutation[i], a.permutation[i2]])

    abCycles = generateABcycle(Ea, Eb, problem, size)

    D = selectRandomCycles(abCycles)

    intermediateSolution = generateIntermediateSolution(D, C)
    subtours = splitTours(intermediateSolution)
    childEdges = modification(problem, subtours, size)
    permutationArray = []
    for i in range(len(a.permutation)):
        permutationArray.append([])
    for edge in childEdges:
        v1 = edge[0]
        v2 = edge[1]
        permutationArray[v1].append(v2)
        permutationArray[v2].append(v1)
    permutation = []
    # generate permutation from edges list
    nxt = 0
    cur = -1
    while (len(permutation) < len(a.permutation)):
        permutation.append(nxt)
        tmp = nxt
        if (permutationArray[nxt][0] != cur):
            nxt = permutationArray[nxt][0]
            cur = tmp
        else:
            nxt = permutationArray[nxt][1]
            cur = tmp
    child = Individual(permutation, problem.evaluate(permutation))
    return child
