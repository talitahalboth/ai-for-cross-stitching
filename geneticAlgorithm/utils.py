
import matplotlib.pyplot as plt


def drawTour(problem, permutation, best, gen):
    coords = []

    splitPermutation = permutation.index(len(permutation) -1)
    firstHalf = permutation[:splitPermutation]
    secondHalf = permutation[splitPermutation+1:]
    print(firstHalf, secondHalf)
    permutation = secondHalf + firstHalf

    for i in permutation:
        if (problem.coords[i] != [0, 0]):
            coords.append(problem.coords[i])
    # if (permutation[0] != len(permutation)):
    # coords.append(problem.coords[permutation[0]])
    # print(coords)
    xs, ys = zip(*coords) #create lists of x and y values

    plt.clf()
    plt.plot(xs,ys, marker='o')
    plt.title("Custo:" + str(best) + " Geração: " + str(gen))
    plt.draw()
    plt.show(block=False)
    if (gen != -1):
        plt.pause(0.01)
    else:
        plt.waitforbuttonpress()