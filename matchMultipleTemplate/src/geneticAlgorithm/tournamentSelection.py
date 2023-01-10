import random

def tournamentSelection(problem, population, randomIndividual=5):
    randomIndividualsArray = []
    # chooses random individuals and makes them get into tournaments to choose the best
    for _ in (0, randomIndividual):
        randomIndividualsArray.append(random.choice(population))
    last = None
    while (len(randomIndividualsArray) > 1):
        # chooses two individuals and remove from the competitors the one that loses
        sakai = random.choice(randomIndividualsArray)
        ryuzo = random.choice(randomIndividualsArray)
        if (ryuzo.fitness >= sakai.fitness):
            randomIndividualsArray.remove(sakai)
            last = ryuzo
        else:
            randomIndividualsArray.remove(ryuzo)
            last = sakai
    return last
