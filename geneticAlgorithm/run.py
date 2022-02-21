from genetic_algorithm import genetic_algorithm
from tsp import TSP
import matplotlib.pyplot as plt
plt.style.use('ggplot')



def ga_tests():
    instances = ['instances/berlin10.tsp', 'instances/berlin15.tsp', 'instances/berlin16.tsp']
    instances += ['instances/dj38.tsp', 'instances/berlin52.tsp', 'instances/eli51.tsp']
    instances += ['instances/teste.tsp']
    print('Executando Algoritmo Genético...')
    for instance in instances:
        problem = TSP(instance)
        path, history = genetic_algorithm(problem)
        cost = problem.evaluate(path)

ga_tests()
