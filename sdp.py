# %%
from data.sd_data import data, nutrients
from charles.charles import Population, Individual
from charles.crossover import uniform_crossover
from charles.mutation import binary_mutation, swap_mutation

valid_set = ["0", "1"]  # with replacement


def get_fitness(self, constraints=nutrients):
    total_cost = 0
    self.constraints = constraints
    nutrient_values = {nutrient: 0 for nutrient in self.constraints.keys()}

    for index, gene in enumerate(self.representation):
        commodity = self.dataset[index]
        quantity = int(gene) * commodity["Unit"]
        total_cost += quantity * commodity["1939 price (cents)"]

        for nutrient in self.constraints:
            nutrient_values[nutrient] += quantity * commodity[nutrient]

    # Check if individual meets the minimum requirements for each nutrient
    for nutrient in self.constraints:
        if nutrient_values[nutrient] < self.constraints[nutrient]:
            return 0

    return 1 / total_cost  # Invert the cost to maximize the fitness


# monkey patching the fitness
Individual.get_fitness = get_fitness
Individual.dataset = data

# %%
