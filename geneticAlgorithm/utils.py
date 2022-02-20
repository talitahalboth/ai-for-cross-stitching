
# from genetic_algorithm import normalizeFitness
# from genetic_algorithm import Individual
# import random
# import copy
import matplotlib.pyplot as plt

# def proportionalSelection(problem, population):
#     normalizeFitness(problem, population)
#     cumulativeProb = 0.0
#     p = random.random()
#     for individual in population:
#         cumulativeProb += individual.fitness
#         if (p <= cumulativeProb):
#             return individual
#     print("nao achou")
#     return population[-1]
#
# def uniformSelection(problem, populationA, populationB, populationSize):
#     newPopulation  = []
#     tmpPopulation = []
#     for individual in populationA:
#         newInd = copy.deepcopy(individual)
#         tmpPopulation.append(newInd)
#     for individual in populationB:
#         newInd = copy.deepcopy(individual)
#         tmpPopulation.append(newInd)
#     normalizeFitness(problem, tmpPopulation)
#     for _ in range(0, populationSize):
#         newIndividual = proportionalSelection(problem, tmpPopulation)
#         newPopulation.append(newIndividual)
#     normalizeFitness(problem, newPopulation)
#
#     return newPopulation
#
# def onePointCrossover(parentA, parentB, problem):
#     used = []
#     newPermutation = []
#     for _ in range(0, len(parentA.permutation)):
#         used.append(0)
#         newPermutation.append(None)
#     for i in range(0, int(len(parentA.permutation)/2)):
#         index = int(parentA.permutation[i])
#         used[index]=1
#         newPermutation [i] = index
#     nextIndex = int(len(parentA.permutation)/2)
#     for elem in parentB.permutation:
#         if (used[int(elem)] == 0):
#             newPermutation[nextIndex] = int(elem)
#             used[int(elem)] = 1
#             nextIndex += 1
#     child = Individual(newPermutation, problem.evaluate(newPermutation) )
#     return child
#
# def chooseRandomParentCut(parentPerm):
#     i = random.randint(0, len(parentPerm)-1)
#     j = random.randint(i+1, len(parentPerm))
#     return i,j
#
# def selectCitiesNotCopied(parent, used):
#     lista = []
#     for i in range(len(parent.permutation)):
#         if (not used[parent.permutation[i]]):
#             lista.append(parent.permutation[i])
#     return lista
#
# def pmx(parentA, parentB, problem):
#     permSize = len(parentA.permutation)
#     indexOf = [[None]*permSize, [None]*permSize]
#     for i in range(permSize):
#         indexOf[0][parentA.permutation[i]]=i
#         indexOf[1][parentB.permutation[i]]=i
#
#     child1 = [None]*permSize
#     child2 = [None]*permSize
#     i,j = chooseRandomParentCut(parentA.permutation)
#     pai = [parentA, parentB]
#     filho = [child1, child2]
#     lista = [[],[]]
#     used = [[None]*permSize, [None]*permSize]
#     for ix in range(i,j):
#         child1[ix] = parentB.permutation[ix]
#         used[0][child1[ix]] = 1
#         child2[ix] = parentA.permutation[ix]
#         used[1][child2[ix]] = 1
#     for v in range(2):
#         lista[v] = selectCitiesNotCopied(pai[(v+1)%2], used[v])
#         for c in lista[v]:
#             aux = c
#             while (i <= indexOf[v][c] < j):
#                 c = filho[v][indexOf[v][c]]
#             filho[v][indexOf[v][c]] = aux
#     filho[0] = Individual(filho[0], problem.evaluate(filho[0]))
#     filho[1] = Individual(filho[1], problem.evaluate(filho[1]))
#     return filho

def drawTour(problem, permutation, best, gen):
    coords = []
    for i in permutation:
        coords.append(problem.coords[i])
    coords.append(problem.coords[permutation[0]])

    xs, ys = zip(*coords) #create lists of x and y values

    plt.clf()
    plt.plot(xs,ys, marker='o')
    plt.title("Custo:" + str(best) + " Geração: " + str(gen))
    plt.draw()
    plt.show(block=False)
    plt.pause(0.01)
