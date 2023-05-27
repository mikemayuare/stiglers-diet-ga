# %%
from data.sd_data import data, nutrients
from charles.charles import Population, Individual
from charles.crossover import (
    uniform_crossover,
    arithmetic_xo,
    blx_alpha_xo,
    simplex_xo,
    entry_5050,
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
import numpy as np
import pandas as pd
import plotly.express as px


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


############ WARNING #############
# this will take time
# testing the operators in a gridsearch manner
# set passes to 1 if you want to test

crossovers = {
    "Uniform xo": uniform_crossover,
    "Arithmetic xo": arithmetic_xo,
    "Blend xo": blx_alpha_xo,
    "Simplex xo": simplex_xo,
    "Entry 50:50": entry_5050,
    "Single point xo": single_point_co,
    "Non-uniform xo": nux_xo,
}

mutations = {
    "Inversion mutation": inversion_mutation,
    "Gaussian mutation": gaussian_mutation,
    "Sine mutation": sine_mutation,
    "Power law mutation": power_law_mutation,
}


###### the following blocks were tested with a value of pass = 25 ####
###### Set to 1 to allow a shorter test
passes = 25
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


df = pd.DataFrame(results)
df = df.apply(lambda x: round(x, 3))
# df.to_csv("heatmap.csv")

fig = px.imshow(df, color_continuous_scale="teal", text_auto=True)
fig.write_image("images/heatmap.svg")

# Testing parameter on best XO operator Blend Crossover
mean_scores = {}

for alpha in np.arange(0.1, 2.1, 0.1):
    scores = []
    for j in range(passes):
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
            select=tournament_sel,
            mutate=power_law_mutation,
            crossover=blx_alpha_xo,
            xo_param=alpha,
            mut_prob=0.1,
            xo_prob=0.9,
            elitism=True,
        )
        best_individual = min(pop.individuals, key=attrgetter("fitness"))
        scores.append(best_individual.fitness)

    mean_scores[round(alpha, 1)] = sum(scores) / passes

fig = px.line(
    x=[key for key in mean_scores.keys()], y=[value for value in mean_scores.values()]
)
fig.update_layout(xaxis_title="alpha", yaxis_title="Fitness score")
fig.write_image("images/alpha-tuning.svg")

mean_scores = {}
for size in range(2, 11):
    scores = []
    for j in range(passes):
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
            select=tournament_sel,
            mutate=power_law_mutation,
            crossover=blx_alpha_xo,
            xo_param=0.8,
            sel_param=size,
            mut_prob=0.1,
            xo_prob=0.9,
            elitism=True,
        )
        best_individual = min(pop.individuals, key=attrgetter("fitness"))
        scores.append(best_individual.fitness)

    mean_scores[round(size, 1)] = sum(scores) / passes

fig = px.line(
    x=[key for key in mean_scores.keys()], y=[value for value in mean_scores.values()]
)
fig.update_layout(xaxis_title="Tournament size", yaxis_title="Fitness score")
fig.write_image("images/tournament-tuning.svg")

# Testing the mutation parameter
mean_scores = {}
for exponent in range(1, 6):
    scores = []
    for j in range(passes):
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
            select=tournament_sel,
            mutate=power_law_mutation,
            crossover=blx_alpha_xo,
            xo_param=0.8,
            sel_param=4,
            mut_param=exponent,
            mut_prob=0.1,
            xo_prob=0.9,
            elitism=True,
        )
        best_individual = min(pop.individuals, key=attrgetter("fitness"))
        scores.append(best_individual.fitness)

    mean_scores[round(exponent, 1)] = sum(scores) / passes

fig = px.line(
    x=[key for key in mean_scores.keys()], y=[value for value in mean_scores.values()]
)
fig.update_layout(xaxis_title="Exponent", yaxis_title="Fitness score")
fig.write_image("images/power-tuning.svg")

# %%
# testing a single run and plotting the best fitness score
# of each generation
pop = Population(
    size=100,
    sol_size=len(data),
    valid_set=[
        0 if random.random() < 0.85 else random.uniform(0, 0.35) for _ in range(50000)
    ],
    replacement=True,
    optim="min",
)

pop.evolve(
    gens=200,
    select=rank_sel,
    mutate=power_law_mutation,
    crossover=blx_alpha_xo,
    xo_param=1,
    # sel_param=4,
    mut_param=5,
    mut_prob=0.1,
    xo_prob=0.9,
    elitism=True,
)

fig = px.line(x=range(1, 201), y=pop.fitness_per_gen)
fig.update_layout(xaxis_title="Generation", yaxis_title="Best fitness")
fig.write_image("images/evolution2.svg")

best_individual = min(pop.individuals, key=attrgetter("fitness"))
best_fitness = best_individual.fitness
best_representation = best_individual.representation
best_representation = [0 if i < 1e-4 else round(i, 2) for i in best_representation]

print(
    f"Expenditure per day: {round(best_fitness, 2)}$\n"
    f"Yearly expenditure: {round(best_fitness * 365, 2)}$\n"
)

for key, value in best_individual.total_nutrients.items():
    print(f"{key}:__{round(value, 2)}__")

print("\n")

commodities = []
for food in data:
    commodities.append(food["Commodity"])

commodities = zip(commodities, best_representation)
best_foods = []
for commodity, value in commodities:
    if value != 0:
        best_foods.append((commodity, value))

for commodity, value in best_foods:
    print(f"{commodity}:__{value}$__")

# %%
