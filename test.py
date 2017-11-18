from graph import Graph
from simulation import simulation
from visualize import visualize_simulation

if __name__ == '__main__':
    graph_file = 'graphs/random.txt'
    ff_per_step = 2

    graph = Graph.from_file(graph_file)
    solution = range(1, 10)

    transitions, score = simulation(graph, solution, ff_per_step=ff_per_step)
    print "\nNodes saved: {}\nNodes occupied by ff: {}".format(score.nodes_saved, score.nodes_occupied_by_ff)
    print "Iterations elapsed: {}\n".format(score.extinguishing_time)

    visualize_simulation(graph, transitions, solution)
