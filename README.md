## Stigler’s Diet Problem with Genetic Algorithms

 The Stigler diet is an optimization problem named for George Stigler, a 1982 Nobel laureate in economics, who posed the following problem [[Wikipedia](https://en.wikipedia.org/wiki/Stigler_diet)]:

   > For a moderately active man weighing 154 pounds, how much of each of 77 foods should be eaten on a daily basis so that the man’s intake of nine nutrients will be at least equal to the recommended dietary allowances (RDAs) suggested by the National Research Council in 1943, with the cost of the diet being minimal?

### Dataset
The dataset is from https://developers.google.com/optimization/lp/stigler_diet.


### Description

This project presents the implementation of genetic algorithms to solve Stigler's Diet Problem. The objective was to build an efficient model capable of finding optimal solutions for this optimization problem. The project involved implementing various selection, crossover, and mutation operators, and comparing their performance. The fitness function was designed to calculate the total cost of the diet while penalizing solutions that did not meet nutritional requirements. Selection methods such as tournament selection, ranking selection, and fitness proportion selection were employed. Configurations were determined by running the algorithms multiple times and applying statistical tests to identify the best combination of operators. The inclusion of elitism was found to improve the algorithm's convergence to the global optimum. Results showed the algorithm's smooth convergence towards optimal or near-optimal solutions. Illustrations were provided to demonstrate the performance of different operator combinations and parameter tuning.

