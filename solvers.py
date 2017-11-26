import argparse

from frameworks import Operators, AlgoIn, ga_framework, DEFAULTS, random_population, strip_score
from generate import load_graph
from graph import Graph
from logging_configs import configure_logging
from operator_adapter import wrap_crossover, wrap_mutation, wrap_selection, wrap_succession
from operators import SELECTION, CROSSOVER, MUTATION, SUCCESSION
from random import sample


class ConfigurableSimpleSolver(Operators):
    def __init__(self, population_size=4, selection_op=None, crossover_op=None, mutation_op=None, succession_op=None,
                 mutation_count=2):
        super(ConfigurableSimpleSolver, self).__init__()

        self.population_size = population_size
        self.mutation_count = mutation_count

        if selection_op is not None:
            self.crossover_selection = wrap_selection(selection_op, 1, 2)
        if crossover_op is not None:
            self.crossover = wrap_crossover(crossover_op)
        if mutation_op is not None:
            self.mutation = wrap_mutation(mutation_op)
        if succession_op is not None:
            self.succession = wrap_succession(succession_op, population_size)

    def population_initialization(self, es):
        return random_population(es, self.population_size)

    def mutation_selection(self, es):
        base_population = strip_score(es.population)
        return sample(base_population, self.mutation_count)


def run_framework(loggers, population_size, selection, crossover, mutation, succession, iters, ffs, graph_props=None,
                  input_file=None):
    configure_logging(loggers)

    if input_file:
        g = Graph.from_file(input_file)
    elif graph_props:
        vertices, density, starting_vertices = graph_props
        g = load_graph(vertices, density, starting_vertices)
    else:
        raise ValueError('Either graph_props or input_file must be specified')

    operators = ConfigurableSimpleSolver(
        population_size=population_size,
        selection_op=SELECTION[selection],
        crossover_op=CROSSOVER[crossover],
        mutation_op=MUTATION[mutation],
        succession_op=SUCCESSION[succession],
    )
    return ga_framework(AlgoIn(g,
                               operators=operators,
                               iter_no=iters,
                               ffs_per_step=ffs,
                               gather_iteration_stats=True,
                               ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-in', '--input_file',
                        help='file containing graph')
    parser.add_argument('-d', '--density',
                        help='edges density; float in range [0..1]',
                        type=float,
                        default=0.2)
    parser.add_argument('-f', '--ffs',
                        help='number of firefighters per step',
                        type=int,
                        default=DEFAULTS['ffs_per_step'])
    parser.add_argument('-i', '--iters',
                        help='number of algorithm iterations',
                        type=int,
                        default=DEFAULTS['algo_iter_no'])
    parser.add_argument('-s', '--starting_vertices',
                        help='number of starting vertices',
                        type=int,
                        default=1)
    parser.add_argument('-v', '--vertices',
                        help='number of vertices in graph',
                        type=int,
                        default=10)
    parser.add_argument('-l', '--loggers',
                        help='configuration of loggers (i.e. graph_printing=info,benchmark_results=info)',
                        default='')
    parser.add_argument('-p', '--population_size',
                        help='size of the population',
                        type=int,
                        default=10)
    parser.add_argument('-os', '--selection',
                        help='selection operator',
                        choices=SELECTION.keys(),
                        default=SELECTION.keys()[0])
    parser.add_argument('-oc', '--crossover',
                        help='crossover operator',
                        choices=CROSSOVER.keys(),
                        default=CROSSOVER.keys()[0])
    parser.add_argument('-om', '--mutation',
                        help='mutation operator',
                        choices=MUTATION.keys(),
                        default=MUTATION.keys()[0])
    parser.add_argument('-oss', '--succession',
                        help='succession operator',
                        choices=SUCCESSION.keys(),
                        default=SUCCESSION.keys()[0])

    args = parser.parse_args()

    run_framework(args.loggers,
                  args.population_size,
                  args.selection,
                  args.crossover,
                  args.mutation,
                  args.succession,
                  args.iters,
                  args.ffs,
                  (args.vertices, args.density, args.starting_vertices),
                  args.input_file)
