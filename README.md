# ai-for-cross-stitching

## Pattern Matching

Cross-stitch patterns typically utilize a grid with symbols to represent the color at each intersection. These diagrams are utilized in this context to determine the position of each stitch.

### Finding template images

We utilize OpenCV to detect the grid that forms the pattern. From this grid, we extract each symbol, ensuring that there are no repeated images by applying template matching.

#### Example

The following pattern[[1]](#1)

![image](https://user-images.githubusercontent.com/19466053/211222253-1566d43f-cc8f-4333-a706-ad4cf27d6d8e.png)

Has 6 different symbols, indicating 6 differente colours, and these are the following:

![template0](https://user-images.githubusercontent.com/19466053/211222243-1b584eb0-b1c1-4a98-bacb-8bda4dd725a7.png)
![template1](https://user-images.githubusercontent.com/19466053/211222287-6f339ced-2447-4755-87ad-bd7fb42325bf.png)
![template2](https://user-images.githubusercontent.com/19466053/211222292-7f66d457-923d-4c40-987f-693184653b91.png)
![template3](https://user-images.githubusercontent.com/19466053/211222296-2d7e0222-964a-446b-ad70-5c7d18ea6356.png)
![template4](https://user-images.githubusercontent.com/19466053/211222307-bdac91ad-d6df-4771-a65a-ba537021f7f8.png)
![template5](https://user-images.githubusercontent.com/19466053/211222312-0e29427e-eecd-4926-bae1-64939c274784.png)


### Finding colour of each stitch

Once again, we utilize OpenCV template matching to identify the coordinates of each colour. These coordinates will form the path that we follow when cross stitching each colour.

### Example:

The blue path is the shortest path found by the genetic algorithm to pass through with that symbol.

![template0](https://user-images.githubusercontent.com/19466053/211222526-ec5648a8-3f06-447c-9aea-007dfc702ad8.png)


## Path finding

Tries to find the most optimized path for cross stitching.
Here we ignore the "cross" and treat each stitch as a point, so, depending on the way the cross is carried out, the optimal path may change.

This is a genetic algorithm, so it is not guaranteed that it'll find the best solution.

We use a genetic algorithm to solve a modified version of the traveling salesman problem, so that it is not necessary to go back to the starting point. This is also known as the [shortest / minimum length hamiltonian path](https://stackoverflow.com/a/7158721).

### Genetic Algorithm

#### Parent Selection

For the parent selection we do the tournament selection.

#### Crossover

The crossover is carried out using the Edge Assembly Crossover (EAX) algorithm [[2]](#2)

#### Mutation

The mutation rate was set to 0.01. The mutation works by randomly swapping elements in the permutation of nodes.

#### Next Generation Selection

The next generation is selected based on their aptitude, combining parents and children, and the n best individuals are chosen.

## References
<a id="1">[1]</a> 
[DMC HEART - CROSS STITCH PATTERN](https://www.dmc.com/us/heart-cross-stitch-pattern-9012115.html)


<a id="2">[2]</a> 
Nagata, Y. (1997). Edge assembly crossover: A high-power genetic algorithm fot the traveling salesman problem. In Proceedings of the 7th International Conference on Genetic Algorithms, 1997.)
