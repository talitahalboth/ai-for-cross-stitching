# AI for Cross Stitching
<a href="https://github.com/talitahalboth/ai-for-cross-stitching/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/talitahalboth/ai-for-cross-stitching?color=f8be29&style=flat-square">
</a>
<a href="https://github.com/talitahalboth/ai-for-cross-stitching/stargazers">
  <img src="https://img.shields.io/github/stars/talitahalboth/ai-for-cross-stitching?color=f8be29&style=flat-square">
</a>

## Requirements

```
pip install -r requirements.txt
```

## Usage

You can run the project with 

```
python main.py
```

use the `-h` option to check the allowed arguments.


## Pattern Matching

Cross-stitch patterns typically utilize a grid with symbols to represent the color at each intersection. These diagrams are utilized in this context to determine the position of each stitch.

### Finding template images

We utilize OpenCV to detect the grid that forms the pattern:

<img src="https://user-images.githubusercontent.com/19466053/211701658-b122620e-b877-401f-81ab-9613437eb4b4.png" width=50% height=50%>


From this grid, we extract each symbol, ensuring that there are no repeated images by applying template matching.

#### Example

The following pattern[[1]](#1):

<img src="https://user-images.githubusercontent.com/19466053/211228312-5c06968f-2e07-434e-bfcd-80ecbdae98d0.png " width=50% height=50%>


Has 5 different symbols, indicating 5 differente colours, and these are represented by the following symbols:

![template1](https://user-images.githubusercontent.com/19466053/211228280-a6a12506-2a43-4f55-9de8-6881fb90b714.png)
![template2](https://user-images.githubusercontent.com/19466053/211228284-4f1b9f95-410d-487e-af25-276b79771635.png)
![template3](https://user-images.githubusercontent.com/19466053/211228293-7874abc4-8d87-47fc-afba-72ee2102a975.png)
![template4](https://user-images.githubusercontent.com/19466053/211228295-7f8f04de-bd31-4332-bf5c-f6c29ce51578.png)
![template5](https://user-images.githubusercontent.com/19466053/211228297-6fef6fc1-b67c-4646-8bdb-fdfb53adb8fe.png)


### Finding colour of each stitch

Once again, we utilize OpenCV template matching to identify the coordinates of each colour. These coordinates will form the path that we follow when cross stitching each colour. To to that, we use a genetic algorithm. To speed things up, on this part we use multiple threads, and each template is a seperate thread.

#### Example:

The blue filled squares are the regions that matched the ![template1](https://user-images.githubusercontent.com/19466053/211228280-a6a12506-2a43-4f55-9de8-6881fb90b714.png) template.

<img src="https://user-images.githubusercontent.com/19466053/211805952-8eee5c86-b84b-4c59-abba-55ee281ed677.png" width=50% height=50%>


The blue path is the shortest path found by the genetic algorithm to pass through each points matching the template we used.

<img src="https://user-images.githubusercontent.com/19466053/211228271-7602a11c-16a4-402e-9d00-8bbdd3e69941.png " width=50% height=50%>



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

## Observations

Big pattern images work better than small ones, and sometimes it has issues with low res images.
The template images' size must be as close as possible to the size of the symbols on the actual pattern.

## References
<a id="1">[1]</a> 
[DMC - ROCKET SHIP PATTERN](https://www.dmc.com/us/rocket-ship--pattern-9003993.html)


<a id="2">[2]</a> 
Nagata, Y. (1997). Edge assembly crossover: A high-power genetic algorithm fot the traveling salesman problem. In Proceedings of the 7th International Conference on Genetic Algorithms, 1997.)
