# ai-for-cross-stitching

Tries to find the most optimized path for cross stitching.

This uses an genetic algorithm to solve the traveling salesman problem, modified so that it is not necessary to go back to the starting point, the [shortest / minimum length hamiltonian path](https://stackoverflow.com/a/7158721).

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
