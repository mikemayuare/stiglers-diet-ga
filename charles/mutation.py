from random import randint, sample


def binary_mutation(individual):
    """Binary mutation for a GA individual. Flips the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_index = randint(0, len(individual) - 1)

    if individual[mut_index] == 0:
        individual[mut_index] = 1
    elif individual[mut_index] == 1:
        individual[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")
    return individual


def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    #mut_indexes = [0,3]
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


def gaussian_mutation(individual):
    mutant = deepcopy(individual)
    size = len(individual)

    for i in range(size):
        # mean and std are randonmly chosen
        mut_value = gauss(uniform(0, 0.35), uniform(0, 0.35))

        if random < 0.5:
            mutant[i] = max(0, mutant[i] + mut_value)
        else:
            mutant[i] = max(0, mutant[i] - mut_value)
    return mutant


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6]
    test = inversion_mutation(test)
    print(test)
















