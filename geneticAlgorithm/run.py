from genetic_algorithm import genetic_algorithm
from tsp import TSP
import time
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def plot_evolution(fitness_history, problem):
    plt.figure()
    plt.plot(range(len(fitness_history)), fitness_history)
    plt.title(str(problem).split('.')[0])
    plt.xlabel('Geração')
    plt.ylabel('Aptidão Média')
    outfile = 'fitness_' + str(problem) + '.pdf'
    plt.savefig(outfile, dpi=300, bbox_inches='tight')



def ga_tests():
    instances = [  'instances/teste.tsp']
    #'instances/berlin15.tsp', 'instances/berlin16.tsp']
    # instances += ['instances/dj38.tsp', 'instances/berlin52.tsp', 'instances/eli51.tsp']
    print('Executando Algoritmo Genético...')
    for instance in instances:
        problem = TSP(instance)
        path, history = genetic_algorithm(problem)
        cost = problem.evaluate(path)


# a_star_tests()
ga_tests()
