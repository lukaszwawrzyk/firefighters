from graph import Graph
from operators.crossover import cycle_crossover
from operators.mutation import inversion_mutation
from operators.selection import tournament_selection
from operators.succession import best_then_uniform_succession
from simulation import simulation
import random


if __name__ == '__main__':

    graph_file = 'graphs/random.txt'
    ff_per_step = 2

    graph = Graph.from_file(graph_file)

    def fitness(specimen):
        _, score = simulation(graph, specimen, ff_per_step)
        return score.nodes_saved

    def evaluate(population):
        return [(specimen, fitness(specimen)) for specimen in population]


    population_size = 1000
    number_of_selected = 300

    indices = range(graph.nodes_number)
    original_population = [list(indices) for _ in range(population_size)]
    for specimen in original_population:
        random.shuffle(specimen)

    # selection
    population_with_fitness = evaluate(original_population)
    selected = tournament_selection(population_with_fitness, number_of_selected)

    # crossover
    crossed_over = list()
    for i in range(number_of_selected / 2):
        parent1 = selected[2*i]
        parent2 = selected[2*i+1]
        child1, child2 = cycle_crossover(parent1, parent2)
        crossed_over.append(child1)
        crossed_over.append(child2)

    # mutation
    mutated = [inversion_mutation(specimen) for specimen in crossed_over]

    new_specimen = mutated

    # succession
    new_population_before_succession = evaluate(original_population + new_specimen)
    new_population = best_then_uniform_succession(new_population_before_succession, population_size, perc_best=0.50)

    for specimen, _ in new_population:
        assert sorted(specimen) == indices
