from graph import Graph
from simulation import simulation
from solvers import run_framework
from visualize import visualize_simulation


def genetic_solution(graph_file, ff_per_step):
    algo_out = run_framework(loggers='',
                             population_size=100,
                             selection='roulette',
                             crossover='injection',
                             mutation='single_swap',
                             succession='best',
                             iters=1000,
                             ffs=ff_per_step,
                             input_file=graph_file)

    graph = Graph.from_file(graph_file)
    return graph, algo_out.best_solution


if __name__ == '__main__':
    from generate import generate_file_data

    vnum = 20
    generate_file_data('graphs/random.rgraph', vertices_num=vnum, density=0.2, starting_vertices_num=2)

    graph_file = 'graphs/random.rgraph'
    ff_per_step = 2

    graph = Graph.from_file(graph_file)
    graph, solution = genetic_solution(graph_file, ff_per_step)

    transitions, score = simulation(graph, solution, ff_per_step=ff_per_step)
    print "Nodes saved: {}\nNodes occupied by ff: {}".format(score.nodes_saved, score.nodes_occupied_by_ff)

    visualize_simulation(graph, transitions, solution)
