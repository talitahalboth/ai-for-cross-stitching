
import matplotlib.pyplot as plt


def drawTour(problem, permutation, best, gen):
    coords = []

    splitPermutation = permutation.index(len(permutation) -1)
    firstHalf = permutation[:splitPermutation]
    secondHalf = permutation[splitPermutation+1:]
    permutation = secondHalf + firstHalf

    for i in permutation:
        if (problem.coords[i] != [0, 0]):
            coords.append(problem.coords[i])
    # coords.append(problem.coords[permutation[0]])
    xs, ys = zip(*coords) #create lists of x and y values
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(problem.fileName)
    plt.clf()
    plt.plot(xs,ys, marker='o')
    plt.title("Custo:" + str(best) + " Geração: " + str(gen))
    plt.draw()
    plt.show(block=False)
    if (gen != -1):
        plt.pause(0.01)
    else:
        plt.waitforbuttonpress()