from random import randint, sample, uniform, random
from copy import deepcopy


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1) - 2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def pmx(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(p1)), 2)
    # xo_points = [3,6]
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x)
        # offspring2
        o[xo_points[0] : xo_points[1]] = x[xo_points[0] : xo_points[1]]
        z = set(y[xo_points[0] : xo_points[1]]) - set(x[xo_points[0] : xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        # numbers that doesn't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2


def arithmetic_xo(p1, p2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = uniform(0, 1)
    o1 = [None] * len(p1)
    o2 = [None] * len(p1)
    for i in range(len(p1)):
        o1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        o2[i] = p2[i] * alpha + (1 - alpha) * p1[i]
    return o1, o2


def blx_alpha_xo(p1, p2, alpha=0.8):
    """
    Performs Blend Alpha Crossover (BLX-α) between two parent solutions.

    Args:
        p1 (list): The first parent solution represented as a list of real numbers.
        p2 (list): The second parent solution represented as a list of real numbers.
        alpha (float, optional): The blending factor controlling the range of the offspring solutions. Default is 0.1.

    Returns:
        o1 (list): The first offspring solution generated by BLX-α crossover.
        o2 (list): The second offspring solution generated by BLX-α crossover.
    """
    size = len(p1)

    o1 = [None] * size
    o2 = [None] * size

    for i in range(size):
        # Determine the lower and upper bounds for the blending range
        min_val = min(p1[i], p2[i])
        max_val = max(p1[i], p2[i])

        # Calculate the range of the blending region
        range_val = max_val - min_val

        # Calculate the lower and upper bounds of the offspring
        low = min_val - alpha * range_val
        high = max_val + alpha * range_val

        # Generate a random value within the blending range
        # ensure genes are non-negative
        o1[i] = max(0, uniform(low, high))
        o2[i] = max(0, uniform(low, high))

    return o1, o2


def simplex_xo(p1, p2):
    """
    Performs simplex crossover on two parents.

    Args:
        p1: The first parent.
        p2: The second parent.

    Returns:
        The two children created by modified uniform crossover.
    """
    # Construct the simplex
    simplex = [p1, p2]
    size = len(p1)

    # Add a random point within the line segment connecting p1 and p2
    random_point = []
    for i in range(size):
        alpha = uniform(0, 1)
        random_coordinate = p1[i] + alpha * (p2[i] - p1[i])
        random_point.append(random_coordinate)
    simplex.append(random_point)

    # Generate offspring
    o1 = []
    o2 = []
    for i in range(size):
        coordinates = [
            vertex[i] for vertex in simplex
        ]  # Get the coordinates of the vertices along the i-th dimension
        min_coordinate = min(coordinates)
        max_coordinate = max(coordinates)

        # Randomly select a point within the range defined by the min and max coordinates
        offspring_coordinate = uniform(min_coordinate, max_coordinate)
        o1.append(offspring_coordinate)

        # Generate a second offspring by taking the average of the parent genes
        avg_coordinate = sum(coordinates) / len(coordinates)
        o2.append(avg_coordinate)

    return o1, o2


def uniform_crossover(p1, p2):
    """
    Performs uniform crossover on two parents.

    Args:
        p1: The first parent.
        p2: The second parent.

    Returns:
        The two children created by modified uniform crossover.
    """

    crossover_point1 = randint(0, len(p1) - 1)
    crossover_point2 = randint(crossover_point1 + 1, len(p1))

    o1 = (
        p1[:crossover_point1]
        + p2[crossover_point1:crossover_point2]
        + p1[crossover_point2:]
    )
    o2 = (
        p2[:crossover_point1]
        + p1[crossover_point1:crossover_point2]
        + p2[crossover_point2:]
    )

    return o1, o2


def nux_xo(p1, p2, eta=5):
    o1 = deepcopy(p1)
    o2 = deepcopy(p2)
    size = len(p1)

    for i in range(size):
        if random() < 0.8:
            beta = (1 - (random() ** (1 / (eta + 1)))) ** (1 / (eta + 1))

            if random() < 0.5:
                delta = (1 - beta) * (o1[i] - o2[i])
                o1[i] = max(0, o1[i] - delta)
                o2[i] = max(0, o2[i] + delta)
            else:
                delta = (1 - beta) * (o1[i] - o2[i])
                o1[i] = max(0, o1[i] + delta)
                o2[i] = max(0, o2[i] - delta)
    return o1, o2


def entry_5050(p1, p2):
    """
    Perform a 50/50 entry crossover between two parents.

    This function takes two parent chromosomes and performs a crossover operation
    where each corresponding gene in the offspring has a 50% chance of being copied
    from one parent or the other.

    Args:
        p1 (list): The first parent chromosome.
        p2 (list): The second parent chromosome.

    Returns:
        tuple of lists: A tuple containing the two offspring chromosomes.
    """

    o1 = deepcopy(p1)
    o2 = deepcopy(p2)
    size = len(p1)

    for i in range(size):
        if random() < 0.5:
            o1[i] = p2[i]
        if random() < 0.5:
            o2[i] = p1[i]
    return o1, o2


if __name__ == "__main__":
    # p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    p1, p2 = [0.1, 0.15, 0.3], [0.3, 0.1, 0.2]
    o1, o2 = arithmetic_xo(p1, p2)
    print(o1, o2)
