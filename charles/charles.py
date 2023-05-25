from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy


class Individual:
    def __init__(
        self,
        representation=None,
        size=None,
        replacement=True,
        valid_set=None,
    ):
        if representation is None:
            if replacement is True:
                self.representation = [choice(valid_set) for i in range(size)]
            elif replacement is False:
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"

    def __lt__(self, other):
        return self.fitness < other.fitness


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )

    def evolve(
        self,
        gens,
        xo_prob,
        mut_prob,
        select,
        mutate,
        crossover,
        elitism,
        xo_param=None,
        mut_param=None,
        sel_param=None,
    ):
        self.fitness_per_gen = []
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                if sel_param == None:
                    parent1, parent2 = select(self), select(self)
                else:
                    parent1, parent2 = select(self, sel_param), select(self, sel_param)

                if random() < xo_prob:
                    if xo_param == None:
                        offspring1, offspring2 = crossover(parent1, parent2)
                    else:
                        offspring1, offspring2 = crossover(
                            parent1,
                            parent2,
                            xo_param,
                        )
                else:
                    offspring1, offspring2 = parent1, parent2

                if mut_param == None:
                    if random() < mut_prob:
                        offspring1 = mutate(offspring1)
                    if random() < mut_prob:
                        offspring2 = mutate(offspring2)
                else:
                    if random() < mut_prob:
                        offspring1 = mutate(offspring1, sel_param)
                    if random() < mut_prob:
                        offspring2 = mutate(offspring2, sel_param)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                best_individual = min(self, key=attrgetter("fitness"))
                # print(f"Best Individual: {best_individual}")
                self.fitness_per_gen.append(best_individual.fitness)

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __lt__(self, other):
        return self.individuals < other.individuals
