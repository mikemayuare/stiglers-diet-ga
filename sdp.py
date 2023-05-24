# %%
from data.sd_data import data, nutrients
from charles.charles import Population, Individual
from charles.crossover import (
    uniform_crossover,
    arithmetic_xo,
    blx_alpha_xo,
    simplex_xo,
    sbx_xo,
    single_point_co,
    nux_xo,
)
from charles.mutation import (
    inversion_mutation,
    gaussian_mutation,
    sine_mutation,
    power_law_mutation,
)
from charles.selection import tournament_sel, rank_sel, fps
from operator import attrgetter
import random


def get_fitness(self):
    # Calculate total cost
    total_cost = sum(self.representation)

    # Initialize total nutrients dictionary
    self.total_nutrients = {nutrient: 0 for nutrient in nutrients}

    # Calculate total nutrients
    for i, gene in enumerate(self.representation):
        for nutrient in self.total_nutrients:
            self.total_nutrients[nutrient] += gene * data[i][nutrient]

    # Initialize fitness value
    fitness_value = total_cost

    # Check minimal intake
    for nutrient in self.total_nutrients:
        if self.total_nutrients[nutrient] < nutrients[nutrient]:
            # penalty
            fitness_value += 100 * (
                nutrients[nutrient] - self.total_nutrients[nutrient]
            )
    # print(self.total_nutrients)
    # print(fitness_value)
    return fitness_value


# monkey patching the fitness
Individual.get_fitness = get_fitness

# initialize a single individual
size = len(data)
# the way this is initialized can impact how long this can take

pop = Population(
    size=100,
    sol_size=size,
    valid_set=[
        0 if random.random() < 0.85 else random.uniform(0, 0.35) for _ in range(10000)
    ],
    replacement=True,
    optim="min",
)

pop.evolve(
    gens=500,
    # select=tournament_sel,
    select=rank_sel,
    # mutate=inversion_mutation,
    mutate=power_law_mutation,
    crossover=blx_alpha_xo,  # (alpha ~ 0.8)
    # crossover=simplex_xo,
    # crossover=uniform_crossover,
    # crossover=single_point_co,
    # crossover=sbx_xo,
    # crossover=nux_xo,  # eta ~ 1 - 3
    # in case the crossover has a third parameter use this
    # if not, comment or delete
    xo_param=0.8,
    mut_prob=0.1,
    xo_prob=0.9,
    elitism=True,
)

best_individual = min(pop.individuals, key=attrgetter("fitness"))
# print(best_individual.representation)
print(best_individual.total_nutrients)
print(f"Yearly budget {best_individual.fitness * 365}")
# representation=[0 if random.random() < 0.85 else random.uniform(0, 0.3) for _ in range(size)]
# individual = Individual(representation=representation)
# print(individual)
# print(individual.representation)
# %%
