# %%
from data.sd_data import data, data_per_unit, nutrients
from charles.charles import Population, Individual
from charles.crossover import uniform_crossover, arithmetic_xo, blx_alpha_crossover
from charles.mutation import inversion_mutation
from charles.selection import tournament_sel
from operator import attrgetter
import random


# def get_fitness(self):
#     # Calculate the total cost of the diet
#     total_cost = sum(
#         self.representation[i] * data_per_unit[i]["1939 price (cents)"]
#         for i in range(len(data_per_unit))
#     )

#     # Calculate the total intake of each nutrient
#     nutrient_intake = {nutrient: 0 for nutrient in nutrients}
#     for i in range(len(data_per_unit)):
#         for nutrient in nutrients:
#             nutrient_intake[nutrient] += self.representation[i] / data_per_unit[i]["Unit"] * data_per_unit[i].get(
#                 nutrient, 0
#             )

#     # Calculate a penalty for not meeting the minimum intake requirements
#     penalty = sum(
#         max(0, nutrients[nutrient] - nutrient_intake[nutrient])
#         for nutrient in nutrients
#     )

#     # The fitness score is the total cost plus a penalty
#     # for not meeting the nutrient requirements
#     fitness_score = (
#         total_cost + penalty * 5000
#     )  # the factor of 1000 is arbitrary and can be adjusted

#     return fitness_score


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
    print(fitness_value)
    return fitness_value


# monkey patching the fitness
Individual.get_fitness = get_fitness

# initialize a single individual
size = len(data)
# the way this is initialized can impact how long this can take

pop = Population(
    size=200,
    sol_size=size,
    valid_set=[
        0 if random.random() < 0.85 else random.uniform(0, 0.3) for _ in range(1000)
    ],
    replacement=True,
    optim="min",
)

pop.evolve(
    gens=100,
    select=tournament_sel,
    mutate=inversion_mutation,
    crossover=blx_alpha_crossover,
    mut_prob=0.05,
    xo_prob=0.9,
    elitism=True,
)

best_individual = min(pop.individuals, key=attrgetter("fitness"))
# print(best_individual.representation)
print(best_individual.total_nutrients)
# representation=[0 if random.random() < 0.85 else random.uniform(0, 0.3) for _ in range(size)]
# individual = Individual(representation=representation)
# print(individual)
# print(individual.representation)
# %%
