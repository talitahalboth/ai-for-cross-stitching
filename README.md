# ai-for-cross-stitching

Tries to find the most optimized path for cross stitching.
Here we ignore the "cross" and treat each stitch as a point, so, depending on the way the cross is carried out, the optimal path may change.

This is a genetic algorithm, so it is not guaranteed that it'll find the best solution.

We use a genetic algorithm to solve a modified version of the traveling salesman problem, so that it is not necessary to go back to the starting point. This is also known as the [shortest / minimum length hamiltonian path](https://stackoverflow.com/a/7158721).

## Genetic Algorithm

### Parent Selection

For the parent selection we do the tournament selection.

### Crossover

The crossover is carried out using the Edge Assembly Crossover (EAX) algorithm [[1]](#1)

### Mutation

The mutation rate was set to 0.01. The mutation works by randomly swapping elements in the permutation of nodes.

### Next Generation Selection

The next generation is selected based on their aptitude, combining parents and children, and the n best individuals are chosen.

## References
<a id="1">[1]</a> 
Nagata, Y. (1997). Edge assembly crossover: A high-power genetic algorithm fot the traveling salesman problem. In Proceedings of the 7th International Conference on Genetic Algorithms, 1997.)
