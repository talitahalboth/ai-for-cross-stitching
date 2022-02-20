
import matplotlib.pyplot as plt


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
