from graph import Graph
from simulation import simulation

if __name__ == '__main__':


    graph_file = 'graphs/random.txt'
    ff_per_step = 4

    graph = Graph.from_file(graph_file)
    solution = range(1, 10)

    transitions, score = simulation(graph, solution, ff_per_step=ff_per_step)
    print "Nodes saved: {}\nNodes occupied by ff: {}".format(score.nodes_saved, score.nodes_occupied_by_ff)
