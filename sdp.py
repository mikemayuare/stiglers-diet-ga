# %%
from data.sd_data import data, data_per_unit, nutrients
from charles.charles import Population, Individual
from charles.crossover import uniform_crossover, arithmetic_xo
from charles.mutation import binary_mutation, swap_mutation
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
    total_nutrients = {nutrient: 0 for nutrient in nutrients}

    # Calculate total nutrients
    for i, gene in enumerate(self.representation):
        for nutrient in total_nutrients:
            total_nutrients[nutrient] += gene * data[i][nutrient]

    # Initialize fitness value
    fitness_value = total_cost

    # Check minimal intake
    for nutrient in total_nutrients:
        if total_nutrients[nutrient] < nutrients[nutrient]:
            # penalty
            fitness_value += 100 * (nutrients[nutrient] - total_nutrients[nutrient])
    print(total_nutrients)
    return fitness_value


# monkey patching the fitness
Individual.get_fitness = get_fitness

# initialize a single individual
size = len(data)
# the way this is initialized can impact how long this can take
representation = [random.gauss(3, 5) for _ in range(size)]

individual = Individual(representation=representation)
print(individual)
print(individual.representation)
# %%
