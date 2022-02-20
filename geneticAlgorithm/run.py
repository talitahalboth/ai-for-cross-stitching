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
        # historiy_list = []
        # mean_time = 0
        # mean_cost = 0
        # print(problem)
        # start_time = time.time()
        path, history = genetic_algorithm(problem)
        # mean_time += time.time() - start_time
        cost = problem.evaluate(path)
        # mean_cost += cost
        # print('Custo do caminho:', cost)
        # historiy_list.append(history)
        # mean_history = [sum(x) for x in zip(*historiy_list)]
        # print('Custo medio:', mean_cost/5)
        # print('Tempo medio:', str(mean_time/5), 'segundos')
        # plot_evolution(mean_history, problem)


# a_star_tests()
ga_tests()
