from random import uniform, choice, sample
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=4):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))


def rank_sel(population, size=4):
    """
    Performs rank-based selection on a population.

    Args:
        population: The population to select from.
        size: The number of individuals to select.

    Returns:
        The selected individuals.
    """

    population.sort(key=lambda individual: individual.fitness)
    selected_individuals = []

    for _ in range(size):
        selected_individuals.append(population.pop(0))

    return selected_individuals
