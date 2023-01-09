
import matplotlib.pyplot as plt


def drawTour(problem, permutation, best, gen, shortestHamPath = False):
    coords = []

    splitPermutation = permutation.index(len(permutation) -1)
    firstHalf = permutation[:splitPermutation]
    secondHalf = permutation[splitPermutation:]
    permutation = secondHalf + firstHalf
    for i in permutation:
        if (problem.coords[i] != [-1, -1]):
            coords.append(problem.coords[i])
    if not shortestHamPath:
        coords.append(problem.coords[permutation[0]])
    xs, ys = zip(*coords) #create lists of x and y values
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(problem.fileName)
    plt.clf()
    plt.gca().invert_yaxis()

    plt.plot(xs,ys, marker='o')
    plt.title("Custo:" + str(best) + " Geração: " + str(gen))
    plt.draw()
    plt.show(block=False)
    if (gen != -1):
        plt.pause(0.01)
    else:
        plt.waitforbuttonpress()