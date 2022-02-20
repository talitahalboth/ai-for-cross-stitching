import random

def tournamentSelection(problem, population, randomIndividual=5):
    randomIndividualsArray = []
    # choses random individuals and makes them get into tournaments to chose the best
    for _ in (0, randomIndividual):
        randomIndividualsArray.append(random.choice(population))
    last = None
    while (len(randomIndividualsArray) > 1):
        # choses two individuals and remove from the competitors the one that loses
        sakai = random.choice(randomIndividualsArray)
        ryuzo = random.choice(randomIndividualsArray)
        if (ryuzo.fitness >= sakai.fitness):
            randomIndividualsArray.remove(sakai)
            last = ryuzo
        else:
            randomIndividualsArray.remove(ryuzo)
            last = sakai
    return last