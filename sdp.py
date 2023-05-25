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
from charles.selection import (
    tournament_sel,
    rank_sel,
    fps,
)
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


# %%
def test_ga(
    crossover,
    mutation,
    selection,
    # xo_param,
    # sel_param,
    mut_prob,
    xo_prob,
):
    pop = Population(
        size=100,
        sol_size=len(data),
        valid_set=[
            0 if random.random() < 0.85 else random.uniform(0, 0.35)
            for _ in range(50000)
        ],
        replacement=True,
        optim="min",
    )

    pop.evolve(
        gens=100,
        select=selection,
        mutate=mutation,
        crossover=crossover,
        # xo_param=xo_param,
        # sel_param=sel_param,
        mut_prob=mut_prob,
        xo_prob=xo_prob,
        elitism=True,
    )

    return pop


# %%
pop = test_ga(
    crossover=blx_alpha_xo,
    selection=tournament_sel,
    mutation=power_law_mutation,
    xo_param=0.8,
    sel_param=6,
    mut_prob=0.1,
    xo_prob=1,
)

# %%
best_individual = min(pop.individuals, key=attrgetter("fitness"))
# print(best_individual.representation)
print(best_individual.total_nutrients)
print(f"Yearly budget {best_individual.fitness * 365}")
# %%
crossovers = {
    "uniform_crossover": uniform_crossover,
    "arithmetic_xo": arithmetic_xo,
    "blx_alpha_xo": blx_alpha_xo,
    "simplex_xo": simplex_xo,
    "sbx_xo": sbx_xo,
    "single_point_co": single_point_co,
    "nux_xo": nux_xo,
}

mutations = {
    "inversion_mutation": inversion_mutation,
    "gaussian_mutation": gaussian_mutation,
    "sine_mutation": sine_mutation,
    "power_law_mutation": power_law_mutation,
}

passes = 5
results = {}
for xo_name, xo in crossovers.items():
    results[xo_name] = {}
    for mut_name, mut in mutations.items():
        ga_results = []
        for _ in range(passes):
            model = test_ga(
                crossover=xo,
                selection=tournament_sel,
                mutation=mut,
                # xo_param=0.8,
                # sel_param=6,
                mut_prob=0.1,
                xo_prob=0.9,
            )
            best_individual = min(model.individuals, key=attrgetter("fitness"))
            ga_results.append(best_individual.fitness)
        results[xo_name][mut_name] = sum(ga_results) / passes

print(results)


# %%
import pandas as pd

df = pd.DataFrame(results)
df.to_csv("heatmap.csv")

print(df)
# %%
import plotly.express as px

fig = px.imshow(df)
fig.write_image("images/heatmap.svg")
# %%
