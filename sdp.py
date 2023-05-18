# %%
from data.sd_data import data_per_unit, nutrients
from charles.charles import Population, Individual
from charles.crossover import uniform_crossover
from charles.mutation import binary_mutation, swap_mutation
import random


def get_fitness(self):
    # Calculate the total cost of the diet
    total_cost = sum(
        self.representation[i] * data_per_unit[i]["1939 price (cents)"]
        for i in range(len(data_per_unit))
    )

    # Calculate the total intake of each nutrient
    nutrient_intake = {nutrient: 0 for nutrient in nutrients}
    for i in range(len(data_per_unit)):
        for nutrient in nutrients:
            nutrient_intake[nutrient] += (
                self.representation[i]
                / data_per_unit[i]["Unit"]
                * data_per_unit[i].get(nutrient, 0)
            )

    # Calculate a penalty for not meeting the minimum intake requirements
    penalty = sum(
        max(0, nutrients[nutrient] - nutrient_intake[nutrient])
        for nutrient in nutrients
    )

    # The fitness score is the total cost plus a penalty
    # for not meeting the nutrient requirements
    fitness_score = (
        total_cost + penalty * 5000
    )  # the factor of 1000 is arbitrary and can be adjusted

    return fitness_score


# monkey patching the fitness
Individual.get_fitness = get_fitness

ind = Individual(
    representation=[random.randint(0, item["Unit"]) for item in data_per_unit]
)
print(ind)
# %%
