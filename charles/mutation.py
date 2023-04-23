from random import randint


def binary_mutation(individual, p=0.1):
    mut_index = randint(len(individual) - 1)
    if individual[mut_index] == 0
        individual[mut_index] = 1
    elif individual[mut_index] == 1
        individual[mut_index] = 0
    return individual
    

