import copy
import random
import sys
from collections.abc import Callable, Iterator
from concurrent import futures
from dataclasses import InitVar, dataclass, field
from operator import attrgetter
from typing import Any, Literal


@dataclass(slots=True, kw_only=True)
class GeneticAlgorithm[T]:
    """Base Genetic Algorithm class.

    Arguments:
        gene_pool: all ancestors to choose from
        fitness_function: function that calculates the ranking of a given solution
        min_sample: minimum size of a solution
        max_sample: maximum size of a solution

        population_size: size of each generation
        generations: number of generations
        crossover_probability: chance of crossover
        mutation_probability: chance of mutation
        elitism: whether to apply elitism
        maximise_fitness: whether to maximise fitness
        verbose: debug
        random_seed: seed for the random
    """

    gene_pool: list[T] = field(kw_only=False)
    fitness_function: Callable[[list[T]], float] = field(kw_only=False)

    min_sample: int = 1
    max_sample: int = 50

    population_size: int = 50
    generations: int = 100
    crossover_probability: float = 0.8
    mutation_probability: float = 0.4
    tournament_size: int = 5
    elitism: bool = True
    maximise_fitness: bool = True
    verbose: bool = False
    random_state: InitVar[int | None] = None
    rnd: random.Random = field(init=False)

    current_generation: list[T] = field(default_factory=list)

    def __post_init__(self, random_state: int | None = None) -> None:
        self.rnd = random.Random(random_state)

    def create_individual(self, seed_data: list[T]) -> list[T]:
        """Create a candidate solution based on a selection of genes."""
        return self.rnd.choices(seed_data, k=self.rnd.randint(self.min_sample, self.max_sample))

    def crossover(self, parent_1: list[T], parent_2: list[T]) -> tuple[list[T], list[T]]:
        """Crossover (mate) two parents to produce two children.

        :param parent_1: candidate solution representation (list)
        :param parent_2: candidate solution representation (list)
        :returns: tuple containing two children

        """
        index = self.rnd.randint(1, min(len(parent_1), len(parent_2)))
        child_1 = parent_1[:index] + parent_2[index:]
        child_2 = parent_2[:index] + parent_1[index:]
        return child_1, child_2

    def mutate(self, genes: list[T]) -> list[T]:
        mutated = genes.copy()
        mutated_gene = self.rnd.randrange(0, len(genes))
        mutated[mutated_gene] = self.rnd.choice(self.gene_pool)
        return mutated

    def random_selection(self, population: list[T]) -> T:
        """Select and return a random member of the population."""
        return self.rnd.choice(population)

    def tournament_selection(self, population: list[T]) -> T:
        """Select a random number of individuals from the population and
        return the fittest member of them all.
        """
        if self.tournament_size == 0:
            self.tournament_size = 2
        members = self.rnd.sample(population, self.tournament_size)
        members.sort(key=attrgetter("fitness"), reverse=self.maximise_fitness)
        return members[0]

    def create_initial_population(self) -> None:
        """Create members of the first population randomly."""
        self.current_generation = [
            Chromosome[T](self.create_individual(self.gene_pool))
            for _ in range(self.population_size)
        ]

    def calculate_population_fitness(
            self, n_workers: int = 1, parallel_type: Literal["process", "thread"] = "process"
    ) -> None:
        """Calculate the fitness of every member of the given population using the supplied fitness_function."""
        # If using a single worker, run on a simple for loop to avoid losing
        # time creating processes.
        if n_workers == 1:
            for individual in self.current_generation:
                individual.fitness = self.fitness_function(individual.genes)
        else:
            if "process" in parallel_type.lower():
                executor = futures.ProcessPoolExecutor(max_workers=n_workers)
            else:
                executor = futures.ThreadPoolExecutor(max_workers=n_workers)

            # Create two lists from the same size to be passed as args to the
            # map function.
            genes = [individual.genes for individual in self.current_generation]
            data = [self.gene_pool for _ in self.current_generation]

            with executor as pool:
                results = pool.map(self.fitness_function, genes, data)

            for individual, result in zip(self.current_generation, results):
                individual.fitness = result

    def rank_population(self) -> None:
        """Sort the population by fitness according to the order defined by
        maximise_fitness.
        """
        self.current_generation.sort(key=attrgetter("fitness"), reverse=self.maximise_fitness)

    def create_new_population(self) -> None:
        """Create a new population using the genetic operators (selection,
        crossover, and mutation) supplied.
        """
        new_population = []
        elite = copy.deepcopy(self.current_generation[0])
        selection = self.tournament_selection

        while len(new_population) < self.population_size:
            parent_1 = copy.deepcopy(selection(self.current_generation))
            parent_2 = copy.deepcopy(selection(self.current_generation))

            child_1, child_2 = parent_1, parent_2
            child_1.fitness, child_2.fitness = 0, 0

            can_crossover = self.rnd.random() < self.crossover_probability
            can_mutate = self.rnd.random() < self.mutation_probability

            if can_crossover:
                child_1.genes, child_2.genes = self.crossover(parent_1.genes, parent_2.genes)

            if can_mutate:
                child_1.genes = self.mutate(child_1.genes)
                child_2.genes = self.mutate(child_2.genes)

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)

        if self.elitism:
            new_population[0] = elite

        self.current_generation = new_population

    def create_first_generation(self, n_workers: int = 1, parallel_type:Literal["process", "thread"]="process") -> None:
        """Create the first population, calculate the population's fitness and
        rank the population by fitness according to the order specified."""
        self.create_initial_population()
        self.calculate_population_fitness(n_workers=n_workers, parallel_type=parallel_type)
        self.rank_population()
        if self.verbose:
            debug(f"Fitness:{self.best_individual()[0]}")

    def create_next_generation(self, n_workers: int = 1, parallel_type:Literal["process", "thread"]="process") -> None:
        """Create subsequent populations, calculate the population fitness and
        rank the population by fitness in the order specified.
        """
        self.create_new_population()
        self.calculate_population_fitness(n_workers=n_workers, parallel_type=parallel_type)
        self.rank_population()
        if self.verbose:
            debug(f"Fitness:{self.best_individual()[0]}")

    def run(self, n_workers: int = 1, parallel_type:Literal["process", "thread"]="processi") -> None:
        """Run (solve) the Genetic Algorithm."""
        self.create_first_generation(n_workers=n_workers, parallel_type=parallel_type)

        for _ in range(1, self.generations):
            self.create_next_generation(n_workers=n_workers, parallel_type=parallel_type)

    def best_individual(self) -> tuple[float, list[T]]:
        """Return the individual with the best fitness in the current
        generation.
        """
        best = self.current_generation[0]
        return best.fitness, best.genes

    def last_generation(self) -> Iterator[tuple[float, list[T]]]:
        """Return members of the last generation as a generator function."""
        for member in self.current_generation:
            yield member.fitness, member.genes


@dataclass(slots=True)
class Chromosome[T]:
    genes: list[T]
    fitness: float = 0.0


type Bottle = tuple[int, ...]
# target = tuple(int(x) for x in input().split())
# bottles = [tuple(int(x) for x in input().split()) for _ in range(int(input()))]

target = (50, 100, 150, 200, 250, 300, 350, 400, 450, 500)
bottles = [
    (34, 98, 297, 175, 122, 6, 0, 0, 0, 501),
    (75, 0, 0, 0, 0, 181, 0, 414, 0, 913),
    (10, 173, 91, 0, 480, 179, 555, 0, 0, 845),
    (36, 9, 0, 0, 13, 0, 545, 469, 801, 316),
    (0, 184, 195, 225, 70, 255, 569, 0, 745, 25),
    (17, 39, 35, 221, 289, 228, 0, 0, 278, 383),
    (18, 0, 289, 352, 0, 0, 253, 446, 0, 655),
    (0, 74, 0, 0, 300, 125, 680, 8, 41, 550),
    (0, 112, 100, 83, 227, 193, 104, 710, 760, 377),
    (0, 29, 99, 127, 76, 293, 34, 0, 573, 979),
    (33, 0, 108, 282, 483, 193, 70, 101, 0, 0),
    (76, 81, 119, 0, 0, 357, 0, 260, 687, 72),
    (13, 59, 178, 303, 0, 600, 18, 378, 536, 565),
    (78, 113, 205, 0, 295, 232, 0, 0, 266, 177),
    (0, 153, 159, 227, 56, 214, 0, 0, 620, 823),
    (94, 125, 211, 112, 138, 0, 0, 527, 0, 421),
    (0, 13, 124, 124, 0, 0, 115, 551, 319, 940),
    (100, 0, 68, 191, 104, 206, 127, 697, 855, 457),
    (0, 153, 218, 266, 352, 260, 478, 98, 605, 308),
    (0, 114, 235, 284, 120, 227, 167, 55, 280, 0),
]


def fitness(selected: list[Bottle]) -> float:
    mix = tuple(sum(bottle[i] for bottle in selected) / len(selected) for i in range(10))
    offset = sum((t - c) ** 2 for t, c in zip(target, mix))
    return (1.0 - (offset / sum(t ** 2 for t in target))) * 1_000_000


def debug(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs, file=sys.stderr, flush=True)


ga = GeneticAlgorithm[Bottle](
    gene_pool=bottles,
    fitness_function=fitness,
    generations=50,
    population_size=400,
    min_sample=30,
    max_sample=50,
    crossover_probability=0.9,
    verbose=True,
)
ga.run()
best_score, best_bottles = ga.best_individual()
debug(target)
debug(bottles)
debug(best_score)
debug()
print(" ".join(str(bottles.index(bottle) + 1) for bottle in best_bottles))
