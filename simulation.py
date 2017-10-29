from logging import getLogger

from graph import NodeState

logger = getLogger("simulation")


class Score(object):
    def __init__(self, putting_out_time, nodes_saved, nodes_occupied_by_ff):
        # in iterations
        self.putting_out_time = putting_out_time
        self.nodes_saved = nodes_saved
        self.nodes_occupied_by_ff = nodes_occupied_by_ff

    def __str__(self):
        return "[T: {}, SAVED: {}, SAVED_FF: {}]".format(self.putting_out_time, self.nodes_saved,
                                                         self.nodes_occupied_by_ff)


def set_initial_nodes_on_fire(graph, transitions):
    # we will store initial fire in the very first element
    transitions[0] = list()
    for init_node in graph.get_init_nodes():
        graph.set_node_as_burning(init_node)
        transitions[0].append((init_node.id, NodeState.BURNING))

    return transitions


def spreading_finished(graph):
    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.get_neighbors():
            if neighbor.state == NodeState.UNTOUCHED:
                return False
    return True


def assign_firefighters(graph, solution, solution_index, n, transitions):
    step = transitions.keys()[-1] + 1
    transitions[step] = list()

    placed_ff = 0
    while placed_ff < n and solution_index < graph.nodes_number:
        if graph.nodes[solution[solution_index]].state == NodeState.UNTOUCHED:
            graph.nodes[solution[solution_index]].state = NodeState.DEFENDED
            transitions[step].append((solution[solution_index], NodeState.DEFENDED))
            placed_ff += 1
        else:
            solution_index += 1
    return solution_index, transitions


def spread_fire(graph, transitions):
    step = transitions.keys()[-1] + 1
    transitions[step] = list()

    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.get_neighbors():
            if neighbor.state == NodeState.UNTOUCHED:
                graph.set_node_as_burning(neighbor)
                transitions[step].append((neighbor.id, NodeState.BURNING))

    return transitions


def evaluate_result(graph):
    saved_ff = 0
    saved_no_ff = 0
    for node in graph.nodes.values():
        if node.state != NodeState.BURNING:
            if node.state == NodeState.DEFENDED:
                saved_ff += 1
            else:
                saved_no_ff += 1
    return saved_ff, saved_no_ff


def simulation(graph, solution, ff_per_step):
    # save nodes transitions to visualize the process
    transitions = dict()
    graph.reset_state()

    transitions = set_initial_nodes_on_fire(graph, transitions)

    solution_index = 0
    iterations = 0
    while not spreading_finished(graph):
        solution_index, transitions = assign_firefighters(graph, solution, solution_index, ff_per_step, transitions)
        transitions = spread_fire(graph, transitions)
        iterations += 1
    logger.info("It took {} iterations for the fire to stop spreading".format(iterations))

    saved_ff, saved_no_ff = evaluate_result(graph)
    all_saved = saved_ff + saved_no_ff
    logger.info("Result: {} (saved nodes, from them {} occupied by firefighters)".format(all_saved, saved_ff))

    return transitions, Score(iterations, all_saved, saved_ff)
