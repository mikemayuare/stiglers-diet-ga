from random import choices, uniform, choice
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Sum total fitness
    total_fitness = sum([i.fitness for i in population])
    # Get a 'position' on the wheel
    spin = uniform(0, total_fitness)

    if population.optim == "max":
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        position = total_fitness
        # Find individual in the position of the spin
        for individual in population:
            position -= individual.fitness
            if position < spin:
                return individual

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


def rank_sel2(population):
    """Rank selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: The selected individual.
    """

    # Assign ranks to individuals based on fitness
    sorted_individuals = sorted(population.individuals, key=attrgetter("fitness"))
    ranks = list(range(1, len(sorted_individuals) + 1))

    # Calculate selection probabilities
    probabilities = [1 / rank for rank in ranks]
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]

    # Select an individual based on ranks and probabilities
    selected_individual = choices(sorted_individuals, probabilities)[0]

    return selected_individual


def rank_sel(population):
    """Ranking selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        pop_sorted = sorted(population.individuals, key=attrgetter("fitness"))
    elif population.optim == "min":
        pop_sorted = sorted(
            population.individuals, key=attrgetter("fitness"), reverse=True
        )
    else:
        raise Exception("No optimization specified (min or max).")

    probs = [
        (rank + 1) / sum(range(len(pop_sorted) + 1))
        for rank, _ in enumerate(pop_sorted)
    ]

    return choices(pop_sorted, probs)[0]
